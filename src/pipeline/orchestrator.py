"""
AutoShorts 2.0 — End-to-End Pipeline Orchestrator.

Takes a single input (gaming parkour video clip) and automatically executes:
  1. Video Ingestion & Probing
  2. LLM Conversation Generation & Quality Check
  3. Edge-TTS Voice Generation & Audio Manifest
  4. Frame-Accurate Timeline Calculation
  5. Background Video Processing (9:16 Vertical Crop/Blur-Fill)
  6. Audio Timeline Mixing (Voices + Pops + Typing + Punchline + Chill BGM)
  7. Animated Chat Overlay Rendering & Video Composition
  8. Quality Assurance & Validation
  9. YouTube Metadata & SEO Generation
 10. Final Asset Packaging & Export
"""
from __future__ import annotations

import json
import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

from rich.console import Console

from src.audio.audio_mixer import mix_master_audio
from src.chat.animation_timeline import build_timeline
from src.config.settings import get, get_output_dir, get_temp_dir
from src.ingestion.video_inspector import inspect_video
from src.llm.conversation_generator import generate_conversation
from src.llm.metadata_generator import generate_metadata
from src.llm.quality_checker import check_conversation_quality
from src.models.schemas import (
    Conversation, HumorStyle, Job, JobStatus, VideoInfo,
)
from src.tts.speech_generator import generate_all_speech
from src.tts.voice_manager import VoiceManager
from src.validation.video_validator import validate_video
from src.video.background_processor import process_background
from src.video.video_compositor import compose_video

console = Console()


