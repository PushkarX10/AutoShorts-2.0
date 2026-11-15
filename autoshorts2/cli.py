"""CLI Interface for AutoShorts 2.0
"""

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from autoshorts2.pipeline import AutoShortsPipeline
from autoshorts2.config import DEFAULT_VOICE

console = Console()

@click.group()
def cli():
    """AutoShorts 2.0 - Cinematic Illustrated Story + Infographic Shorts Engine"""
    pass

@cli.command("create")
@click.argument("topic", default="US Mint $1 Coin Free Shipping Loophole")
@click.option("--voice", default=DEFAULT_VOICE, help="Neural documentary voice profile")
def create_short(topic: str, voice: str):
    """Generate a complete 1080x1920 30FPS Cinematic YouTube Short from topic to final MP4."""
    console.print(Panel.fit(
        f"[bold #FF2A85]AutoShorts 2.0 Engine[/bold #FF2A85]\n"
        f"[white]Topic:[/white] [bold cyan]{topic}[/bold cyan]\n"
        f"[white]Voice:[/white] [bold yellow]{voice}[/bold yellow]",
        border_style="#FF2A85"
    ))
    pipeline = AutoShortsPipeline(voice=voice)
    project = pipeline.run(topic)
    
    pkg = project.output_package
    if pkg:
        table = Table(title="Generated 16-Deliverable Output Package", border_style="#FF2A85")
        table.add_column("Deliverable", style="cyan", no_wrap=True)
        table.add_column("Status / Path", style="green")
        
        table.add_row("01. Title", pkg.title)
        table.add_row("02. Hook", f"\"{pkg.hook}\"")
        table.add_row("03. Script", f"{len(pkg.full_script.split())} words")
        table.add_row("04. Scene Plan", f"{len(pkg.scene_plan)} dynamic scenes")
        table.add_row("05. Character Bible", f"{pkg.character_bible.name}")
        table.add_row("06. Visual Prompts", f"{len(pkg.visual_prompts)} prompts")
        table.add_row("07. Infographic Specs", f"{len(pkg.infographic_specs)} beige data layouts")
        table.add_row("08. Voiceover Script", "Synchronized Whisper timestamps")
        table.add_row("09. Subtitle Files", ".srt and .ass (hot pink highlights)")
        table.add_row("10. Music Direction", "5-stage evolving tension score")
        table.add_row("11. SFX Timeline", f"{len(pkg.sfx_timeline)} synchronized audio cues")
        table.add_row("12. Editing Timeline", f"{len(pkg.editing_timeline)} cuts & transitions")
        table.add_row("13. Final MP4", pkg.final_mp4_path)
        table.add_row("14. Thumbnail Frame", pkg.thumbnail_path)
        table.add_row("15. YouTube Description", "Ready for upload")
        table.add_row("16. Hashtags", " ".join(pkg.hashtags))
        console.print(table)

@cli.command("studio")
@click.option("--port", default=8000, help="Port to run Studio server on")
def run_studio(port: int):
    """Launch the Interactive Web Studio dashboard."""
    import uvicorn
    from autoshorts2.studio.server import app
    console.print(f"[bold #FF2A85]Launching AutoShorts 2.0 Web Studio on http://localhost:{port}...[/bold #FF2A85]")
    uvicorn.run(app, host="0.0.0.0", port=port)

