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

    # Build ffmpeg complex filter
    # Inputs:
    # 0: voice_raw.mp3
    # 1: bgm (loop)
    # 2: radio_static.wav (scene 1 comms)
    # 3: whoosh.wav (scene 2 low-g float)
    # 4: digital_scan.wav (scene 3 infographic scan)
    # 5: elevator_ding.wav (scene 4 airlock chime)
    # 6: tension_pulse.wav (scene 5 storm pulse)
    # 7: boom.wav (scene 6 cliffhanger hit)

    sfx_static = sfx_dir / "radio_static.wav"
    sfx_whoosh = sfx_dir / "whoosh.wav"
    sfx_scan = sfx_dir / "digital_scan.wav"
    sfx_airlock = sfx_dir / "elevator_ding.wav"
    sfx_pulse = sfx_dir / "tension_pulse.wav"
    sfx_boom = sfx_dir / "boom.wav"

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
        "-i", str(VOICE_PATH),
        "-i", str(bgm_path),
        "-i", str(sfx_static),
        "-i", str(sfx_whoosh),
        "-i", str(sfx_scan),
        "-i", str(sfx_airlock),
        "-i", str(sfx_pulse),
        "-i", str(sfx_boom),
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
