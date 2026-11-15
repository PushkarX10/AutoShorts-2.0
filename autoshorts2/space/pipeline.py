"""WHAT IF? — Space & Planet Exploration Autonomous Production Pipeline
Generates broadcast-ready 1080x1920 30FPS educational space Shorts with 2D Stickman animation,
scientific infographics, HUD telemetry, and interactive community voting cliffhangers.
"""

import asyncio
import json
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

import edge_tts
from autoshorts2.space.planet_data import PLANET_DATABASE, PlanetFacts

ROOT_DIR = Path(__file__).resolve().parents[2]
PROJECTS_DIR = ROOT_DIR / "projects"
OUTPUT_DIR = ROOT_DIR / "output"
PUBLIC_DIR = ROOT_DIR / "renderer" / "public"
ASSETS_DIR = ROOT_DIR / "autoshorts2" / "assets"

DEFAULT_VOICE = "en-US-ChristopherNeural"
DEFAULT_RATE = "+9%"

EMPHASIS_KEYWORDS = {
    "mars", "moon", "jupiter", "titan", "venus", "space", "gravity", "atmosphere",
    "pressure", "vacuum", "radiation", "oxygen", "storm", "crashes", "lethal",
    "boils", "freezing", "seconds", "hours", "days", "supplies", "protocol",
    "option", "survive", "comment", "a", "b", "base", "alpha", "rover", "hazard"
}

