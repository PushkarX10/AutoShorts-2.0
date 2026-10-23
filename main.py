"""
AutoShorts 2.0 — Local AI YouTube Shorts Automation Factory.

Command-Line Interface and Service Launcher.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config.settings import get, get_available_voices, get_input_dir, get_output_dir
from src.models.schemas import HumorStyle

console = Console(legacy_windows=False)


def cmd_check_env(args):
    """Check and display local environment readiness."""
    import shutil
    import subprocess
    import httpx

    table = Table(title="AutoShorts 2.0 — System Environment Status", show_header=True, header_style="bold cyan")
    table.add_column("Component", style="bold")
    table.add_column("Status")
    table.add_column("Details")

    # Python
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    table.add_row("Python", "[green]Ready[/green]", f"{py_ver} ({sys.executable})")

    # FFmpeg
    ffmpeg_bin = shutil.which("ffmpeg")
    if ffmpeg_bin:
        try:
            res = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, timeout=5)
            first_line = res.stdout.splitlines()[0] if res.stdout else "Available"
            table.add_row("FFmpeg", "[green]Ready[/green]", first_line[:60])
        except Exception:
            table.add_row("FFmpeg", "[green]Ready[/green]", ffmpeg_bin)
    else:
        table.add_row("FFmpeg", "[red]Missing[/red]", "ffmpeg not found in PATH")

    # Ollama
    ollama_url = get("llm", "base_url", "http://localhost:11434")
    model_name = get("llm", "model", "llama3.1:latest")
    try:
        resp = httpx.get(f"{ollama_url}/api/tags", timeout=3)
        if resp.status_code == 200:
            models = [m.get("name") for m in resp.json().get("models", [])]
            if any(model_name in m for m in models):
                table.add_row("Ollama LLM", "[green]Ready[/green]", f"{model_name} loaded at {ollama_url}")
            else:
                table.add_row("Ollama LLM", "[yellow]Warning[/yellow]", f"Running, but {model_name} not found in {models}")
        else:
            table.add_row("Ollama LLM", "[red]Error[/red]", f"Returned HTTP {resp.status_code}")
    except Exception as e:
        table.add_row("Ollama LLM", "[red]Offline[/red]", f"Cannot connect to {ollama_url} ({e})")

    # Edge-TTS
    try:
        import edge_tts
        table.add_row("Edge-TTS", "[green]Ready[/green]", f"Version {getattr(edge_tts, '__version__', 'Installed')}")
    except ImportError:
        table.add_row("Edge-TTS", "[red]Missing[/red]", "Package edge-tts not installed")

    # Output Dir
    out_dir = get_output_dir()
    table.add_row("Output Directory", "[green]Ready[/green]", str(out_dir))

    console.print(table)


def cmd_voices(args):
    """List available Edge-TTS voices."""
    voices = get_available_voices()
    table = Table(title="Configured Character Voices", show_header=True, header_style="bold magenta")
    table.add_column("Voice Key", style="bold cyan")
    table.add_column("Azure Voice ID")
    table.add_column("Description")
    table.add_column("Rate")
    table.add_column("Pitch")

    for k, v in voices.items():
        table.add_row(
            k,
            v.get("id", ""),
            v.get("label", ""),
            v.get("rate", "+0%"),
            v.get("pitch", "+0Hz"),
        )
    console.print(table)


def cmd_sample_video(args):
    """Generate a synthetic 9:16 parkour clip."""
    from src.video.sample_generator import generate_sample_gaming_clip
    out = generate_sample_gaming_clip(duration_sec=args.duration)
    console.print(f"[bold green]✓ Sample video saved to:[/bold green] {out}")


def cmd_inspect(args):
    """Inspect a video clip."""
    from src.ingestion.video_inspector import inspect_video
    info = inspect_video(args.path)

    table = Table(title=f"Video Analysis: {info.filename}", show_header=True, header_style="bold green")
    table.add_column("Property")
    table.add_column("Value")

    table.add_row("Resolution", f"{info.width}x{info.height}")
    table.add_row("Orientation", info.orientation)
    table.add_row("Duration", f"{info.duration:.2f} seconds")
    table.add_row("FPS", f"{info.fps:.2f}")
    table.add_row("Video Codec", info.codec)
    table.add_row("Audio Track", "Yes" if info.has_audio else "No (Muted)")
    table.add_row("File Size", f"{info.file_size_mb:.2f} MB")
    table.add_row("Status", "[green]Valid[/green]" if info.is_valid else f"[red]Invalid: {info.error}[/red]")

    console.print(table)


def cmd_generate(args):
    """Generate a YouTube Short from a video clip."""
    from src.pipeline.orchestrator import PipelineOrchestrator

    input_path = Path(args.video)
    if not input_path.exists():
        # Check input directory
        candidate = get_input_dir() / args.video
        if candidate.exists():
            input_path = candidate
        else:
            console.print(f"[bold red]Error:[/bold red] Video file '{args.video}' not found.")
            sys.exit(1)

    style = HumorStyle(args.style)
    orchestrator = PipelineOrchestrator()

    custom_convo = None
    if getattr(args, "script", None):
        script_arg = args.script
        script_path = Path(script_arg)
        if script_path.exists() and script_path.is_file():
            raw_text = script_path.read_text(encoding="utf-8")
        else:
            raw_text = script_arg
        from src.llm.custom_convo_parser import parse_custom_conversation
        custom_convo = parse_custom_conversation(raw_text)

    panel_text = (
        f"[bold]Input Video:[/bold] {input_path.name}\n"
        f"[bold]Comedy Style:[/bold] {style.value.upper()}\n"
        f"[bold]Custom Script:[/bold] {'Yes (' + custom_convo.story_title + ')' if custom_convo else 'None (AI Generated)'}\n"
        f"[bold]Custom Theme:[/bold] {args.theme or 'Auto (Random AI Theme)'}"
    )

    console.print(Panel(
        panel_text,
        title="[bold cyan]AutoShorts 2.0 — Generation Task[/bold cyan]",
        border_style="cyan",
    ))

    job = orchestrator.run(
        input_video_path=input_path,
        conversation=custom_convo,
        humor_style=style,
        theme=args.theme,
        job_id=getattr(args, "job_id", None),
    )

    console.print("\n[bold green]Short generation completed successfully![/bold green]")
    console.print(f"Output: {job.output_video_path}\n")


def cmd_dashboard(args):
    """Launch the Web Dashboard."""
    import uvicorn
    console.print(f"[bold cyan]Launching AutoShorts 2.0 Web Dashboard on port {args.port}…[/bold cyan]")
    console.print(f"[green]Open in browser: http://localhost:{args.port}[/green]\n")
    uvicorn.run("src.dashboard.app:app", host="0.0.0.0", port=args.port, reload=args.reload)


def main():
    parser = argparse.ArgumentParser(
        description="AutoShorts 2.0 — Local AI YouTube Shorts Automation Factory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # generate
    gen_parser = subparsers.add_parser("generate", help="Generate a YouTube Short")
    gen_parser.add_argument("video", help="Path or filename of the gaming parkour video")
    gen_parser.add_argument(
        "--style",
        choices=["wholesome", "sarcastic", "chaotic", "awkward", "dark"],
        default="wholesome",
        help="Humor style (default: wholesome)",
    )
    gen_parser.add_argument("--theme", help="Optional specific theme or prompt")
    gen_parser.add_argument("--script", help="Path to custom chat conversation script file (.txt, .json) or inline text")
    gen_parser.add_argument("--job-id", help="Optional job ID to resume or specify temp directory")
    gen_parser.set_defaults(func=cmd_generate)

    # dashboard
    dash_parser = subparsers.add_parser("dashboard", help="Start the Web Dashboard Studio")
    dash_parser.add_argument("--port", type=int, default=8000, help="Port to listen on (default: 8000)")
    dash_parser.add_argument("--reload", action="store_true", help="Enable live code reload")
    dash_parser.set_defaults(func=cmd_dashboard)

    # sample-video
    sample_parser = subparsers.add_parser("sample-video", help="Generate a synthetic 9:16 parkour clip")
    sample_parser.add_argument("--duration", type=float, default=35.0, help="Duration in seconds (default: 35.0)")
    sample_parser.set_defaults(func=cmd_sample_video)

    # inspect
    inspect_parser = subparsers.add_parser("inspect", help="Inspect a video file")
    inspect_parser.add_argument("path", help="Path to video file")
    inspect_parser.set_defaults(func=cmd_inspect)

    # voices
    voice_parser = subparsers.add_parser("voices", help="List configured TTS voices")
    voice_parser.set_defaults(func=cmd_voices)

    # check-env
    env_parser = subparsers.add_parser("check-env", help="Check local environment & prerequisites")
    env_parser.set_defaults(func=cmd_check_env)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
