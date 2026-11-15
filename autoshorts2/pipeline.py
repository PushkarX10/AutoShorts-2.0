"""AutoShorts 2.0 Autonomous Generation Pipeline
Implements the 45-point autonomous creation engine:
Research -> Angles -> Hooks -> Script -> Character Bible -> Audio & Subtitles -> Remotion 1080x1920 30FPS Video -> Quality Control -> 16 Packaged Deliverables.
"""

import json
import time
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

from autoshorts2.config import (
    ROOT_DIR, PROJECTS_DIR, OUTPUT_DIR, RENDERER_DIR,
    DEFAULT_VOICE, FPS, VIDEO_WIDTH, VIDEO_HEIGHT
)
from autoshorts2.models import (
    ShortProject, Storyboard, FinalOutputPackage
)
from autoshorts2.agents.research_agent import ResearchAgent
from autoshorts2.agents.story_angle_generator import StoryAngleGenerator, HookOptimizer
from autoshorts2.agents.script_writer import ScriptWriter
from autoshorts2.agents.character_bible import create_default_protagonist
from autoshorts2.agents.qc_auditor import QualityControlAuditor
from autoshorts2.voice.tts_engine import TTSEngine
from autoshorts2.voice.subtitle_generator import SubtitleGenerator
from autoshorts2.audio.audio_mixer import AudioMixer

