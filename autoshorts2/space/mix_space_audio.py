"""Master and mix speech, space tension ambient BGM, and sound effects into space_soundtrack.wav
"""
import json
import shutil
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
PROJECT_DIR = ROOT_DIR / "projects" / "mars_demo"
PUBLIC_DIR = ROOT_DIR / "renderer" / "public"
ASSETS_DIR = ROOT_DIR / "autoshorts2" / "assets"

VOICE_PATH = PROJECT_DIR / "voice_raw.mp3"
PROJECT_DATA_PATH = PROJECT_DIR / "project_data.json"
OUTPUT_AUDIO = PROJECT_DIR / "space_soundtrack.wav"

def mix_audio():
    if not PROJECT_DATA_PATH.exists() or not VOICE_PATH.exists():
        print("Waiting for voice and project data...")
        return False

    with open(PROJECT_DATA_PATH, "r", encoding="utf-8") as f:
        pdata = json.load(f)

    total_dur = pdata["total_duration"]
    scenes = pdata["scenes"]

    bgm_path = ASSETS_DIR / "bgm" / "cinematic_tension_score.wav"
    sfx_dir = ASSETS_DIR / "sfx"

    # Scene timestamps
    s1_t = scenes[0]["start_time"]
    s2_t = scenes[1]["start_time"]
    s3_t = scenes[2]["start_time"]
    s4_t = scenes[3]["start_time"]
    s5_t = scenes[4]["start_time"]
    s6_t = scenes[5]["start_time"]

    # Clean documentary audio mix: Pure Brian Neural Voice + Subtle Cinematic Tension BGM (No artificial SFX)
    filter_complex = (
        f"[0:a]volume=1.0[voice];"
        f"[1:a]aloop=loop=-1:size=2e+09,atrim=0:{total_dur:.2f},volume=0.10,afade=t=in:st=0:d=1.0,afade=t=out:st={total_dur-1.5:.2f}:d=1.5[bgm];"
        f"[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[outa]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(VOICE_PATH),
        "-i", str(bgm_path),
        "-filter_complex", filter_complex,
        "-map", "[outa]",
        "-c:a", "pcm_s16le",
        "-ar", "44100",
        str(OUTPUT_AUDIO)
    ]

    print("Running audio mix with ffmpeg...")
    subprocess.run(cmd, check=True)
    print(f"Master soundtrack generated: {OUTPUT_AUDIO}")

    # Copy to renderer/public
    public_audio = PUBLIC_DIR / "space_soundtrack.wav"
    shutil.copy2(OUTPUT_AUDIO, public_audio)
    print(f"Copied to public dir: {public_audio}")
    return True

if __name__ == "__main__":
    mix_audio()