class PipelineOrchestrator:
    """
    Coordinates all stages of YouTube Shorts generation.
    """

    def __init__(self):
        self.voice_manager = VoiceManager()

    def run(
        self,
        input_video_path: str | Path,
        conversation: Optional[Conversation] = None,
        humor_style: HumorStyle = HumorStyle.WHOLESOME,
        theme: Optional[str] = None,
        job_id: Optional[str] = None,
        progress_callback: Optional[Callable[[Job], None]] = None,
    ) -> Job:
        """
        Execute the end-to-end video creation pipeline.
        """
        input_path = Path(input_video_path).resolve()
        if not input_path.exists():
            raise FileNotFoundError(f"Input video file not found: {input_path}")

        job = Job(
            input_path=str(input_path),
            humor_style=humor_style,
        )
        if job_id:
            job.id = job_id

        temp_job_dir = get_temp_dir() / job.id
        temp_job_dir.mkdir(parents=True, exist_ok=True)

        def _update(status: JobStatus, progress: int = -1, error: str | None = None):
            job.set_status(status, progress)
            if error:
                job.error = error
            if progress_callback:
                progress_callback(job)

        console.rule(f"[bold cyan]AutoShorts 2.0 — Job {job.id}[/bold cyan]")
        t0 = time.time()

        try:
            # ── 1. Video Ingestion ─────────────────────────────────────────
            _update(JobStatus.INSPECTING, 5)
            console.print(f"[bold cyan][1/9] Inspecting Input Video…[/bold cyan]")
            video_info = inspect_video(input_path)
            if not video_info.is_valid:
                raise ValueError(f"Input video is invalid: {video_info.error}")
            job.video_info = video_info
            console.print(f"  Duration: {video_info.duration:.1f}s | {video_info.width}x{video_info.height} | {video_info.fps:.1f} fps")

            # ── 2. Conversation Loading / Generation ────────────────────────
            _update(JobStatus.GENERATING_CONVERSATION, 15)
            if conversation is not None:
                console.print(f"[bold cyan][2/9] Using Custom Conversation Input…[/bold cyan]")
                if theme and not conversation.theme:
                    conversation.theme = theme
            else:
                console.print(f"[bold cyan][2/9] Generating Comedy Script via Local LLM…[/bold cyan]")
                conversation = generate_conversation(
                    humor_style=humor_style,
                    num_characters=get("comedy", "num_characters", 2),
                    min_messages=get("comedy", "min_messages", 10),
                    max_messages=get("comedy", "max_messages", 18),
                )
                if theme:
                    conversation.theme = theme

            # Quality Check
            passed, issues = check_conversation_quality(conversation)
            job.conversation = conversation
            console.print(f"  Story Title: [bold green]{conversation.story_title}[/bold green] ({len(conversation.messages)} messages)")

            # ── 3. Edge-TTS Voice Generation ──────────────────────────────
            _update(JobStatus.GENERATING_VOICES, 30)
            console.print(f"[bold cyan][3/9] Synthesizing Character Voices…[/bold cyan]")
            audio_dir = temp_job_dir / "audio"
            manifest = generate_all_speech(
                conversation=conversation,
                voice_manager=self.voice_manager,
                output_dir=audio_dir,
            )
            job.audio_manifest = manifest

            # ── 4. Animation Timeline Calculation ─────────────────────────
            _update(JobStatus.BUILDING_TIMELINE, 45)
            console.print(f"[bold cyan][4/9] Calculating Synchronized Timeline…[/bold cyan]")
            fps = get("video", "fps", 30)
            timeline = build_timeline(conversation, manifest, fps=fps)
            job.timeline = timeline
            console.print(f"  Target video length: {timeline.total_duration_sec:.1f}s ({timeline.total_frames} frames)")

            # ── 5. Background Video Processing ────────────────────────────
            _update(JobStatus.COMPOSITING, 52)
            console.print(f"[bold cyan][5/9] Processing Background Gameplay (9:16 Vertical)…[/bold cyan]")
            bg_output_path = temp_job_dir / "background_processed.mp4"
            process_background(
                video_info=video_info,
                target_duration=timeline.total_duration_sec,
                output_path=bg_output_path,
            )

            # ── 6. Audio Mixing ───────────────────────────────────────────
            _update(JobStatus.COMPOSITING, 60)
            console.print(f"[bold cyan][6/9] Mixing Audio Master Track (Voices + SFX + BGM)…[/bold cyan]")
            master_audio_path = temp_job_dir / "master_audio.wav"
            mix_master_audio(
                timeline=timeline,
                audio_manifest=manifest,
                output_path=master_audio_path,
            )

            # ── 7. Chat Overlay Rendering & Composition ───────────────────
            _update(JobStatus.ENCODING, 68)
            console.print(f"[bold cyan][7/9] Compositing Chat Overlay with Gameplay Footage…[/bold cyan]")
            raw_rendered_video = temp_job_dir / "composed_video.mp4"

            def _comp_prog(pct: int, desc: str):
                overall_pct = 68 + int(pct * 0.16)
                _update(JobStatus.ENCODING, overall_pct)

            compose_video(
                background_video_path=bg_output_path,
                conversation=conversation,
                timeline=timeline,
                master_audio_path=master_audio_path,
                output_path=raw_rendered_video,
                progress_callback=_comp_prog,
            )

            # ── 8. Quality Assurance & Validation ─────────────────────────
            _update(JobStatus.VALIDATING, 86)
            console.print(f"[bold cyan][8/9] Running Quality Assurance Checks…[/bold cyan]")
            qa_report = validate_video(raw_rendered_video, job_id=job.id)
            job.quality_report = qa_report

            # ── 9. YouTube Metadata & Packaging ───────────────────────────
            _update(JobStatus.GENERATING_METADATA, 92)
            console.print(f"[bold cyan][9/9] Generating YouTube Metadata & Packaging Assets…[/bold cyan]")
            metadata = generate_metadata(conversation)
            job.youtube_metadata = metadata

            # Packaging to output directory
            date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = metadata.suggested_filename or "funny_chat_story"
            bundle_dir_name = f"{date_str}_{job.id}_{safe_title}"
            final_bundle_dir = get_output_dir() / bundle_dir_name
            final_bundle_dir.mkdir(parents=True, exist_ok=True)

            # Copy video
            final_video_path = final_bundle_dir / f"{safe_title}.mp4"
            shutil.copy2(raw_rendered_video, final_video_path)
            job.output_video_path = str(final_video_path)

            # Copy subtitles (.srt)
            raw_srt = raw_rendered_video.with_suffix(".srt")
            if raw_srt.exists():
                shutil.copy2(raw_srt, final_bundle_dir / f"{safe_title}.srt")

            # Copy thumbnail (.jpg)
            raw_thumb = raw_rendered_video.with_name(f"{raw_rendered_video.stem}_thumbnail.jpg")
            if raw_thumb.exists():
                shutil.copy2(raw_thumb, final_bundle_dir / f"{safe_title}_thumbnail.jpg")

            # Save conversation JSON
            convo_path = final_bundle_dir / "conversation.json"
            convo_path.write_text(conversation.model_dump_json(indent=2), encoding="utf-8")

            # Save metadata JSON & TXT
            meta_json_path = final_bundle_dir / "metadata.json"
            meta_json_path.write_text(metadata.model_dump_json(indent=2), encoding="utf-8")
            job.output_metadata_path = str(meta_json_path)

            meta_txt_path = final_bundle_dir / "youtube_upload_info.txt"
            _write_upload_guide(metadata, conversation, qa_report, meta_txt_path)

            # Save QA report
            qa_path = final_bundle_dir / "quality_report.json"
            qa_path.write_text(qa_report.model_dump_json(indent=2), encoding="utf-8")

            # Completed!
            _update(JobStatus.COMPLETED, 100)
            elapsed = time.time() - t0
            console.rule(f"[bold green]✓ Short Generated Successfully in {elapsed:.1f}s[/bold green]")
            console.print(f"  [bold]Video:[/bold] {final_video_path}")
            console.print(f"  [bold]Title:[/bold] {metadata.title}")
            console.print(f"  [bold]Hashtags:[/bold] {' '.join(metadata.hashtags)}")

            return job

        except Exception as e:
            console.print(f"[bold red]Pipeline Error:[/bold red] {e}")
            _update(JobStatus.FAILED, error=str(e))
            raise


def _write_upload_guide(metadata, conversation, qa_report, output_path: Path):
    """Write user-friendly copy-paste YouTube metadata file."""
    hashtags_str = " ".join(metadata.hashtags)
    content = f"""================================================================================
AUTOSHORTS 2.0 — YOUTUBE SHORTS UPLOAD METADATA
================================================================================

TITLE (Copy to YouTube Title field):
{metadata.title} {hashtags_str[:30]}

DESCRIPTION (Copy to YouTube Description field):
{metadata.description}

{hashtags_str}

--------------------------------------------------------------------------------
PINNED COMMENT (Post and pin in comments):
{metadata.pinned_comment}

--------------------------------------------------------------------------------
TAGS:
{', '.join([h.replace('#', '') for h in metadata.hashtags])}

--------------------------------------------------------------------------------
VIDEO METRICS:
Duration: {qa_report.duration_sec}s
Resolution: {qa_report.resolution}
Size: {qa_report.file_size_mb} MB
QA Status: {'Passed' if qa_report.all_passed else 'Warnings'}

CHARACTERS:
{chr(10).join([f"• {c.name} ({c.personality}) - Voice: {c.voice_id}" for c in conversation.characters])}
================================================================================
"""
    output_path.write_text(content, encoding="utf-8")