class AutoShortsPipeline:
    def __init__(self, voice: str = DEFAULT_VOICE):
        self.voice = voice
        self.research_agent = ResearchAgent()
        self.angle_gen = StoryAngleGenerator()
        self.hook_optimizer = HookOptimizer()
        self.script_writer = ScriptWriter()
        self.tts_engine = TTSEngine(voice=voice)
        self.audio_mixer = AudioMixer()
        self.subtitle_gen = SubtitleGenerator()
        self.qc_auditor = QualityControlAuditor()

    def run(self, topic: str = "US Mint $1 Coin Free Shipping Loophole") -> ShortProject:
        timestamp = int(time.time())
        project_id = f"autoshort_cinematic_{timestamp}"
        project_dir = PROJECTS_DIR / project_id
        project_dir.mkdir(parents=True, exist_ok=True)
        
        print("\n=======================================================")
        print(f"[AUTOSHORTS 2.0] CINEMATIC SHORTS ENGINE")
        print(f"Project ID: {project_id}")
        print(f"Topic: {topic}")
        print("=======================================================\n")

        # 1. Research & Fact Verification
        print("[1/9] Researching factual claims & statutory background...")
        fact_sheet = self.research_agent.research_topic(topic)
        print(f"  -> Extracted {len(fact_sheet.claims)} verified claims.")

        # 2. Story Angle Generation
        print("\n[2/9] Generating 5 story angles & scoring retention potential...")
        angles = self.angle_gen.generate_angles(fact_sheet)
        selected_angle = angles[0]
        print(f"  -> Selected Angle: '{selected_angle.title}' (Score: {selected_angle.total_score}/10)")

        # 3. Hook Optimization
        print("\n[3/9] Generating 10 scored hooks (PERSON + ACTION + CONSEQUENCE)...")
        selected_hook, all_hooks = self.hook_optimizer.generate_and_score_hooks(selected_angle)
        print(f"  -> Winner Hook: \"{selected_hook.hook_text}\" (Score: {selected_hook.total_score}/10)")

        # 4. Character Bible & Protagonist Consistency
        print("\n[4/9] Loading persistent protagonist Character Bible...")
        char_bible = create_default_protagonist()
        print(f"  -> Protagonist: {char_bible.name}")

        # 5. Script Writing & Scene Planning
        print("\n[5/9] Writing high-retention script & 6-beat scene plan...")
        script_res = self.script_writer.create_script(selected_hook, fact_sheet)
        print(f"  -> Planned {len(script_res.scenes)} dynamic scenes (Total Words: {script_res.word_count})")

        # 6. Neural Voice Synthesis & Whisper Word Alignment
        print(f"\n[6/9] Synthesizing documentary narration ({self.voice}) with Whisper timestamps...")
        raw_voice_path = project_dir / "voice.mp3"
        total_audio_dur, subtitle_words = self.tts_engine.synthesize_sync(
            script_res.full_script_text, raw_voice_path
        )
        print(f"  -> Audio Duration: {total_audio_dur:.2f}s | Words Aligned: {len(subtitle_words)}")

        # Distribute scene durations based on audio alignment
        scene_end_times = []
        w_idx = 0
        for s in script_res.scenes:
            last_word_target = s.narration.split()[-1].lower().rstrip(".,!?\"'")
            found_t = None
            for i in range(w_idx, len(subtitle_words)):
                clean = subtitle_words[i].word.lower().rstrip(".,!?\"'")
                if clean == last_word_target:
                    found_t = subtitle_words[i].end
                    w_idx = i + 1
                    break
            if found_t is not None:
                scene_end_times.append(found_t)
            else:
                prev = scene_end_times[-1] if scene_end_times else 0.0
                scene_end_times.append(prev + 5.5)
        if scene_end_times:
            scene_end_times[-1] = total_audio_dur

        curr_t = 0.0
        for idx, scene in enumerate(script_res.scenes):
            end_t = scene_end_times[idx]
            scene.start_time = round(curr_t, 3)
            scene.end_time = round(end_t, 3)
            scene.duration = round(end_t - curr_t, 3)
            curr_t = end_t

        # 7. Subtitle Generation (.srt and .ass)
        print("\n[7/9] Exporting burned-in subtitle tracks with electric pink emphasis...")
        srt_file = project_dir / "subtitles.srt"
        ass_file = project_dir / "subtitles.ass"
        self.subtitle_gen.export_srt(subtitle_words, srt_file)
        self.subtitle_gen.export_ass(subtitle_words, ass_file)

        storyboard = Storyboard(
            project_id=project_id,
            topic=topic,
            voice_profile=self.voice,
            total_duration=round(total_audio_dur, 3),
            scenes=script_res.scenes,
            words=subtitle_words
        )

        # 8. Audio Mastering (Narration + Ducked Tension BGM + Synced SFX)
        print("\n[8/9] Mastering multi-track audio soundtrack (-14 LUFS)...")
        master_soundtrack = project_dir / "soundtrack.wav"
        self.audio_mixer.mix_soundtrack(raw_voice_path, storyboard, master_soundtrack)
        print(f"  -> Master soundtrack exported: {master_soundtrack.name}")

        # QC Audit before render
        qc_report = self.qc_auditor.audit_project(script_res, storyboard)
        print(f"  -> QC Audit Status: {'PASSED' if qc_report['passed'] else 'WARNING'}")

        # 9. Remotion Video Rendering (1080x1920 30FPS H.264)
        print("\n[9/9] Rendering broadcast 1080x1920 30FPS MP4 via Remotion Engine...")
        
        # Prepare Remotion props data
        remotion_props = {
            "project_id": project_id,
            "topic": topic,
            "total_duration": storyboard.total_duration,
            "character_bible": char_bible.model_dump(),
            "scenes": [s.model_dump() for s in storyboard.scenes],
            "words": [w.model_dump() for w in storyboard.words],
            "audio_url": "soundtrack.wav"
        }
        
        props_file = RENDERER_DIR / "public" / "project.json"
        props_file.parent.mkdir(parents=True, exist_ok=True)
        props_file.write_text(json.dumps(remotion_props, indent=2), encoding="utf-8")
        shutil.copy(master_soundtrack, RENDERER_DIR / "public" / "soundtrack.wav")
        
        final_mp4 = project_dir / "final_short.mp4"
        total_frames = int(storyboard.total_duration * FPS)

        render_cmd = [
            "npx.cmd", "remotion", "render",
            "src/index.ts", "CinematicShort",
            str(final_mp4.resolve()),
            "--props=public/project.json",
            f"--frames=0-{total_frames - 1}",
            "--concurrency=4"
        ]
        
        subprocess.run(render_cmd, cwd=str(RENDERER_DIR), shell=True, check=True)
        print(f"  -> Video Render Complete: {final_mp4.name} ({final_mp4.stat().st_size / 1_000_000:.2f} MB)")

        # Render Thumbnail at 4.0s mark
        thumbnail_png = project_dir / "thumbnail.png"
        thumb_frame = min(total_frames - 10, int(4.0 * FPS))
        thumb_cmd = [
            "npx.cmd", "remotion", "still",
            "src/index.ts", "CinematicShort",
            str(thumbnail_png.resolve()),
            "--props=public/project.json",
            f"--frame={thumb_frame}"
        ]
        subprocess.run(thumb_cmd, cwd=str(RENDERER_DIR), shell=True, check=True)
        print(f"  -> High-Res Thumbnail Rendered: {thumbnail_png.name}")

        # Assemble Full 16-Item Package
        visual_prompts = []
        for sc in storyboard.scenes:
            visual_prompts.append({
                "scene_id": str(sc.scene_id),
                "prompt": (
                    f"Vertical cinematic 2D digital illustration, simplified expressive cartoon character ({char_bible.silhouette}), "
                    f"inside {sc.environment}, {sc.visual_description}, {sc.lighting} lighting, dramatic warm shadows, "
                    f"thick clean black outlines, hand-drawn texture, muted palette with selective neon pink accents (#FF2A85), "
                    f"cinematic 9:16 vertical perspective, high detail."
                )
            })

        sfx_timeline = [
            {"time_sec": sc.start_time, "scene": sc.scene_id, "sfx": sc.sound_effect}
            for sc in storyboard.scenes if sc.sound_effect
        ]

        editing_timeline = [
            {
                "scene_id": sc.scene_id,
                "beat": sc.beat,
                "start": sc.start_time,
                "end": sc.end_time,
                "duration": sc.duration,
                "camera": sc.camera,
                "transition": sc.transition
            }
            for sc in storyboard.scenes
        ]

        package = FinalOutputPackage(
            title="The $300,000 Government Coin Glitch",
            hook=selected_hook.hook_text,
            full_script=script_res.full_script_text,
            character_bible=char_bible,
            scene_plan=[s.model_dump() for s in storyboard.scenes],
            visual_prompts=visual_prompts,
            infographic_specs=[
                sc.infographic_spec.model_dump() for sc in storyboard.scenes if sc.infographic_spec
            ],
            voiceover_script=script_res.full_script_text,
            subtitle_file_srt=srt_file.read_text(encoding="utf-8"),
            subtitle_file_ass=ass_file.read_text(encoding="utf-8"),
            music_direction={
                "0_10s": "Subtle mystery (deep sub-bass drone and Rhodes chimes)",
                "10_30s": "Increasing tension (ticking clock 8th notes and heartbeat bass)",
                "30_50s": "Analytical documentary arpeggio (crisp synth sequence)",
                "50_65s": "Climax tension & sudden drop into dead silence",
                "ending": "Dramatic brass sting & coin impact hit"
            },
            sfx_timeline=sfx_timeline,
            editing_timeline=editing_timeline,
            final_mp4_path=str(final_mp4.resolve()),
            thumbnail_path=str(thumbnail_png.resolve()),
            youtube_description=(
                "He ordered $300,000 in government coins with free shipping... and earned thousands in free cashback.\n\n"
                "In 2008, the US Mint created the Presidential $1 Coin Direct Ship program to promote currency circulation. "
                "Because purchases were made at face value ($1 for $1) with credit cards and $0 shipping, clever arbitrageurs "
                "wheeled millions in coins into banks to pay off their cards—racking up free cash and lifetime airline status.\n\n"
                "Did he break the law? Watch till the end to find out what the Secret Service discovered.\n\n"
                "#Money #Loophole #Finance #Animation #Arbitrage #Banking #TrueStory #Shorts"
            ),
            hashtags=["#Money", "#Loophole", "#Finance", "#Arbitrage", "#Shorts", "#TrueStory", "#Banking"]
        )

        project = ShortProject(
            project_id=project_id,
            topic=topic,
            research=fact_sheet,
            selected_angle=selected_angle,
            character_bible=char_bible,
            script=script_res,
            storyboard=storyboard,
            audio_path=str(master_soundtrack.resolve()),
            final_video_path=str(final_mp4.resolve()),
            thumbnail_path=str(thumbnail_png.resolve()),
            output_package=package,
            created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ")
        )

        # Save project metadata and mirror to output/
        project_json_file = project_dir / "project.json"
        project_json_file.write_text(project.model_dump_json(indent=2), encoding="utf-8")
        
        # Mirror exports to root and output/
        shutil.copy(final_mp4, OUTPUT_DIR / "final_short.mp4")
        shutil.copy(thumbnail_png, OUTPUT_DIR / "thumbnail.png")
        shutil.copy(final_mp4, ROOT_DIR / "final_short.mp4")
        shutil.copy(thumbnail_png, ROOT_DIR / "thumbnail.png")

        print("\n=======================================================")
        print("[SUCCESS] AUTOSHORTS 2.0 PIPELINE COMPLETED SUCCESSFULLY!")
        print(f"Final MP4: {final_mp4.resolve()}")
        print(f"Thumbnail: {thumbnail_png.resolve()}")
        print("=======================================================\n")
        return project
