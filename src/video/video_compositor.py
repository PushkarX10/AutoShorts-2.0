"""
AutoShorts 2.0 — Video Compositor.

Composites the animated chat overlay directly onto the processed 9:16 background video,
syncs with the master audio track, and renders a high-quality vertical MP4 YouTube Short.
Also generates an SRT subtitle track and thumbnail image.
"""
from __future__ import annotations

import math
import subprocess
import time
from pathlib import Path
from typing import Callable, Optional

from PIL import Image
from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn

from src.chat.chat_renderer import ChatRenderer
from src.config.settings import get, get_temp_dir
from src.models.schemas import Conversation, Timeline

console = Console()


def _format_srt_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp format: HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def generate_srt_subtitles(
    conversation: Conversation,
    timeline: Timeline,
    output_path: Path,
) -> Path:
    """Generate an SRT subtitle file from the timeline events."""
    char_map = {c.id: c.name for c in conversation.characters}
    lines: list[str] = []

    for idx, event in enumerate(timeline.events, start=1):
        char_name = char_map.get(event.character_id, event.character_id)
        start_ts = _format_srt_timestamp(event.voice_start_sec)
        end_ts = _format_srt_timestamp(event.display_end_sec)
        lines.append(str(idx))
        lines.append(f"{start_ts} --> {end_ts}")
        lines.append(f"{char_name}: {event.text}")
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def extract_thumbnail(
    video_path: Path,
    timeline: Timeline,
    output_path: Path,
) -> Path:
    """
    Extract a high-impact frame from the finished video for use as thumbnail.
    Prefers the punchline timestamp if available.
    """
    # Find punchline or message near 70% of video
    thumb_time = timeline.total_duration_sec * 0.7
    for event in timeline.events:
        if event.is_punchline:
            thumb_time = event.bubble_appear_sec + 0.3
            break

    thumb_time = max(0.5, min(thumb_time, timeline.total_duration_sec - 0.5))

    cmd = [
        "ffmpeg", "-y",
        "-ss", f"{thumb_time:.3f}",
        "-i", str(video_path),
        "-vframes", "1",
        "-q:v", "2",
        str(output_path),
    ]
    subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return output_path


def compose_video(
    background_video_path: Path,
    conversation: Conversation,
    timeline: Timeline,
    master_audio_path: Path,
    output_path: Path,
    progress_callback: Optional[Callable[[int, str], None]] = None,
) -> Path:
    """
    Composites chat frames over the background video along with master audio.

    Args:
        background_video_path: Path to vertical 1080x1920 background MP4.
        conversation: Conversation data model.
        timeline: Frame-accurate animation timeline.
        master_audio_path: Synchronized master WAV audio.
        output_path: Final destination MP4 file.
        progress_callback: Optional function receiving (percentage: int, message: str).

    Returns:
        Path to the rendered MP4 file.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    video_cfg = get("video", default={})
    width = video_cfg.get("width", 1080)
    height = video_cfg.get("height", 1920)
    fps = video_cfg.get("fps", 30)
    codec = video_cfg.get("codec", "libx264")
    crf = video_cfg.get("crf", 18)
    preset = video_cfg.get("preset", "fast")
    audio_codec = video_cfg.get("audio_codec", "aac")
    audio_bitrate = video_cfg.get("audio_bitrate", "192k")

    total_duration = timeline.total_duration_sec
    total_frames = timeline.total_frames
    if total_frames <= 0:
        total_frames = int(total_duration * fps)

    console.print(f"[cyan]🎬[/cyan] Initializing chat renderer ({total_frames} frames @ {fps} fps)…")
    renderer = ChatRenderer(conversation, timeline)

    # Build FFmpeg command:
    # Input 0: Background video (looped or pre-cut to duration)
    # Input 1: Pipe raw RGBA video frames
    # Input 2: Master audio track
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", str(background_video_path),
        "-f", "rawvideo",
        "-pix_fmt", "rgba",
        "-s", f"{width}x{height}",
        "-r", str(fps),
        "-i", "pipe:0",
        "-i", str(master_audio_path),
        "-filter_complex", "[0:v][1:v]overlay=0:0[vout]",
        "-map", "[vout]",
        "-map", "2:a",
        "-c:v", codec,
        "-preset", preset,
        "-crf", str(crf),
        "-pix_fmt", "yuv420p",
        "-r", str(fps),
        "-c:a", audio_codec,
        "-b:a", str(audio_bitrate),
        "-t", f"{total_duration:.3f}",
        "-movflags", "+faststart",
        str(output_path),
    ]

    console.print(f"[cyan]⏳[/cyan] Rendering chat frames and compositing video…")
    t_start = time.time()
    log_file_path = output_path.with_name(f"{output_path.stem}_ffmpeg.log")

    with open(log_file_path, "w", encoding="utf-8", errors="replace") as log_f:
        proc = subprocess.Popen(
            ffmpeg_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=log_f,
        )

        if proc.stdin is None:
            raise RuntimeError("Failed to open stdin pipe to FFmpeg.")

        update_interval = max(1, total_frames // 40)

        try:
            for frame_idx in range(total_frames):
                t_sec = frame_idx / fps
                frame_img = renderer.render_frame(t_sec)
                proc.stdin.write(frame_img.tobytes())

                if frame_idx % update_interval == 0 or frame_idx == total_frames - 1:
                    pct = int((frame_idx + 1) / total_frames * 100)
                    elapsed = time.time() - t_start
                    fps_render = (frame_idx + 1) / max(elapsed, 0.001)
                    desc = f"Compositing: {pct}% ({fps_render:.1f} fps)"
                    if progress_callback:
                        progress_callback(pct, desc)

            proc.stdin.close()
        except Exception as e:
            proc.kill()
            raise RuntimeError(f"Error while feeding frames to FFmpeg: {e}")

        proc.wait(timeout=300)

    stderr_text = log_file_path.read_text(encoding="utf-8", errors="replace") if log_file_path.exists() else ""
    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg compositing failed with code {proc.returncode}:\n{stderr_text[-1200:]}")

    log_file_path.unlink(missing_ok=True)

    if not output_path.exists() or output_path.stat().st_size < 10000:
        raise RuntimeError(f"Rendered video is missing or too small: {output_path}")

    elapsed_total = time.time() - t_start
    console.print(f"[green]✓[/green] Video composition complete in {elapsed_total:.1f}s → {output_path.name}")

    # Generate companion subtitle file (.srt)
    srt_path = output_path.with_suffix(".srt")
    generate_srt_subtitles(conversation, timeline, srt_path)

    # Generate companion thumbnail (.jpg)
    thumb_path = output_path.with_name(f"{output_path.stem}_thumbnail.jpg")
    extract_thumbnail(output_path, timeline, thumb_path)

    return output_path