@cli.command("history")
@click.argument("topic", default="Caesar's Impossible Double Wall at Alesia")
@click.option("--voice", default="en-US-ChristopherNeural", help="Documentary neural voice")
def create_history(topic: str, voice: str):
    """Generate a complete 1080x1920 30FPS Historical Facts Documentary Short (Restrained SFX)."""
    from autoshorts2.history.pipeline import HistoryShortsPipeline
    console.print(Panel.fit(
        f"[bold #FF2A85]AutoShorts 2.0 - AI History Facts Generator[/bold #FF2A85]\n"
        f"[white]Topic:[/white] [bold cyan]{topic}[/bold cyan]\n"
        f"[white]Voice:[/white] [bold yellow]{voice}[/bold yellow]\n"
        f"[white]Sound Design:[/white] [bold green]Restrained (3 Motivated Cues)[/bold green]",
        border_style="#FF2A85"
    ))
    pipeline = HistoryShortsPipeline(voice=voice)
    project = pipeline.run(topic)
    
    pkg = project.output_package
    if pkg:
        table = Table(title="Generated 17-Deliverable Historical Output Package", border_style="#FF2A85")
        table.add_column("Deliverable", style="cyan", no_wrap=True)
        table.add_column("Details / Status", style="green")
        
        table.add_row("01. Title", pkg.title)
        table.add_row("02. Hook", f"\"{pkg.hook}\"")
        table.add_row("03. Historical Fact Sheet", f"{len(pkg.historical_fact_sheet.verified_claims)} verified claims")
        table.add_row("04. Full Script", f"{len(pkg.full_script.split())} words")
        table.add_row("05. Scene Plan", f"{len(pkg.scene_plan)} dynamic scenes")
        table.add_row("06. Visual Prompts", f"{len(pkg.historical_visual_prompts)} prompts")
        table.add_row("07. Map Specifications", "Contravallation (11mi) & Circumvallation (14mi)")
        table.add_row("08. Timeline Specs", f"{len(pkg.timeline_specifications.get('events', []))} historical milestones")
        table.add_row("09. Infographic Specs", "Warm beige troop comparison ratio")
        table.add_row("10. Voiceover Script", "Synchronized Whisper timestamps")
        table.add_row("11. Subtitle Files", ".srt & .ass (electric magenta highlights)")
        table.add_row("12. Music Direction", pkg.music_direction.get("track", "cinematic_tension_score.wav"))
        table.add_row("13. SFX Timeline", f"{len(pkg.sfx_timeline)} restrained cues (horn, digging, clash)")
        table.add_row("14. Editing Timeline", f"{len(pkg.editing_timeline)} dynamic scenes")
        table.add_row("15. Final Video", pkg.final_video_path)
        table.add_row("16. Thumbnail", pkg.thumbnail_path)
        table.add_row("17. Description & Hashtags", " ".join(pkg.hashtags))
        console.print(table)

@cli.command("light")
@click.argument("topic", default="The Spotlight Effect: Why Nobody Cares as Much as You Think")
@click.option("--voice", default="en-US-BrianMultilingualNeural", help="Clean explainer voice profile")
def create_light(topic: str, voice: str):
    """Generate a clean 1080x1920 30FPS Light Minimalist Explainer Short (AutoShorts 3.0 style, 0 SFX)."""
    from autoshorts2.light.pipeline import LightShortsPipeline
    console.print(Panel.fit(
        f"[bold #F59E0B]AutoShorts 2.0 - Light Minimalist Explainer Engine[/bold #F59E0B]\n"
        f"[white]Inspiration:[/white] [bold cyan]AutoShorts 3.0 / Zenn / MinutePhysics[/bold cyan]\n"
        f"[white]Canvas:[/white] [bold white]Pure White (#FFFFFF) / Minimal Line Art[/bold white]\n"
        f"[white]Topic:[/white] [bold yellow]{topic}[/bold yellow]\n"
        f"[white]SFX Count:[/white] [bold green]0 SFX (Clean VO + Sidechain Ducked Upright Bass BGM)[/bold green]",
        border_style="#F59E0B"
    ))
    pipeline = LightShortsPipeline(voice=voice)
    project = pipeline.run(topic)
    
    pkg = project.output_package
    if pkg:
        table = Table(title="Generated AutoShorts 3.0-Style Light Explainer Package", border_style="#F59E0B")
        table.add_column("Deliverable", style="cyan", no_wrap=True)
        table.add_column("Details / Status", style="green")
        
        table.add_row("01. Theme", "Pure White #FFFFFF, 4.5px stroke, gold #F5C518 accents")
        table.add_row("02. Character", "Minimal modular stick figure (gentle breathing + blink)")
        table.add_row("03. Title", pkg.title)
        table.add_row("04. Hook", f"\"{pkg.hook}\"")
        table.add_row("05. Full Script", f"{len(pkg.full_script.split())} words")
        table.add_row("06. Scenes", f"{len(pkg.scenes)} minimal metaphor scenes")
        table.add_row("07. SFX Count", "0 SFX (Zero audio clutter)")
        table.add_row("08. Music", "Quirky upright bass (ducked to -20dB during narration)")
        table.add_row("09. Captions", "Kinetic safe-zone captions (Y: 340px)")
        table.add_row("10. Final Video", pkg.final_video_path)
        table.add_row("11. Thumbnail", pkg.thumbnail_path)
        console.print(table)

