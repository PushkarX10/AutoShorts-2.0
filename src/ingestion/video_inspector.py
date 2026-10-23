"""
AutoShorts 2.0 — Video Inspector.

Uses FFprobe to analyze input gaming clips: duration, resolution, codec, etc.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from rich.console import Console

from src.models.schemas import VideoInfo

console = Console()

SUPPORTED_EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v", ".wmv"}


def inspect_video(path: str | Path) -> VideoInfo:
    """
    Run FFprobe on the given video file and return a structured VideoInfo.
    Raises RuntimeError if the file cannot be decoded.
    """
    path = Path(path).resolve()
    filename = path.name

    if not path.exists():
        return VideoInfo(
            path=str(path), filename=filename,
            duration=0, width=0, height=0, fps=0, codec="",
            has_audio=False, file_size_mb=0, is_valid=False,
            error=f"File not found: {path}",
        )

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return VideoInfo(
            path=str(path), filename=filename,
            duration=0, width=0, height=0, fps=0, codec="",
            has_audio=False, file_size_mb=0, is_valid=False,
            error=f"Unsupported format: {path.suffix}",
        )

    file_size_mb = path.stat().st_size / (1024 * 1024)

    try:
        probe = _run_ffprobe(path)
    except Exception as e:
        return VideoInfo(
            path=str(path), filename=filename,
            duration=0, width=0, height=0, fps=0, codec="",
            has_audio=False, file_size_mb=file_size_mb,
            is_valid=False, error=str(e),
        )

    # Find video stream
    video_stream = None
    audio_stream = None
    for stream in probe.get("streams", []):
        if stream.get("codec_type") == "video" and video_stream is None:
            video_stream = stream
        elif stream.get("codec_type") == "audio" and audio_stream is None:
            audio_stream = stream

    if video_stream is None:
        return VideoInfo(
            path=str(path), filename=filename,
            duration=0, width=0, height=0, fps=0, codec="",
            has_audio=False, file_size_mb=file_size_mb,
            is_valid=False, error="No video stream found",
        )

    # Parse fields
    width = int(video_stream.get("width", 0))
    height = int(video_stream.get("height", 0))
    codec = video_stream.get("codec_name", "unknown")

    # Duration: try format-level first, then stream-level
    duration = 0.0
    fmt = probe.get("format", {})
    if "duration" in fmt:
        duration = float(fmt["duration"])
    elif "duration" in video_stream:
        duration = float(video_stream["duration"])

    # FPS
    fps = _parse_fps(video_stream.get("r_frame_rate", "30/1"))

    # Orientation
    if width > height:
        orientation = "landscape"
    elif width < height:
        orientation = "portrait"
    else:
        orientation = "square"

    has_audio = audio_stream is not None
    audio_codec = audio_stream.get("codec_name") if audio_stream else None

    info = VideoInfo(
        path=str(path),
        filename=filename,
        duration=round(duration, 2),
        width=width,
        height=height,
        fps=round(fps, 2),
        codec=codec,
        has_audio=has_audio,
        audio_codec=audio_codec,
        file_size_mb=round(file_size_mb, 2),
        orientation=orientation,
        is_valid=True,
    )

    console.print(f"[green]✓[/green] Inspected [bold]{filename}[/bold]: "
                  f"{width}×{height}, {duration:.1f}s, {fps:.0f}fps, {codec}")
    return info


def _run_ffprobe(path: Path) -> dict:
    """Execute FFprobe and return parsed JSON output."""
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        str(path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        raise RuntimeError(f"FFprobe failed: {result.stderr.strip()}")
    return json.loads(result.stdout)


def _parse_fps(rate_str: str) -> float:
    """Parse FFprobe frame rate string like '30/1' or '29.97'."""
    try:
        if "/" in rate_str:
            num, den = rate_str.split("/")
            return float(num) / float(den)
        return float(rate_str)
    except (ValueError, ZeroDivisionError):
        return 30.0


def estimate_short_duration(
    video_info: VideoInfo,
    target_min: int = 35,
    target_max: int = 55,
) -> float:
    """Estimate a suitable Short duration based on the source clip."""
    if video_info.duration <= 0:
        return float(target_min)
    # If source is shorter than min, we'll loop — target the minimum
    if video_info.duration < target_min:
        return float(target_min)
    # If within range, use source duration
    if video_info.duration <= target_max:
        return video_info.duration
    # If longer, cap at target max
    return float(target_max)
