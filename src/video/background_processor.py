"""
AutoShorts 2.0 — Background Video Processor.

Takes raw gaming footage and produces a normalized 9:16 vertical video:
  • Crops or pads with blurred fill to fit 1080×1920.
  • Loops short clips seamlessly.
  • Applies optional darkening for chat readability.
  • Mutes original audio.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from rich.console import Console

from src.config.settings import get, get_temp_dir
from src.models.schemas import VideoInfo

console = Console()


def process_background(
    video_info: VideoInfo,
    target_duration: float,
    output_path: str | Path | None = None,
) -> Path:
    """
    Process raw gaming footage into a vertical 9:16 background video.

    Returns the path to the processed MP4.
    """
    src = Path(video_info.path)
    if output_path is None:
        output_path = get_temp_dir() / "processed_bg.mp4"
    else:
        output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists() and output_path.stat().st_size > 100000:
        console.print(f"[green]✓[/green] Reusing processed background: {output_path.name}")
        return output_path

    width = get("video", "width", 1080)
    height = get("video", "height", 1920)
    fps = get("video", "fps", 30)
    darken = get("video", "background_darken", 0.3)

    console.print(f"[cyan]⏳[/cyan] Processing background: {video_info.filename} → {width}×{height}")

    # Build the FFmpeg filter chain
    filters = _build_filter_chain(video_info, width, height, fps, darken, target_duration)

    cmd = [
        "ffmpeg", "-y",
        "-i", str(src),
    ]

    # If we need to loop because source is shorter than target
    if video_info.duration > 0 and video_info.duration < target_duration:
        loop_count = int(target_duration / video_info.duration) + 1
        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", str(loop_count),
            "-i", str(src),
        ]

    cmd += [
        "-t", str(target_duration),
        "-filter_complex", filters,
        "-map", "[vout]",
        "-an",                        # mute original audio
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-r", str(fps),
        "-movflags", "+faststart",
        str(output_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        raise RuntimeError(f"Background processing failed:\n{result.stderr[-1000:]}")

    if not output_path.exists() or output_path.stat().st_size < 1000:
        raise RuntimeError("Background processing produced empty or missing output.")

    console.print(f"[green]✓[/green] Background processed → {output_path.name}")
    return output_path


def _build_filter_chain(
    info: VideoInfo,
    target_w: int,
    target_h: int,
    fps: int,
    darken: float,
    duration: float,
) -> str:
    """
    Build an FFmpeg filter_complex string that:
    1. Creates a blurred+scaled background fill layer.
    2. Scales the main video to fit within 1080×1920 (no stretch).
    3. Overlays the sharp video centered on the blurred fill.
    4. Applies a darkening overlay for chat readability.
    """
    target_ratio = target_w / target_h  # 0.5625 for 9:16
    src_ratio = info.width / max(info.height, 1)

    # Strategy: always create blurred fill + centered sharp overlay
    # This handles landscape, portrait, and square sources gracefully.

    fit_mode = get("video", "fit_mode", "crop")
    filters = []

    # If fit_mode is crop (default for shorts/reels) or video is already vertical, center-crop to 9:16
    if fit_mode == "crop" or info.orientation == "portrait" or abs(src_ratio - target_ratio) < 0.05:
        filters.append(
            f"[0:v]fps={fps},setpts=PTS-STARTPTS,"
            f"scale={target_w}:{target_h}:force_original_aspect_ratio=increase,"
            f"crop={target_w}:{target_h},setsar=1[composed]"
        )
    else:
        # Landscape/Square: fast blurred fill by downscaling before blur
        filters.append(f"[0:v]fps={fps},setpts=PTS-STARTPTS[src]")
        filters.append(
            f"[src]split=2[bg_src][fg_src];"
            f"[bg_src]scale=270:480:force_original_aspect_ratio=increase,"
            f"crop=270:480,boxblur=6:6,scale={target_w}:{target_h}[bg_blur];"
            f"[fg_src]scale={target_w}:{target_h}:force_original_aspect_ratio=decrease,"
            f"pad={target_w}:{target_h}:(ow-iw)/2:(oh-ih)/2:color=black@0[fg_scaled];"
            f"[bg_blur][fg_scaled]overlay=0:0[composed]"
        )

    # Apply darkening
    if darken > 0:
        # Use a dark color overlay with blend
        alpha = min(darken, 0.6)
        hex_alpha = format(int(alpha * 255), "02x")
        filters.append(
            f"color=black@{alpha}:s={target_w}x{target_h}[dark];"
            f"[composed][dark]overlay=0:0:shortest=1[vout]"
        )
    else:
        filters.append("[composed]copy[vout]")

    return ";".join(filters)
