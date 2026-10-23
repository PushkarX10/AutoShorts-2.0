"""
AutoShorts 2.0 — Synthetic Gaming Clip Generator.

Generates a procedural vertical (1080x1920) 30fps gaming action footage clip
with dynamic motion, scrolling neon grid, floating runner blocks, and speed lines.
Allows immediate local testing of the complete pipeline without requiring external downloads.
"""
from __future__ import annotations

import math
import subprocess
from pathlib import Path

import cv2
import numpy as np
from rich.console import Console

from src.config.settings import get_project_root

console = Console(legacy_windows=False)


def generate_sample_gaming_clip(
    output_path: Path | None = None,
    duration_sec: float = 40.0,
    fps: int = 30,
) -> Path:
    """
    Generate an engaging vertical 9:16 neon parkour / runner demo clip.
    """
    if output_path is None:
        root = get_project_root()
        output_path = root / "input" / "sample_parkour.mp4"
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    width = 1080
    height = 1920
    total_frames = int(duration_sec * fps)

    console.print(f"[cyan]🎮[/cyan] Generating synthetic parkour gameplay clip: {duration_sec}s @ {fps}fps…")

    # Use FFmpeg pipe for fast generation
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-pix_fmt", "bgr24",
        "-s", f"{width}x{height}",
        "-r", str(fps),
        "-i", "pipe:0",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "22",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(output_path),
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if proc.stdin is None:
        raise RuntimeError("Failed to start FFmpeg for sample generation")

    # Generate animated gaming frames:
    # 3D perspective grid scrolling forward + parkour runner jumping + neon platforms + speed particles
    horizon_y = int(height * 0.42)
    vanishing_x = width // 2

    # Starfield / speed lines particles
    num_particles = 90
    rng = np.random.default_rng(42)
    p_x = rng.uniform(0, width, num_particles)
    p_y = rng.uniform(0, height, num_particles)
    p_speed = rng.uniform(4.0, 14.0, num_particles)
    p_len = rng.uniform(10.0, 35.0, num_particles)

    # Runner position
    runner_x = width // 2
    runner_y = int(height * 0.78)

    batch_size = 30
    for frame_idx in range(total_frames):
        t = frame_idx / fps

        # Background gradient: dark cyberpunk indigo to deep purple
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        # Sky gradient (top to horizon)
        y_indices = np.arange(horizon_y)[:, None]
        sky_r = (18 + 12 * (y_indices / horizon_y)).astype(np.uint8)
        sky_g = (12 + 10 * (y_indices / horizon_y)).astype(np.uint8)
        sky_b = (36 + 25 * (y_indices / horizon_y)).astype(np.uint8)
        frame[:horizon_y, :] = np.dstack([sky_b, sky_g, sky_r])

        # Ground gradient (horizon to bottom)
        ground_h = height - horizon_y
        y_ground = np.arange(ground_h)[:, None]
        g_r = (24 + 18 * (y_ground / ground_h)).astype(np.uint8)
        g_g = (14 + 12 * (y_ground / ground_h)).astype(np.uint8)
        g_b = (42 + 28 * (y_ground / ground_h)).astype(np.uint8)
        frame[horizon_y:, :] = np.dstack([g_b, g_g, g_r])

        # Perspective Grid Lines on ground
        # Moving horizontal grid lines (scrolling down towards viewer)
        grid_speed = 3.5
        scroll = (t * grid_speed) % 1.0
        for i in range(14):
            frac = (i + scroll) / 14.0
            frac_curved = frac ** 2.2  # Perspective compression near horizon
            gy = int(horizon_y + frac_curved * ground_h)
            if horizon_y <= gy < height:
                alpha = int(frac * 160)
                cv2.line(frame, (0, gy), (width, gy), (220, 80, 160), 2)

        # Perspective Radial lines converging to vanishing point
        for angle in np.linspace(-1.3, 1.3, 15):
            bx = int(vanishing_x + math.tan(angle) * (height - horizon_y) * 1.2)
            cv2.line(frame, (vanishing_x, horizon_y), (bx, height), (180, 50, 130), 2)

        # Floating Neon Parkour Platforms
        for plat_idx in range(4):
            plat_t = (t * 0.8 + plat_idx * 0.25) % 1.0
            depth = plat_t ** 2.0
            plat_y = int(horizon_y + depth * (ground_h * 0.85))
            plat_scale = 0.3 + depth * 1.2
            plat_w = int(220 * plat_scale)
            plat_h = int(32 * plat_scale)
            # Sway platform x
            plat_x = int(vanishing_x + math.sin(t * 1.5 + plat_idx) * 260 * depth - plat_w // 2)

            if horizon_y < plat_y < height:
                # Glowing neon box
                glow_color = (255, 120, 20) if plat_idx % 2 == 0 else (20, 240, 255)
                cv2.rectangle(frame, (plat_x, plat_y), (plat_x + plat_w, plat_y + plat_h), glow_color, -1)
                cv2.rectangle(frame, (plat_x - 3, plat_y - 3), (plat_x + plat_w + 3, plat_y + plat_h + 3), (255, 255, 255), 2)

        # Parkour Runner Character (smooth jumping & running motion)
        jump_phase = (t * 3.2) % (2 * np.pi)
        jump_offset = int(abs(math.sin(jump_phase)) * 70)
        lean = math.sin(t * 6.0) * 8

        cur_runner_y = runner_y - jump_offset
        cur_runner_x = int(runner_x + math.sin(t * 1.8) * 120)

        # Runner shadow on ground
        cv2.ellipse(frame, (cur_runner_x, runner_y + 40), (45, 16), 0, 0, 360, (15, 10, 25), -1)

        # Runner body: glowing cyber cube / athlete silhouette
        runner_size = 50
        rx1 = cur_runner_x - runner_size // 2
        ry1 = cur_runner_y - runner_size // 2
        cv2.rectangle(frame, (rx1, ry1), (rx1 + runner_size, ry1 + runner_size), (0, 255, 200), -1)
        # Inner glow
        cv2.rectangle(frame, (rx1 + 6, ry1 + 6), (rx1 + runner_size - 6, ry1 + runner_size - 6), (255, 255, 255), -1)

        # Speed particles / sparks
        p_y += p_speed
        mask = p_y >= height
        p_y[mask] = rng.uniform(0, 50, np.sum(mask))
        p_x[mask] = rng.uniform(0, width, np.sum(mask))

        for px, py, plen in zip(p_x, p_y, p_len):
            cv2.line(frame, (int(px), int(py)), (int(px), int(py + plen)), (255, 220, 140), 2)

        # HUD Overlay elements (stylish gaming vibes)
        cv2.putText(frame, "PARKOUR RUN // AUTO-PLAY", (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (120, 240, 255), 2)
        score = int(t * 1250)
        cv2.putText(frame, f"SCORE: {score:06d}", (width - 340, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 200, 50), 2)
        cv2.line(frame, (50, 110), (width - 50, 110), (80, 80, 120), 2)

        # Write frame bytes to FFmpeg stdin
        proc.stdin.write(frame.tobytes())

    proc.stdin.close()
    proc.wait()

    console.print(f"[green]✓[/green] Synthetic gaming clip created: {output_path.name} ({duration_sec}s)")
    return output_path
