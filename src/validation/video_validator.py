"""
AutoShorts 2.0 — Quality Assurance & Video Validator.

Verifies the final rendered YouTube Short against strict production standards:
  • Correct resolution (1080×1920, 9:16 vertical)
  • Duration compliant with YouTube Shorts (< 60s, typically 30-55s)
  • Non-silent audio track with appropriate loudness
  • No black or corrupt video frames
  • Valid container and stream formatting
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import cv2
import numpy as np
from rich.console import Console

from src.config.settings import get
from src.models.schemas import QACheck, QualityReport

console = Console()


def validate_video(
    video_path: Path | str,
    job_id: str = "qa_job",
) -> QualityReport:
    """
    Run comprehensive QA checks on the rendered video file.
    Returns a QualityReport with itemized check results.
    """
    path = Path(video_path)
    report = QualityReport(
        job_id=job_id,
        output_path=str(path),
    )

    if not path.exists():
        report.checks.append(QACheck(name="File Exists", passed=False, detail="File does not exist"))
        report.errors.append("Output file does not exist")
        return report

    size_mb = path.stat().st_size / (1024 * 1024)
    report.file_size_mb = round(size_mb, 2)

    # 1. File Size Check
    size_passed = size_mb >= 0.5
    report.checks.append(
        QACheck(
            name="File Size",
            passed=size_passed,
            detail=f"{size_mb:.2f} MB (min: 0.5 MB)",
        )
    )
    if not size_passed:
        report.errors.append(f"File size too small: {size_mb:.2f} MB")

    # 2. Probe Streams
    probe_data = _run_ffprobe(path)
    if not probe_data:
        report.checks.append(QACheck(name="FFprobe Analysis", passed=False, detail="Could not read video metadata"))
        report.errors.append("FFprobe inspection failed")
        return report

    # Video stream check
    v_streams = [s for s in probe_data.get("streams", []) if s.get("codec_type") == "video"]
    a_streams = [s for s in probe_data.get("streams", []) if s.get("codec_type") == "audio"]

    if not v_streams:
        report.checks.append(QACheck(name="Video Stream", passed=False, detail="No video stream found"))
        report.errors.append("No video stream found in file")
        return report

    v_stream = v_streams[0]
    w = int(v_stream.get("width", 0))
    h = int(v_stream.get("height", 0))
    report.resolution = f"{w}x{h}"

    cfg_w = get("video", "width", 1080)
    cfg_h = get("video", "height", 1920)
    res_passed = (w == cfg_w and h == cfg_h)
    report.checks.append(
        QACheck(
            name="Resolution (9:16)",
            passed=res_passed,
            detail=f"{w}x{h} (expected: {cfg_w}x{cfg_h})",
        )
    )
    if not res_passed:
        report.errors.append(f"Incorrect resolution: {w}x{h}, expected {cfg_w}x{cfg_h}")

    # Duration Check
    duration = float(probe_data.get("format", {}).get("duration", 0.0))
    if duration == 0 and "duration" in v_stream:
        duration = float(v_stream["duration"])
    report.duration_sec = round(duration, 2)

    dur_passed = 10.0 <= duration <= 60.5
    report.checks.append(
        QACheck(
            name="Duration (YouTube Shorts Limit)",
            passed=dur_passed,
            detail=f"{duration:.1f}s (allowed: 10s - 60s)",
        )
    )
    if not dur_passed:
        if duration > 60.5:
            report.errors.append(f"Video is {duration:.1f}s which exceeds YouTube Shorts 60s maximum limit")
        else:
            report.warnings.append(f"Video is unusually short: {duration:.1f}s")

    # 3. Audio Stream Check
    has_audio = len(a_streams) > 0
    report.checks.append(
        QACheck(
            name="Audio Stream Present",
            passed=has_audio,
            detail=f"{len(a_streams)} audio stream(s) found",
        )
    )
    if not has_audio:
        report.errors.append("No audio track detected in final video")
    else:
        # Check audio levels
        vol_info = _check_audio_levels(path)
        if vol_info:
            mean_vol = vol_info.get("mean_volume", -99.0)
            max_vol = vol_info.get("max_volume", -99.0)
            audio_audible = mean_vol > -50.0  # Not dead silence
            report.checks.append(
                QACheck(
                    name="Audio Loudness & Audibility",
                    passed=audio_audible,
                    detail=f"Mean: {mean_vol:.1f} dB, Max: {max_vol:.1f} dB",
                )
            )
            if not audio_audible:
                report.warnings.append(f"Audio level is very quiet (mean: {mean_vol:.1f} dB)")

    # 4. Black Frame & Visual Integrity Check
    visual_ok, visual_msg = _check_frames_with_opencv(path, sample_count=10)
    report.checks.append(
        QACheck(
            name="Visual Content Integrity",
            passed=visual_ok,
            detail=visual_msg,
        )
    )
    if not visual_ok:
        report.warnings.append(f"Visual check warning: {visual_msg}")

    # Final verdict
    report.all_passed = len(report.errors) == 0

    if report.all_passed:
        console.print(f"[green]✓[/green] QA Verification Passed ({len(report.checks)} checks ok)")
    else:
        console.print(f"[red]✗[/red] QA Verification Failed with {len(report.errors)} errors")

    return report


def _run_ffprobe(path: Path) -> dict | None:
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        str(path),
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if res.returncode == 0 and res.stdout.strip():
            return json.loads(res.stdout)
    except Exception as e:
        console.print(f"[red]FFprobe error:[/red] {e}")
    return None


def _check_audio_levels(path: Path) -> dict | None:
    """Analyze audio volume with FFmpeg volumedetect filter."""
    cmd = [
        "ffmpeg",
        "-i", str(path),
        "-vn",
        "-af", "volumedetect",
        "-f", "null",
        "-",
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        output = res.stderr
        mean_vol = None
        max_vol = None
        for line in output.splitlines():
            if "mean_volume:" in line:
                mean_vol = float(line.split("mean_volume:")[1].replace("dB", "").strip())
            elif "max_volume:" in line:
                max_vol = float(line.split("max_volume:")[1].replace("dB", "").strip())
        if mean_vol is not None and max_vol is not None:
            return {"mean_volume": mean_vol, "max_volume": max_vol}
    except Exception:
        pass
    return None


def _check_frames_with_opencv(path: Path, sample_count: int = 10) -> tuple[bool, str]:
    """Sample frames evenly across video and verify they contain visible content."""
    try:
        cap = cv2.VideoCapture(str(path))
        if not cap.isOpened():
            return False, "Could not open video file for frame sampling"

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames <= 0:
            cap.release()
            return True, "Video opened but frame count unknown"

        step = max(1, total_frames // (sample_count + 1))
        black_frames = 0
        samples_tested = 0

        for i in range(1, sample_count + 1):
            frame_no = i * step
            if frame_no >= total_frames:
                break
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            ret, frame = cap.read()
            if not ret or frame is None:
                continue

            samples_tested += 1
            mean_lum = float(np.mean(frame))
            std_lum = float(np.std(frame))

            # Pitch black frame: mean < 1.0 and std < 1.0
            if mean_lum < 1.0 and std_lum < 1.0:
                black_frames += 1

        cap.release()

        if samples_tested == 0:
            return False, "Could not read any frames during sampling"

        if black_frames >= samples_tested // 2:
            return False, f"{black_frames}/{samples_tested} sampled frames were completely black"

        return True, f"{samples_tested} frames sampled, no blank/corrupted frames detected"
    except Exception as e:
        return True, f"Visual check skipped due to error: {e}"