@cli.command("history_light")
@click.argument("topic", default="Caesar's Impossible Double Wall at Alesia")
@click.option("--voice", default="en-US-BrianMultilingualNeural", help="Clean documentary voice")
@click.option("--upload", is_flag=True, default=False, help="Automatically upload to YouTube Shorts after rendering")
@click.option("--privacy", default="unlisted", type=click.Choice(["private", "unlisted", "public"]), help="YouTube privacy status")
def create_history_light(topic: str, voice: str, upload: bool, privacy: str):
    """Generate a clean 1080x1920 30FPS Light Minimalist History Facts Short (0 SFX)."""
    from autoshorts2.light.history_pipeline import HistoryLightShortsPipeline
    console.print(Panel.fit(
        f"[bold #EF4444]AutoShorts 2.0 - Light History Facts Engine[/bold #EF4444]\n"
        f"[white]Style:[/white] [bold cyan]AutoShorts 3.0 Light Theme / Pure White Canvas[/bold cyan]\n"
        f"[white]Topic:[/white] [bold yellow]{topic}[/bold yellow]\n"
        f"[white]SFX Count:[/white] [bold green]0 SFX (Clean Narration + Ducked Upright Bass BGM)[/bold green]\n"
        f"[white]Auto Upload:[/white] [bold yellow]{'Enabled (' + privacy + ')' if upload else 'Disabled'}[/bold yellow]",
        border_style="#EF4444"
    ))
    pipeline = HistoryLightShortsPipeline(voice=voice)
    pkg = pipeline.run(topic)
    
    if pkg:
        table = Table(title="Generated 17-Deliverable Light History Facts Package", border_style="#EF4444")
        table.add_column("Deliverable", style="cyan", no_wrap=True)
        table.add_column("Details / Status", style="green")
        
        table.add_row("01. Title", pkg["title"])
        table.add_row("02. Hook", f"\"{pkg['hook']}\"")
        table.add_row("03. Historical Fact Sheet", f"{len(pkg['historical_fact_sheet']['verified_claims'])} verified claims")
        table.add_row("04. Full Script", f"{len(pkg['full_script'].split())} words")
        table.add_row("05. Scene-by-Scene Plan", f"{len(pkg['scene_by_scene_plan'])} minimal diagram scenes")
        table.add_row("06. Visual Prompts", f"{len(pkg['historical_visual_prompts'])} prompts")
        table.add_row("07. Map Specs", pkg['map_specifications']['type'])
        table.add_row("08. Timeline Specs", f"{len(pkg['timeline_specifications'])} milestones")
        table.add_row("09. Infographic Specs", pkg['infographic_specifications']['ratio'])
        table.add_row("10. Voiceover Script", f"{pkg['voiceover_script']['duration_seconds']}s ({pkg['voiceover_script']['words_count']} words)")
        table.add_row("11. Subtitle File", pkg['subtitle_file']['format'])
        table.add_row("12. Music Direction", pkg['music_direction']['track'])
        table.add_row("13. SFX Timeline", "0 SFX (Zero audio clutter)")
        table.add_row("14. Editing Timeline", f"{len(pkg['editing_timeline'])} scenes")
        table.add_row("15. Final Video", pkg['final_video_path'])
        table.add_row("16. Thumbnail", pkg['thumbnail_path'])
        table.add_row("17. Description & Hashtags", " ".join(pkg['hashtags']))
        console.print(table)

        if upload:
            from autoshorts2.uploader.youtube_uploader import YouTubeUploader
            console.print(f"\n[bold #FF2A85]Uploading to YouTube Shorts ({privacy})...[/bold #FF2A85]")
            uploader = YouTubeUploader()
            res = uploader.upload_short(
                video_path=pkg["final_video_path"],
                title=pkg["title"],
                description=pkg["description"],
                tags=pkg["hashtags"],
                privacy_status=privacy,
                thumbnail_path=pkg["thumbnail_path"]
            )
            console.print(f"[bold green]SUCCESS: Video published at: {res['video_url']}[/bold green]")

if __name__ == "__main__":
    cli()
