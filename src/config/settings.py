"""
AutoShorts 2.0 — Settings loader.

Reads config.yaml and merges with environment variable overrides.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

import yaml
from rich.console import Console

if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

console = Console(legacy_windows=False)

_CONFIG: dict[str, Any] | None = None
_PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent


def get_project_root() -> Path:
    """Return the absolute project root directory."""
    return _PROJECT_ROOT


def load_config(config_path: str | Path | None = None) -> dict[str, Any]:
    """Load and cache configuration from YAML, with env-var overrides."""
    global _CONFIG
    if _CONFIG is not None:
        return _CONFIG

    if config_path is None:
        config_path = _PROJECT_ROOT / "config.yaml"
    else:
        config_path = Path(config_path)

    if not config_path.exists():
        console.print(f"[yellow]⚠ Config file not found at {config_path}, using defaults[/yellow]")
        _CONFIG = _default_config()
        return _CONFIG

    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

    # Apply environment variable overrides
    _apply_env_overrides(cfg)

    # Ensure directories exist
    for key in ("output_dir", "input_dir", "temp_dir"):
        dir_path = _PROJECT_ROOT / cfg.get("project", {}).get(key, key.replace("_dir", ""))
        dir_path.mkdir(parents=True, exist_ok=True)

    _CONFIG = cfg
    return _CONFIG


def reload_config(config_path: str | Path | None = None) -> dict[str, Any]:
    """Force reload the configuration."""
    global _CONFIG
    _CONFIG = None
    return load_config(config_path)


def get(section: str, key: str | None = None, default: Any = None) -> Any:
    """Get a config value. Usage: get('video', 'width') or get('video')."""
    cfg = load_config()
    section_data = cfg.get(section, {})
    if key is None:
        return section_data if section_data else default
    return section_data.get(key, default)


def get_path(relative: str) -> Path:
    """Resolve a relative path against the project root."""
    return _PROJECT_ROOT / relative


def get_output_dir() -> Path:
    return get_path(get("project", "output_dir", "output"))


def get_input_dir() -> Path:
    return get_path(get("project", "input_dir", "input"))


def get_temp_dir() -> Path:
    return get_path(get("project", "temp_dir", "temp"))


def get_voice_config(voice_key: str) -> dict[str, str]:
    """Get TTS voice configuration by key name."""
    voices = get("tts", "voices", {})
    return voices.get(voice_key, {})


def get_available_voices() -> dict[str, dict]:
    """Return all configured TTS voices."""
    return get("tts", "voices", {})


def _apply_env_overrides(cfg: dict) -> None:
    """Override config values from environment variables."""
    env_map = {
        "OLLAMA_BASE_URL": ("llm", "base_url"),
        "OLLAMA_MODEL": ("llm", "model"),
        "INPUT_DIR": ("project", "input_dir"),
        "OUTPUT_DIR": ("project", "output_dir"),
        "TEMP_DIR": ("project", "temp_dir"),
        "LOG_LEVEL": ("project", "log_level"),
    }
    for env_key, (section, key) in env_map.items():
        val = os.environ.get(env_key)
        if val is not None:
            cfg.setdefault(section, {})[key] = val


def _default_config() -> dict[str, Any]:
    """Minimal default configuration when no config file exists."""
    return {
        "project": {
            "name": "AutoShorts 2.0",
            "output_dir": "output",
            "input_dir": "input",
            "temp_dir": "temp",
            "log_level": "INFO",
        },
        "video": {
            "width": 1080,
            "height": 1920,
            "fps": 30,
            "codec": "libx264",
            "audio_codec": "aac",
            "audio_bitrate": "192k",
            "pixel_format": "yuv420p",
            "crf": 18,
            "preset": "medium",
            "target_duration_min": 35,
            "target_duration_max": 55,
            "background_darken": 0.3,
        },
        "llm": {
            "provider": "ollama",
            "model": "llama3.1:latest",
            "base_url": "http://localhost:11434",
            "temperature": 0.85,
            "max_retries": 3,
            "timeout": 120,
        },
        "tts": {
            "engine": "edge-tts",
            "voices": {
                "female_01": {"id": "en-US-JennyNeural", "rate": "+0%", "pitch": "+0Hz", "volume": "+0%"},
                "male_01": {"id": "en-US-GuyNeural", "rate": "+0%", "pitch": "+0Hz", "volume": "+0%"},
            },
        },
        "chat": {
            "panel_width": 920,
            "panel_margin_top": 180,
            "panel_margin_x": 80,
            "panel_height_max": 1400,
            "panel_bg_color": [28, 28, 30, 235],
            "panel_corner_radius": 28,
            "header_height": 90,
            "bubble_incoming_color": [58, 58, 62],
            "bubble_outgoing_color": [0, 122, 255],
            "bubble_incoming_text_color": [255, 255, 255],
            "bubble_outgoing_text_color": [255, 255, 255],
            "text_font_size": 30,
            "header_font_size": 34,
            "bubble_corner_radius": 20,
            "bubble_max_width": 640,
            "bubble_spacing": 12,
            "bubble_margin_x": 16,
            "message_appear_duration_ms": 250,
            "scroll_pixels_per_frame": 8,
            "avatar_size": 52,
            "avatar_colors": [[0, 122, 255], [255, 59, 48], [52, 199, 89]],
        },
        "audio": {
            "voice_volume": 1.0,
            "music_volume": 0.12,
            "pause_between_messages_ms": 350,
            "pause_before_punchline_ms": 700,
            "pause_after_punchline_ms": 1200,
        },
        "comedy": {
            "humor_style": "wholesome",
            "num_characters": 2,
            "min_messages": 10,
            "max_messages": 18,
            "language": "en",
        },
        "subtitles": {"enabled": False},
        "qa": {"max_render_retries": 2},
    }
