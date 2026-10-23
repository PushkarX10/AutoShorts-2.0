"""
AutoShorts 2.0 — FastAPI Web Studio & Dashboard.

Provides a rich visual UI for uploading gameplay footage, configuring humor styles,
triggering video generation, viewing live multi-stage pipeline logs, previewing the
vertical video in real-time, and copying YouTube metadata.
"""
from __future__ import annotations

import asyncio
import json
import os
import shutil
import threading
import time
import uuid
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.config.settings import (
    get, get_available_voices, get_input_dir, get_output_dir, get_project_root, get_temp_dir,
)
from src.ingestion.video_inspector import inspect_video
from src.models.schemas import HumorStyle, Job, JobStatus
from src.pipeline.orchestrator import PipelineOrchestrator
from src.video.sample_generator import generate_sample_gaming_clip

app = FastAPI(
    title="AutoShorts 2.0 Studio",
    description="Local AI YouTube Shorts Automation Factory",
    version="2.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory job registry & log buffers
_jobs_lock = threading.Lock()
_jobs: dict[str, Job] = {}
_job_logs: dict[str, list[dict[str, Any]]] = {}

# Static mounts
root_dir = get_project_root()
static_dir = Path(__file__).resolve().parent / "static"
templates_dir = Path(__file__).resolve().parent / "templates"
output_dir = get_output_dir()
static_dir.mkdir(parents=True, exist_ok=True)
templates_dir.mkdir(parents=True, exist_ok=True)
output_dir.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
app.mount("/output", StaticFiles(directory=str(output_dir)), name="output")


def _log_job_event(job_id: str, level: str, message: str):
    """Append a log event for SSE broadcasting."""
    with _jobs_lock:
        if job_id not in _job_logs:
            _job_logs[job_id] = []
        _job_logs[job_id].append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "level": level,
            "message": message,
        })


# ── API Models ─────────────────────────────────────────────────────────────

class GenerateRequest(BaseModel):
    video_filename: str
    humor_style: str = "wholesome"
    theme: Optional[str] = None
    character_count: int = 2


# ── Routes ─────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index():
    index_file = templates_dir / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Dashboard UI not found")
    return HTMLResponse(content=index_file.read_text(encoding="utf-8"))


@app.get("/api/status")
async def get_system_status():
    """Get overall system readiness and metrics."""
    import httpx
    ollama_url = get("llm", "base_url", "http://localhost:11434")
    model_name = get("llm", "model", "llama3.1:latest")
    ollama_ready = False
    try:
        r = httpx.get(f"{ollama_url}/api/tags", timeout=2)
        ollama_ready = (r.status_code == 200)
    except Exception:
        ollama_ready = False

    ffmpeg_ready = shutil.which("ffmpeg") is not None
    input_files = list(get_input_dir().glob("*.mp4")) + list(get_input_dir().glob("*.mov"))
    output_shorts = [d for d in get_output_dir().iterdir() if d.is_dir()]

    return {
        "status": "ready" if (ffmpeg_ready and ollama_ready) else "degraded",
        "ffmpeg": ffmpeg_ready,
        "ollama": {
            "online": ollama_ready,
            "model": model_name,
            "url": ollama_url,
        },
        "voices_count": len(get_available_voices()),
        "input_videos_count": len(input_files),
        "generated_shorts_count": len(output_shorts),
    }


@app.get("/api/inputs")
async def list_input_videos():
    """List videos available in the input/ folder."""
    in_dir = get_input_dir()
    files = []
    for ext in ("*.mp4", "*.mov", "*.mkv", "*.webm"):
        for f in in_dir.glob(ext):
            try:
                info = inspect_video(f)
                files.append({
                    "filename": f.name,
                    "path": str(f),
                    "size_mb": info.file_size_mb,
                    "duration": info.duration,
                    "resolution": f"{info.width}x{info.height}",
                    "orientation": info.orientation,
                    "is_valid": info.is_valid,
                })
            except Exception:
                files.append({
                    "filename": f.name,
                    "path": str(f),
                    "size_mb": round(f.stat().st_size / (1024 * 1024), 2),
                    "duration": 0,
                    "resolution": "unknown",
                    "orientation": "unknown",
                    "is_valid": True,
                })
    return {"videos": files}


