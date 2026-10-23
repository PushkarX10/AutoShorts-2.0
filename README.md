# AutoShorts 2.0
### Autonomous Multi-Agent Content Engine

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Ollama](https://img.shields.io/badge/Ollama-llama3.1-black.svg?style=flat&logo=ollama&logoColor=white)](https://ollama.ai)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-5.0+-007808.svg?style=flat&logo=ffmpeg&logoColor=white)](https://ffmpeg.org)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Table of Contents
- **[01 — What is AutoShorts 2.0 ?](#01--what-is-autoshorts-20-)**
- **[02 — Why it exists](#02--why-it-exists)**
- **[03 — Architecture](#03--architecture)**
- **[04 — Agent System](#04--agent-system)**
- **[05 — How it works](#05--how-it-works)**
- **[06 — Example Run](#06--example-run)**
- **[07 — Evaluation](#07--evaluation)**
- **[08 — Security & Auditing](#08--security--auditing)**
- **[09 — Tech Stack](#09--tech-stack)**
- **[10 — Installation](#10--installation)**
- **[11 — Roadmap](#11--roadmap)**
- **[12 — Contributing](#12--contributing)**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 01 — What is AutoShorts 2.0 ?

**AutoShorts 2.0** is an autonomous, locally orchestrated multi-agent content factory engineered to convert raw horizontal gaming parkour clips into viral, high-retention vertical **YouTube Shorts**, **TikToks**, and **Instagram Reels**.

Given only a **single input file** — a gaming gameplay clip (e.g., Minecraft parkour, Subway Surfers, racing loops) — AutoShorts 2.0 autonomously executes the entire creative and production lifecycle:
- Brainstorms comedic premises and formats structured, multi-character text messaging conversations.
- Casts distinctive voice personas and synthesizes synchronized voice acting with pacing and pauses.
- Renders 60+ FPS animated chat overlays featuring authentic message bubbles, avatars, pop-in micro-animations, and bouncing typing indicators.
- Crops or fills background gameplay into vertical **9:16 (1080×1920)** resolution with seamless crossfade looping.
- Master-mixes dialogue with procedural sound effects (pops, clicks, whooshes, punchline stingers) and background music normalized to broadcast loudness standards (-14 LUFS).
- Generates high-resolution thumbnail stills, synchronized `.srt` subtitles, automated quality assurance reports, and complete YouTube SEO distribution packages.

---

## 02 — Why it exists

Short-form content dominates social discovery, but producing viral text-story Shorts manually involves high friction:
1. **Time-Intensive Workflows**: A creator typically spends 2 to 4 hours per 45-second Short drafting scripts, recording or generating voice clips, keyframing graphic assets in Premiere Pro or After Effects, aligning subtitles, and formatting SEO descriptions.
2. **Expensive Cloud Dependencies**: Many commercial SaaS video creators charge recurring monthly subscriptions or high per-minute API costs for proprietary cloud rendering and third-party LLM inference.
3. **Privacy Concerns**: Uploading proprietary clips, scripts, and production material to cloud services exposes private data and dependencies on external network availability.

**AutoShorts 2.0** solves this by delivering an **end-to-end autonomous pipeline that runs 100% locally on your machine**. With zero API costs, full data privacy, and multi-agent coordination, creators can generate high-quality video bundles in seconds.

---

## 03 — Architecture

AutoShorts 2.0 is built on a modular, decoupled agentic architecture. Each stage of the pipeline functions as an autonomous worker with discrete input/output contracts, coordinated by a central orchestrator.

```mermaid
flowchart TD
    A[Input: Raw Gameplay Clip] --> B[Video Ingestion & Probe Agent]
    
    subgraph Creative & Audio Engine
        C[Ollama LLM Agent] -->|Structured JSON Script| D[Dialogue Quality Agent]
        D -->|Validated Conversation| E[Voice Casting & TTS Agent]
        E -->|Individual Audio Clips| F[Timeline & Sync Agent]
        F -->|Precise Timestamps| G[Audio Mastering & SFX Agent]
    end
    
    subgraph Visual Engine
        B -->|Resolution & FPS Data| H[9:16 Background Processor]
        F -->|Message Timing Coordinates| I[Pillow Chat Renderer]
        H -->|Vertical Looped Background| J[Video Compositor]
        I -->|Transparent Animated Overlay| J
    end
    
    G -->|Normalized Master Audio -14 LUFS| J
    
    subgraph Quality & Distribution
        J --> K[QA & Validation Agent]
        K -->|Passed Verification| L[SEO & Metadata Agent]
        L --> M[Final Output Bundle: MP4 + SRT + Thumb + SEO]
    end
```

---

## 04 — Agent System

AutoShorts 2.0 distributes specialized responsibilities across distinct sub-agents:

| Agent | Module | Primary Responsibility |
|---|---|---|
| **Creative Scriptwriter** | `src/llm/conversation_generator.py` | Generates comedic chat dialogues with character dynamics, humor themes, and punchlines using local Ollama (`llama3.1`). |
| **Dialogue Gatekeeper** | `src/llm/quality_checker.py` | Enforces message length constraints, character count limits, emotional arc progression, and JSON schema conformity. |
| **Voice Director** | `src/tts/` | Assigns matching voice profiles (Clara, Aria, Sara, Steffan, Brian, Eric) and generates natural speech cadence using Edge-TTS. |
| **Audio Mastering Engineer** | `src/audio/` | Mixes dialogue stems, applies procedural typing clicks, bubble pops, whooshes, stingers, background music, and normalizes to -14 LUFS. |
| **Visual Compositor** | `src/chat/` & `src/video/` | Renders high-performance PIL chat frames (>130 FPS), typing indicators, avatar circles, and crops/blurs background footage to 9:16. |
| **Quality Auditor** | `src/validation/` | Performs automated QA checks on resolution, frame drops, audio levels, black frames, and video duration compliance. |
| **Distribution & SEO Agent** | `src/llm/metadata_generator.py` | Generates viral titles, YouTube descriptions, hashtags, pinned comments, and upload cheat sheets. |

---

## 05 — How it works

The execution pipeline operates in five distinct phases:

1. **Ingestion & Analysis**:
   - The probe agent inspects the input video file using `ffprobe`, extracting duration, resolution, framerate, and codec specifications.
2. **Script Generation & Auditing**:
   - The LLM agent receives the selected comedic theme (e.g., `wholesome`, `sarcastic`, `chaotic`, `awkward`, `dark`) and generates a structured JSON script featuring characters, speech tags, delivery speeds, and emotional states.
   - The quality checker validates message count (10–18 messages) and punchline timing before approving the script.
3. **Voice Synthesis & Timeline Construction**:
   - Each message is synthesized into an audio stem using Edge-TTS.
   - The timeline agent measures exact audio durations and inserts dynamic pauses (natural inter-message pauses, pre-punchline suspense pauses, and post-punchline resolution pauses).
4. **Visual Rendering & Compositing**:
   - The chat overlay renderer generates transparent animation frames with Pillow at native 30/60 FPS, calculating pop-in bubble scales and scrolling offsets.
   - The background video processor center-crops horizontal video to 1080×1920 or creates a blurred background fill, applying seamless crossfading if looping is required.
   - FFmpeg composites the background video, transparent chat stream, and master audio track in a single hardware-accelerated pass.
5. **QA Verification & Packaging**:
   - The output bundle is audited against quality thresholds, a thumbnail is captured at the peak comedic moment, `.srt` subtitles are written, and YouTube Studio metadata is formatted.

---

## 06 — Example Run

### Command-Line Execution
Generate a complete YouTube Short from a raw gameplay clip:

```bash
# 1. Verify your local environment
python main.py check-env

# 2. Run basic automated generation
python main.py generate input/minecraft_parkour.mp4

# 3. Specify a distinct comedy style and custom theme
python main.py generate input/minecraft_parkour.mp4 --style chaotic --theme "accidental text to landlord"
```

### Web Studio Dashboard
Launch the interactive web studio to preview chats, configure styles, and track real-time rendering:

```bash
python main.py dashboard --port 8899
```
Navigate to **http://localhost:8899** in your browser.

### Generated Output Bundle
Each job produces a self-contained production bundle in `output/<timestamp>_<job_id>_<slug>/`:

```
output/20261023_193000_a1b2c3d4_landlord_chaos/
├── landlord_chaos.mp4             # Final vertical 1080x1920 YouTube Short
├── landlord_chaos.srt             # Synchronized subtitles
├── landlord_chaos_thumbnail.jpg   # High-resolution thumbnail
├── conversation.json              # Full conversation transcript & character metadata
├── metadata.json                  # YouTube SEO metadata (title, description, tags)
├── youtube_upload_info.txt        # Copy-paste guide for YouTube Studio
└── quality_report.json            # Automated QA validation report
```

---

## 07 — Evaluation

AutoShorts 2.0 is benchmarked for speed, visual fidelity, and audio clarity on standard consumer hardware:

| Metric | Target | AutoShorts 2.0 Benchmark |
|---|---|---|
| **Chat Render Speed** | > 60 FPS | **130 – 180 FPS** (Pillow C-extension accelerated) |
| **End-to-End Generation Time** | < 60s (for 45s video) | **~35 – 45 seconds** (using local Ollama + FFmpeg) |
| **Audio Loudness Standard** | -14 LUFS ± 1.0 | **-14.0 LUFS** (ITU-R BS.1770-4 normalized) |
| **Frame Integrity** | 0 black frames | **100% verified** by automated QA agent |
| **Resolution & Aspect Ratio** | 1080×1920 (9:16) | **Strict 9:16 compliance** (verified via ffprobe) |

---

## 08 — Security & Auditing

- **100% Local Inference**: Runs entirely on your workstation via Ollama (`llama3.1`) and local FFmpeg. No private user data, scripts, or media files are uploaded to third-party cloud servers.
- **Content Safety Filtering**: Includes automatic pre-generation guardrails against restricted categories (`politics`, `religion`, `violence`, `real_people`).
- **Deterministic Quality Auditing**: Every render job outputs a `quality_report.json` logging audio loudness, resolution metrics, render durations, and validation checks for complete traceability.

---

## 09 — Tech Stack

- **Core & CLI**: Python 3.10+, Click, Rich, Pydantic v2, PyYAML, python-dotenv
- **AI & Language Models**: Ollama (`llama3.1:latest`), httpx
- **Voice Synthesis**: Microsoft Edge-TTS (`edge-tts`)
- **Video & Graphics Engine**: FFmpeg, OpenCV, Pillow (PIL), NumPy
- **Audio Processing**: PyLoudNorm, Wave, Procedural Sine/Noise Synthesizers
- **Web Studio Dashboard**: FastAPI, Uvicorn, aiofiles, Vanilla CSS/HTML5, Server-Sent Events (SSE)

---

## 10 — Installation

### Prerequisites
1. **Python**: 3.10 or higher
2. **FFmpeg**: Installed and accessible in your system `PATH` ([Download FFmpeg](https://ffmpeg.org/download.html))
3. **Ollama**: Installed and running locally ([Download Ollama](https://ollama.ai))

### Setup Steps

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/AutoShorts2.0.git
cd AutoShorts2.0

# 2. Create and activate a virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# 3. Install required Python packages
pip install -r requirements.txt

# 4. Pull the recommended local LLM model
ollama pull llama3.1

# 5. Verify your installation
python main.py check-env
```

---

## 11 — Roadmap

- [ ] **Direct Social Publishing**: Automated one-click uploads via YouTube Data API v3 and TikTok Content Posting API.
- [ ] **Dynamic Avatar Reactions**: Adaptive character avatar expressions switching between happy, shocked, crying, and angry states based on message sentiment.
- [ ] **Karaoke-Style Subtitle Overlays**: Animated word-by-word bouncing captions with custom font stylings.
- [ ] **Multi-Lingual Dubbing**: Automatic cross-lingual script translation and multi-lingual voice synthesis (Spanish, French, German, Japanese).
- [ ] **AI Smart-Crop Gameplay Tracking**: Dynamic pan-and-scan camera focusing on the most action-heavy gameplay coordinates.

---

## 12 — Contributing

Contributions, feature requests, and bug reports are welcome!

1. Fork the Project repository.
2. Create your Feature Branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your Changes:
   ```bash
   git commit -m "Add amazing feature"
   ```
4. Run the Test Suite:
   ```bash
   python -m unittest discover -s tests -v
   ```
5. Push to the Branch:
   ```bash
   git push origin feature/amazing-feature
   ```
6. Open a Pull Request.

---

## 📜 License
Distributed under the **MIT License**. See `LICENSE` for more information.
