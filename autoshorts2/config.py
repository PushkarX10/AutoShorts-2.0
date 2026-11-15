"""AutoShorts 2.0 Configuration
Global paths, constants, colors, and environment loader.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load workspace .env
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

PROJECTS_DIR = ROOT_DIR / "projects"
OUTPUT_DIR = ROOT_DIR / "output"
RENDERER_DIR = ROOT_DIR / "renderer"
ASSETS_DIR = Path(__file__).resolve().parent / "assets"
SFX_DIR = ASSETS_DIR / "sfx"
BGM_DIR = ASSETS_DIR / "bgm"

# Ensure directories exist
PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Visual Identity Palette (Strictly Enforced)
COLOR_DEEP_BLACK = "#0D0E12"
COLOR_CHARCOAL = "#16171D"
COLOR_WARM_SHADOW = "#1C1818"
COLOR_NEON_PINK = "#FF2A85"
COLOR_MAGENTA_GLOW = "rgba(255, 42, 133, 0.4)"
COLOR_BEIGE_BG = "#F4EFEB"
COLOR_BEIGE_CARD = "#EAE3DA"
COLOR_INK_BLACK = "#111114"
COLOR_WHITE = "#FFFFFF"

# Voice & Production defaults
DEFAULT_VOICE = os.getenv("AUTOSHORTS_VOICE", "en-US-ChristopherNeural")
FPS = 30
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
ASPECT_RATIO = "9:16"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