@app.post("/api/upload")
async def upload_video(file: UploadFile = File(...)):
    """Upload a new gaming parkour video to input/."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="Empty filename")

    clean_name = Path(file.filename).name
    dest = get_input_dir() / clean_name
    dest.parent.mkdir(parents=True, exist_ok=True)

    with open(dest, "wb") as f_out:
        shutil.copyfileobj(file.file, f_out)

    try:
        info = inspect_video(dest)
        return {
            "filename": clean_name,
            "size_mb": info.file_size_mb,
            "duration": info.duration,
            "resolution": f"{info.width}x{info.height}",
            "is_valid": info.is_valid,
        }
    except Exception as e:
        return {"filename": clean_name, "is_valid": True, "error": str(e)}


@app.post("/api/sample-video")
async def generate_sample_video():
    """Generate a procedural 35s neon parkour video clip into input/."""
    out_path = get_input_dir() / "sample_parkour.mp4"
    generate_sample_gaming_clip(output_path=out_path, duration_sec=35.0)
    info = inspect_video(out_path)
    return {
        "filename": out_path.name,
        "size_mb": info.file_size_mb,
        "duration": info.duration,
        "resolution": f"{info.width}x{info.height}",
    }


@app.get("/api/voices")
async def list_voices():
    """List configured Edge-TTS character voices."""
    return {"voices": get_available_voices()}


@app.post("/api/generate")
async def start_generation(req: GenerateRequest, background_tasks: BackgroundTasks):
    """Trigger an asynchronous video generation job."""
    video_path = get_input_dir() / req.video_filename
    if not video_path.exists():
        raise HTTPException(status_code=404, detail=f"Input video '{req.video_filename}' not found.")

    try:
        style = HumorStyle(req.humor_style.lower())
    except ValueError:
        style = HumorStyle.WHOLESOME

    job_id = uuid.uuid4().hex[:10]
    job = Job(
        id=job_id,
        input_path=str(video_path),
        humor_style=style,
    )

    with _jobs_lock:
        _jobs[job_id] = job
        _job_logs[job_id] = []

    _log_job_event(job_id, "INFO", f"Job queued: {req.video_filename} ({style.value})")

    # Launch in background worker
    def _worker():
        orchestrator = PipelineOrchestrator()

        def _progress_cb(updated_job: Job):
            with _jobs_lock:
                _jobs[job_id] = updated_job
            _log_job_event(
                job_id,
                "INFO",
                f"Stage: {updated_job.status.value} ({updated_job.progress_pct}%)",
            )

        try:
            orchestrator.run(
                input_video_path=video_path,
                humor_style=style,
                theme=req.theme,
                job_id=job_id,
                progress_callback=_progress_cb,
            )
            _log_job_event(job_id, "SUCCESS", "YouTube Short created successfully!")
        except Exception as e:
            _log_job_event(job_id, "ERROR", f"Job failed: {e}")

    background_tasks.add_task(_worker)
    return {"job_id": job_id, "status": "queued"}


@app.get("/api/jobs/{job_id}")
async def get_job_details(job_id: str):
    """Retrieve current job state, conversation, metadata, and video url."""
    with _jobs_lock:
        job = _jobs.get(job_id)
        logs = _job_logs.get(job_id, [])

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    video_rel_url = None
    thumb_rel_url = None
    if job.output_video_path and Path(job.output_video_path).exists():
        rel = Path(job.output_video_path).relative_to(get_output_dir())
        video_rel_url = f"/output/{rel.as_posix()}"
        thumb_p = Path(job.output_video_path).with_name(f"{Path(job.output_video_path).stem}_thumbnail.jpg")
        if thumb_p.exists():
            thumb_rel = thumb_p.relative_to(get_output_dir())
            thumb_rel_url = f"/output/{thumb_rel.as_posix()}"

    return {
        "job": job.model_dump(),
        "video_url": video_rel_url,
        "thumbnail_url": thumb_rel_url,
        "logs": logs[-40:],
    }


@app.get("/api/jobs/{job_id}/stream")
async def stream_job_events(job_id: str):
    """SSE endpoint for real-time progress updates and log messages."""
    async def event_generator():
        last_log_count = 0
        while True:
            with _jobs_lock:
                job = _jobs.get(job_id)
                logs = _job_logs.get(job_id, [])

            if not job:
                yield f"data: {json.dumps({'error': 'Job not found'})}\n\n"
                break

            new_logs = logs[last_log_count:]
            last_log_count = len(logs)

            video_rel_url = None
            if job.output_video_path and Path(job.output_video_path).exists():
                rel = Path(job.output_video_path).relative_to(get_output_dir())
                video_rel_url = f"/output/{rel.as_posix()}"

            data = {
                "status": job.status.value,
                "progress_pct": job.progress_pct,
                "error": job.error,
                "new_logs": new_logs,
                "video_url": video_rel_url,
                "story_title": job.conversation.story_title if job.conversation else None,
            }

            yield f"data: {json.dumps(data)}\n\n"

            if job.status in (JobStatus.COMPLETED, JobStatus.FAILED):
                break

            await asyncio.sleep(0.8)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.get("/api/library")
async def get_library():
    """List all previously generated Shorts packages from output/."""
    out_dir = get_output_dir()
    items = []

    for bundle_dir in sorted(out_dir.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
        if not bundle_dir.is_dir():
            continue

        mp4_files = list(bundle_dir.glob("*.mp4"))
        if not mp4_files:
            continue

        video_file = mp4_files[0]
        meta_file = bundle_dir / "metadata.json"
        convo_file = bundle_dir / "conversation.json"
        qa_file = bundle_dir / "quality_report.json"
        thumb_files = list(bundle_dir.glob("*_thumbnail.jpg"))

        metadata_dict = {}
        if meta_file.exists():
            try:
                metadata_dict = json.loads(meta_file.read_text(encoding="utf-8"))
            except Exception:
                pass

        convo_dict = {}
        if convo_file.exists():
            try:
                convo_dict = json.loads(convo_file.read_text(encoding="utf-8"))
            except Exception:
                pass

        qa_dict = {}
        if qa_file.exists():
            try:
                qa_dict = json.loads(qa_file.read_text(encoding="utf-8"))
            except Exception:
                pass

        rel_vid = video_file.relative_to(out_dir).as_posix()
        rel_thumb = thumb_files[0].relative_to(out_dir).as_posix() if thumb_files else None

        items.append({
            "bundle_id": bundle_dir.name,
            "title": metadata_dict.get("title", convo_dict.get("story_title", bundle_dir.name)),
            "created_at": datetime.fromtimestamp(bundle_dir.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
            "video_url": f"/output/{rel_vid}",
            "thumbnail_url": f"/output/{rel_thumb}" if rel_thumb else None,
            "duration": qa_dict.get("duration_sec", 0.0),
            "size_mb": qa_dict.get("file_size_mb", round(video_file.stat().st_size / (1024 * 1024), 2)),
            "hashtags": metadata_dict.get("hashtags", []),
            "description": metadata_dict.get("description", ""),
            "pinned_comment": metadata_dict.get("pinned_comment", ""),
        })

    return {"library": items}


@app.get("/api/download/{bundle_id}/zip")
async def download_bundle_zip(bundle_id: str):
    """Create and download a ZIP archive containing all assets for a Short."""
    bundle_dir = get_output_dir() / bundle_id
    if not bundle_dir.exists() or not bundle_dir.is_dir():
        raise HTTPException(status_code=404, detail="Bundle not found")

    zip_path = get_temp_dir() / f"{bundle_id}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in bundle_dir.iterdir():
            if f.is_file():
                zf.write(f, arcname=f.name)

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename=f"{bundle_id}_assets.zip",
    )