class SpaceShortsPipeline:
    def __init__(self, voice: str = DEFAULT_VOICE, rate: str = DEFAULT_RATE):
        self.voice = voice
        self.rate = rate

    def generate_short(self, topic: str, planet_key: str = "mars") -> Dict[str, Any]:
        planet = PLANET_DATABASE.get(planet_key.lower(), PLANET_DATABASE["mars"])
        timestamp = int(time.time())
        project_id = f"whatif_{planet_key}_{timestamp}"
        project_dir = PROJECTS_DIR / project_id
        project_dir.mkdir(parents=True, exist_ok=True)
        PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        print("=" * 65)
        print("  WHAT IF? — SPACE & PLANET EXPLORATION ENGINE")
        print(f"  Topic: {topic}")
        print(f"  Target Planet: {planet.name} (Gravity: {planet.gravity_g}g | Pressure: {planet.surface_pressure_atm} ATM)")
        print("=" * 65)

        # 1. Plan 6-beat scientific storytelling script
        scenes_plan = self._build_script(topic, planet)

        # 2. Synthesize audio with edge_tts scene-by-scene
        print("\n[1/4] Synthesizing crisp documentary narration with Edge-TTS...")
        pdata = asyncio.run(self._synthesize_narration(scenes_plan, project_dir, topic, planet))

        # 3. Master audio soundtrack
        print("\n[2/4] Mastering ambient space tension score & restrained SFX...")
        soundtrack_path = self._master_audio(project_dir, pdata)

        # 4. Render Remotion 1080x1920 MP4
        output_mp4 = OUTPUT_DIR / f"{project_id}.mp4"
        print(f"\n[3/4] Rendering broadcast-ready vertical video to {output_mp4}...")
        self._render_video(project_dir, output_mp4)

        # 5. Extract metadata and community engagement package
        meta = self._generate_metadata(topic, planet, pdata)
        meta_file = project_dir / "youtube_metadata.json"
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        print("\n[4/4] COMPLETE! Deliverable ready:")
        print(f"  -> Video: {output_mp4}")
        print(f"  -> Metadata: {meta_file}")
        return {
            "project_id": project_id,
            "video_path": str(output_mp4),
            "project_dir": str(project_dir),
            "metadata": meta
        }

    def _build_script(self, topic: str, planet: PlanetFacts) -> List[Dict[str, Any]]:
        # Structured 6-beat narrative template grounded in physical facts
        return [
            {
                "scene_id": 1,
                "beat": "HOOK",
                "narration": f"What if you woke up on {planet.name} tomorrow... with only thirty days of supplies?",
                "environment": f"{planet.name.lower()}_surface",
                "camera": "slow_push_in",
                "character_action": f"Looking out across the alien horizon of {planet.name}",
                "character_pose": "walk_explore",
                "character_expression": "curious",
                "lighting": "subtle_cinematic",
                "music_state": "mystery",
                "transition": "cut",
                "hud_state": {
                    "label_1": planet.name,
                    "val_1": "SOL 01",
                    "label_2": planet.surface_temp_avg.split()[0],
                    "val_2": planet.surface_temp_avg.split()[0],
                    "label_3": f"{planet.gravity_g}g",
                    "val_3": f"{planet.gravity_g}g",
                    "progress_percent": 95,
                }
            },
            {
                "scene_id": 2,
                "beat": "GRAVITY_REVEAL",
                "narration": f"On {planet.name}, gravity is only {int(planet.gravity_g * 100)} percent of Earth. Every single jump sends you soaring in slow-motion flight.",
                "environment": f"{planet.name.lower()}_surface",
                "camera": "pan_up",
                "character_action": "Jumping across terrain in buoyant low gravity",
                "character_pose": "low_gravity_jump",
                "character_expression": "alert",
                "lighting": "subtle_cinematic",
                "music_state": "wonder",
                "transition": "cut",
                "hud_state": {
                    "label_1": planet.name,
                    "val_1": "SOL 05",
                    "label_2": planet.surface_temp_avg.split()[0],
                    "val_2": planet.surface_temp_avg.split()[0],
                    "label_3": f"{planet.gravity_g}g",
                    "val_3": f"{planet.gravity_g}g (LOW-G)",
                    "progress_percent": 91,
                }
            },
            {
                "scene_id": 3,
                "beat": "SCIENTIFIC_HAZARD",
                "narration": f"Outside your suit, {planet.name} is lethal. The air is {planet.atmosphere_composition.split(',')[0]}, and air pressure is near vacuum. Without this suit, your blood boils in fifteen seconds.",
                "environment": "planet_comparison",
                "camera": "slow_push_in",
                "character_action": "Scanning planetary telemetry comparison",
                "character_pose": "check_telemetry",
                "character_expression": "focused",
                "lighting": "infographic_neon",
                "music_state": "tension",
                "transition": "cut",
                "hud_state": {
                    "label_1": planet.name,
                    "val_1": "SOL 12",
                    "label_2": planet.surface_temp_avg.split()[0],
                    "val_2": planet.surface_temp_avg.split()[0],
                    "label_3": f"{planet.surface_pressure_atm} ATM",
                    "val_3": f"{planet.surface_pressure_atm} ATM",
                    "progress_percent": 82,
                }
            },
            {
                "scene_id": 4,
                "beat": "HABITAT_SANCTUARY",
                "narration": "Your only sanctuary is Base Alpha: a geodesic dome with hydroponic crops and solar oxygen scrubbers.",
                "environment": f"{planet.name.lower()}_habitat",
                "camera": "pan_left",
                "character_action": "Approaching pressurized habitat airlock",
                "character_pose": "enter_airlock",
                "character_expression": "relief",
                "lighting": "subtle_cinematic",
                "music_state": "relief",
                "transition": "cut",
                "hud_state": {
                    "label_1": "Base Alpha",
                    "val_1": "SOL 15",
                    "label_2": "+21°C",
                    "val_2": "+21°C",
                    "label_3": "1.0 ATM",
                    "val_3": "1.0 ATM",
                    "progress_percent": 88,
                }
            },
            {
                "scene_id": 5,
                "beat": "CRISIS_EVENT",
                "narration": "Sol eighteen. A violent dust storm blots out the Sun. Solar power crashes by eighty-five percent, and oxygen drops to twenty-two percent.",
                "environment": f"{planet.name.lower()}_dust_storm",
                "camera": "shake_subtle",
                "character_action": "Gasping in panic as suit life-support alarms flash red",
                "character_pose": "panic_o2",
                "character_expression": "shock",
                "lighting": "storm_red_alert",
                "music_state": "crisis",
                "transition": "cut",
                "hud_state": {
                    "label_1": "CRITICAL",
                    "val_1": "SOL 18",
                    "label_2": "-85°C",
                    "val_2": "-85°C",
                    "label_3": "100 KM/H",
                    "val_3": "100 KM/H",
                    "progress_percent": 22,
                }
            },
            {
                "scene_id": 6,
                "beat": "INTERACTIVE_CLIFFHANGER",
                "narration": "Two survival protocols remain: Option A: Brave the one hundred kilometer per hour storm to clear the panels. Or Option B: Shut off heaters and cryo-hibernate in the rover. What would you do? Comment A or B!",
                "environment": "space_cliffhanger",
                "camera": "slow_push_in",
                "character_action": "Presenting urgent survival decision to audience",
                "character_pose": "point_sky",
                "character_expression": "focused",
                "lighting": "high_contrast",
                "music_state": "decision",
                "transition": "cut",
                "hud_state": {
                    "label_1": "DECISION",
                    "val_1": "TIME CRITICAL",
                    "label_2": "O2: 19%",
                    "val_2": "O2: 19%",
                    "label_3": "00:03",
                    "val_3": "00:03",
                    "progress_percent": 19,
                }
            }
        ]

    async def _synthesize_narration(self, scenes: List[Dict[str, Any]], project_dir: Path, topic: str, planet: PlanetFacts) -> Dict[str, Any]:
        scenes_audio_dir = project_dir / "scene_audios"
        scenes_audio_dir.mkdir(parents=True, exist_ok=True)

        scene_files = []
        all_subtitle_words = []
        calculated_scenes = []
        running_time = 0.0

        for sc in scenes:
            scene_id = sc["scene_id"]
            text = sc["narration"]
            out_mp3 = scenes_audio_dir / f"scene_{scene_id}.mp3"

            communicate = edge_tts.Communicate(text, self.voice, rate=self.rate)
            audio_bytes = bytearray()
            sentence_boundaries = []

            async for chunk in communicate.stream():
                ctype = chunk.get("type")
                if ctype == "audio":
                    audio_bytes.extend(chunk["data"])
                elif ctype == "SentenceBoundary":
                    start_s = chunk["offset"] / 10_000_000.0
                    dur_s = chunk["duration"] / 10_000_000.0
                    sentence_boundaries.append({
                        "text": chunk["text"],
                        "start": round(start_s, 3),
                        "duration": round(dur_s, 3),
                        "end": round(start_s + dur_s, 3)
                    })

            with open(out_mp3, "wb") as f:
                f.write(audio_bytes)

            duration = self._get_audio_dur(out_mp3)
            scene_files.append(out_mp3)

            # Subtitle mapping
            scene_words = []
            if sentence_boundaries:
                for sb in sentence_boundaries:
                    s_words = sb["text"].strip().split()
                    if not s_words:
                        continue
                    s_start = sb["start"]
                    s_end = sb["end"]
                    s_dur = max(0.2, s_end - s_start)
                    total_chars = sum(max(1, len(w)) for w in s_words)
                    curr_w_start = s_start
                    for w in s_words:
                        w_fraction = max(1, len(w)) / total_chars
                        w_dur = s_dur * w_fraction
                        w_end = min(s_end, curr_w_start + w_dur)
                        clean = w.lower().strip(".,!?:;$\"'")
                        is_emp = clean in EMPHASIS_KEYWORDS or any(c.isdigit() for c in clean)
                        
                        scene_words.append({
                            "word": w,
                            "start": round(running_time + curr_w_start, 3),
                            "end": round(running_time + w_end, 3),
                            "is_emphasized": is_emp
                        })
                        curr_w_start = w_end
            else:
                words = text.split()
                w_dur = duration / max(1, len(words))
                for i, w in enumerate(words):
                    clean = w.lower().strip(".,!?:;$\"'")
                    is_emp = clean in EMPHASIS_KEYWORDS or any(c.isdigit() for c in clean)
                    scene_words.append({
                        "word": w,
                        "start": round(running_time + i * w_dur, 3),
                        "end": round(running_time + (i + 1) * w_dur, 3),
                        "is_emphasized": is_emp
                    })

            all_subtitle_words.extend(scene_words)

            scene_pad = 0.15 if scene_id < 6 else 0.50
            scene_total_dur = round(duration + scene_pad, 2)
            scene_end = round(running_time + scene_total_dur, 2)

            sc_data = dict(sc)
            sc_data["start_time"] = round(running_time, 2)
            sc_data["end_time"] = scene_end
            sc_data["duration"] = scene_total_dur
            calculated_scenes.append(sc_data)
            running_time = scene_end

        total_duration = calculated_scenes[-1]["end_time"]

        concat_list = scenes_audio_dir / "concat_list.txt"
        with open(concat_list, "w", encoding="utf-8") as f:
            for sf in scene_files:
                escaped = str(sf.resolve()).replace("\\", "/")
                f.write(f"file '{escaped}'\n")

        raw_voice_out = project_dir / "voice_raw.mp3"
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_list),
            "-c", "copy",
            str(raw_voice_out)
        ], check=True)

        project_data = {
            "project_id": project_dir.name,
            "topic": topic,
            "total_duration": total_duration,
            "character_bible": {
                "character_id": "astronaut_stickman_01",
                "name": "Astronaut Stickman",
                "silhouette": "Minimalist 2D vector stickman with pressurized white helmet & cyan life-support backpack",
                "face_shape": "Circular light head with reflective visor",
                "face_color": "#F5F6F8",
                "headwear": "Pressurized EVA Helmet with cyan HUD reflection",
                "clothing": "White-grey exploration suit with life support chest unit",
                "legs_and_feet": "Dark stickman legs with heavy lunar/martian boots",
                "expression_library": ["curious", "alert", "focused", "relief", "shock"],
                "body_animations": ["walk_explore", "low_gravity_jump", "check_telemetry", "enter_airlock", "panic_o2", "point_sky"]
            },
            "scenes": calculated_scenes,
            "words": all_subtitle_words,
            "audio_url": "space_soundtrack.wav"
        }

        with open(project_dir / "project_data.json", "w", encoding="utf-8") as f:
            json.dump(project_data, f, indent=2)

        with open(PUBLIC_DIR / "project_data.json", "w", encoding="utf-8") as f:
            json.dump(project_data, f, indent=2)

        return project_data

    def _master_audio(self, project_dir: Path, pdata: Dict[str, Any]) -> Path:
        total_dur = pdata["total_duration"]
        scenes = pdata["scenes"]
        voice_path = project_dir / "voice_raw.mp3"
        out_soundtrack = project_dir / "space_soundtrack.wav"

        bgm_path = ASSETS_DIR / "bgm" / "cinematic_tension_score.wav"
        sfx_dir = ASSETS_DIR / "sfx"

        s1_t = scenes[0]["start_time"]
        s2_t = scenes[1]["start_time"]
        s3_t = scenes[2]["start_time"]
        s4_t = scenes[3]["start_time"]
        s5_t = scenes[4]["start_time"]
        s6_t = scenes[5]["start_time"]

        filter_complex = (
            f"[0:a]volume=1.0[voice];"
            f"[1:a]aloop=loop=-1:size=2e+09,atrim=0:{total_dur:.2f},volume=0.12,afade=t=in:st=0:d=1.5,afade=t=out:st={total_dur-2:.2f}:d=2[bgm];"
            f"[2:a]adelay={int(s1_t * 1000)}|{int(s1_t * 1000)},volume=0.15[sfx1];"
            f"[3:a]adelay={int(s2_t * 1000 + 400)}|{int(s2_t * 1000 + 400)},volume=0.25[sfx2];"
            f"[4:a]adelay={int(s3_t * 1000 + 300)}|{int(s3_t * 1000 + 300)},volume=0.22[sfx3];"
            f"[5:a]adelay={int(s4_t * 1000 + 200)}|{int(s4_t * 1000 + 200)},volume=0.20[sfx4];"
            f"[6:a]adelay={int(s5_t * 1000 + 100)}|{int(s5_t * 1000 + 100)},volume=0.28[sfx5];"
            f"[7:a]adelay={int(s6_t * 1000)}|{int(s6_t * 1000)},volume=0.35[sfx6];"
            f"[voice][bgm][sfx1][sfx2][sfx3][sfx4][sfx5][sfx6]amix=inputs=8:duration=first:dropout_transition=2[outa]"
        )

        cmd = [
            "ffmpeg", "-y",
            "-i", str(voice_path),
            "-i", str(bgm_path),
            "-i", str(sfx_dir / "radio_static.wav"),
            "-i", str(sfx_dir / "whoosh.wav"),
            "-i", str(sfx_dir / "digital_scan.wav"),
            "-i", str(sfx_dir / "elevator_ding.wav"),
            "-i", str(sfx_dir / "tension_pulse.wav"),
            "-i", str(sfx_dir / "boom.wav"),
            "-filter_complex", filter_complex,
            "-map", "[outa]",
            "-c:a", "pcm_s16le",
            "-ar", "44100",
            str(out_soundtrack)
        ]
        subprocess.run(cmd, check=True)
        shutil.copy2(out_soundtrack, PUBLIC_DIR / "space_soundtrack.wav")
        return out_soundtrack

    def _render_video(self, project_dir: Path, output_mp4: Path) -> None:
        cmd = [
            "npx", "--prefix", "renderer", "remotion", "render",
            "renderer/src/index.ts", "WhatIfShort", str(output_mp4),
            "--public-dir=renderer/public",
            f"--props={project_dir / 'project_data.json'}"
        ]
        subprocess.run(cmd, check=True)

    def _get_audio_dur(self, file_path: Path) -> float:
        cmd = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(res.stdout.strip())

    def _generate_metadata(self, topic: str, planet: PlanetFacts, pdata: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "title": f"{topic} (Scientific Survival Simulation) #Shorts",
            "description": (
                f"What if you actually lived on {planet.name}? Could human biology survive the extreme {planet.gravity_g}g gravity, "
                f"{planet.surface_temp_avg} temperatures, and lethal {planet.atmosphere_composition.split(',')[0]} atmosphere?\n\n"
                f"Survive the mission: Would you pick Protocol A (Brave the Storm) or Protocol B (Cryo-Hibernate)?\n"
                f"Drop your vote in the comments!\n\n"
                f"#Space #WhatIf #Mars #Astronomy #Science #StickmanAnimation #Survival #Shorts"
            ),
            "tags": ["Space", "What If", planet.name, "Science", "Astronomy", "Stickman", "Animation", "Physics", "Survival"],
            "community_poll": {
                "question": f"Day 18 Crisis on {planet.name}: Oxygen at 22%. What is your survival protocol?",
                "option_a": "Protocol A: Brave the 100 km/h dust storm & clean the solar panels",
                "option_b": "Protocol B: Cut habitat heat & cryo-hibernate in the rover pod"
            }
        }
