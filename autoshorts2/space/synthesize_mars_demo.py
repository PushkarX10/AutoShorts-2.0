"""Synthesize scene-by-scene voiceover with exact durations and word alignments for Mars Demo Short (Target 50s-52s).
"""
import asyncio
import json
import shutil
import subprocess
from pathlib import Path
import edge_tts

ROOT_DIR = Path(__file__).resolve().parents[2]
PROJECTS_DIR = ROOT_DIR / "projects"
PROJECT_DIR = PROJECTS_DIR / "mars_demo"
PUBLIC_DIR = ROOT_DIR / "renderer" / "public"

VOICE = "en-US-ChristopherNeural"
RATE = "+9%"  # clear, punchy, engaging tempo

SCENE_DEFS = [
    {
        "scene_id": 1,
        "beat": "HOOK",
        "narration": "What if you woke up on Mars tomorrow... with only thirty days of supplies?",
        "environment": "mars_surface",
        "camera": "slow_push_in",
        "character_action": "Looking out across the red Martian horizon",
        "character_pose": "walk_explore",
        "character_expression": "curious",
        "lighting": "subtle_cinematic",
        "music_state": "mystery",
        "transition": "cut",
        "hud_state": {
            "label_1": "Mars",
            "val_1": "SOL 01",
            "label_2": "-63°C",
            "val_2": "-63°C",
            "label_3": "0.38g",
            "val_3": "0.38g",
            "progress_percent": 95,
        }
    },
    {
        "scene_id": 2,
        "beat": "GRAVITY_REVEAL",
        "narration": "On Mars, gravity is only thirty-eight percent of Earth. Every single jump sends you soaring in slow-motion flight.",
        "environment": "mars_surface",
        "camera": "pan_up",
        "character_action": "Jumping across Martian dunes in buoyant low gravity",
        "character_pose": "low_gravity_jump",
        "character_expression": "alert",
        "lighting": "subtle_cinematic",
        "music_state": "wonder",
        "transition": "cut",
        "hud_state": {
            "label_1": "Mars",
            "val_1": "SOL 05",
            "label_2": "-55°C",
            "val_2": "-55°C",
            "label_3": "0.38g",
            "val_3": "0.38g (LOW-G)",
            "progress_percent": 91,
        }
    },
    {
        "scene_id": 3,
        "beat": "SCIENTIFIC_HAZARD",
        "narration": "Outside your suit, Mars is lethal. The air is ninety-five percent carbon dioxide, and air pressure is near vacuum. Without this suit, your blood boils in fifteen seconds.",
        "environment": "planet_comparison",
        "camera": "slow_push_in",
        "character_action": "Scanning planetary telemetry comparison",
        "character_pose": "check_telemetry",
        "character_expression": "focused",
        "lighting": "infographic_neon",
        "music_state": "tension",
        "transition": "cut",
        "hud_state": {
            "label_1": "Mars",
            "val_1": "SOL 12",
            "label_2": "-72°C",
            "val_2": "-72°C",
            "label_3": "0.006 ATM",
            "val_3": "0.006 ATM",
            "progress_percent": 82,
        }
    },
    {
        "scene_id": 4,
        "beat": "HABITAT_SANCTUARY",
        "narration": "Your only sanctuary is Base Alpha: a geodesic dome with hydroponic crops and solar oxygen scrubbers.",
        "environment": "mars_habitat",
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
        "environment": "mars_dust_storm",
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

EMPHASIS_KEYWORDS = {
    "mars", "tomorrow", "thirty", "supplies", "gravity", "thirty-eight", "earth", "soaring",
    "slow-motion", "lethal", "ninety-five", "carbon", "dioxide", "vacuum", "boils", "fifteen",
    "base", "alpha", "geodesic", "hydroponic", "oxygen", "eighteen", "storm", "blots",
    "crashes", "eighty-five", "twenty-two", "protocols", "option", "storm", "clear",
    "cryo-hibernate", "rover", "survive", "comment", "a", "b"
}

def get_audio_duration(file_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

async def synthesize_scenes():
    PROJECT_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    scenes_audio_dir = PROJECT_DIR / "scene_audios"
    scenes_audio_dir.mkdir(parents=True, exist_ok=True)

    print("[1] Synthesizing scene-by-scene narration (Target: ~51s)...")
    scene_files = []
    all_subtitle_words = []
    calculated_scenes = []
    running_time = 0.0

    for sc in SCENE_DEFS:
        scene_id = sc["scene_id"]
        text = sc["narration"]
        out_mp3 = scenes_audio_dir / f"scene_{scene_id}.mp3"

        communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
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

        duration = get_audio_duration(out_mp3)
        scene_files.append(out_mp3)

        # Build word alignments for this scene
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

        # Padding between scenes
        scene_pad = 0.15 if scene_id < 6 else 0.50
        scene_total_dur = round(duration + scene_pad, 2)
        scene_end = round(running_time + scene_total_dur, 2)

        sc_data = dict(sc)
        sc_data["start_time"] = round(running_time, 2)
        sc_data["end_time"] = scene_end
        sc_data["duration"] = scene_total_dur
        calculated_scenes.append(sc_data)

        print(f"  Scene {scene_id}: Audio={duration:.2f}s | Range=[{running_time:.2f}s - {scene_end:.2f}s] ({scene_total_dur:.2f}s)")
        running_time = scene_end

    total_duration = calculated_scenes[-1]["end_time"]

    concat_list = scenes_audio_dir / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for sf in scene_files:
            escaped = str(sf.resolve()).replace("\\", "/")
            f.write(f"file '{escaped}'\n")

    raw_voice_out = PROJECT_DIR / "voice_raw.mp3"
    concat_cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(raw_voice_out)
    ]
    subprocess.run(concat_cmd, check=True)
    print(f"\n[2] Concatenated voiceover: {raw_voice_out} (Duration: {total_duration:.2f}s)")

    # Write project_data.json
    project_data = {
        "project_id": "whatif_mars_30days",
        "topic": "What If You Lived on Mars for 30 Days?",
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

    project_data_path = PROJECT_DIR / "project_data.json"
    with open(project_data_path, "w", encoding="utf-8") as f:
        json.dump(project_data, f, indent=2)

    public_target = PUBLIC_DIR / "project_data.json"
    with open(public_target, "w", encoding="utf-8") as f:
        json.dump(project_data, f, indent=2)

    print(f"[3] Successfully wrote project_data.json ({len(all_subtitle_words)} words, {len(calculated_scenes)} scenes, Total: {total_duration:.2f}s)")

if __name__ == "__main__":
    asyncio.run(synthesize_scenes())
