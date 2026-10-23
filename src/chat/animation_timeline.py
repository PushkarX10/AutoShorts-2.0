"""
AutoShorts 2.0 — Animation Timeline Builder.

Calculates frame-accurate timing for every message:
  • When the typing indicator appears
  • When the message bubble animates in
  • When the voice plays
  • When the next message can start
  • Total video duration
"""
from __future__ import annotations

from rich.console import Console

from src.config.settings import get
from src.models.schemas import (
    AudioManifest, Conversation, Timeline, TimelineEvent,
)

console = Console()


def build_timeline(
    conversation: Conversation,
    audio_manifest: AudioManifest,
    fps: int = 30,
) -> Timeline:
    """
    Build a frame-accurate timeline from the conversation and audio manifest.

    Each message gets:
      typing_start   → typing indicator appears
      typing_end     → typing indicator disappears / bubble appears
      bubble_appear  → message bubble animates in
      voice_start    → voice audio begins playing
      voice_end      → voice audio ends
      display_end    → message stays visible (voice_end + read buffer)
    """
    audio_cfg = get("audio", default={})
    chat_cfg = get("chat", default={})

    pause_between = audio_cfg.get("pause_between_messages_ms", 350) / 1000.0
    pause_punchline = audio_cfg.get("pause_before_punchline_ms", 700) / 1000.0
    pause_after_punch = audio_cfg.get("pause_after_punchline_ms", 1200) / 1000.0
    typing_dur = chat_cfg.get("typing_indicator_duration_ms", 700) / 1000.0
    appear_dur = chat_cfg.get("message_appear_duration_ms", 250) / 1000.0

    events: list[TimelineEvent] = []
    current_time = 0.5  # Small initial delay before first message

    for msg in conversation.messages:
        clip = audio_manifest.get_clip(msg.id)
        voice_duration = clip.duration_sec if clip else 1.0

        # Add extra pause before punchline
        if msg.is_punchline and events:
            current_time += pause_punchline

        # Typing indicator
        typing_start = current_time
        typing_end = typing_start + typing_dur

        # Bubble appears right after typing
        bubble_appear = typing_end

        # Voice starts slightly after bubble appears (let it pop in first)
        voice_start = bubble_appear + 0.1
        voice_end = voice_start + voice_duration

        # Message stays visible until voice ends + small buffer
        read_buffer = 0.15
        display_end = voice_end + read_buffer

        # Extra hold after punchline
        if msg.is_punchline:
            display_end += pause_after_punch

        events.append(TimelineEvent(
            message_id=msg.id,
            character_id=msg.character_id,
            text=msg.text,
            typing_start_sec=round(typing_start, 3),
            typing_end_sec=round(typing_end, 3),
            bubble_appear_sec=round(bubble_appear, 3),
            voice_start_sec=round(voice_start, 3),
            voice_end_sec=round(voice_end, 3),
            display_end_sec=round(display_end, 3),
            is_punchline=msg.is_punchline,
        ))

        # Next message starts after display + pause
        current_time = display_end + pause_between

    # Automatic duration compaction to guarantee YouTube Shorts compliance (< 59s)
    if events and (events[-1].display_end_sec + 0.5) > 58.5:
        console.print("[yellow]ℹ[/yellow] Timeline exceeds 58.5s; auto-compacting pacing to stay within YouTube Shorts limit…")
        typing_dur = max(0.25, typing_dur * 0.5)
        pause_between = max(0.12, pause_between * 0.4)
        pause_punchline = max(0.3, pause_punchline * 0.5)
        pause_after_punch = max(0.5, pause_after_punch * 0.5)

        events = []
        current_time = 0.25
        for msg in conversation.messages:
            clip = audio_manifest.get_clip(msg.id)
            voice_duration = clip.duration_sec if clip else 1.0

            if msg.is_punchline and events:
                current_time += pause_punchline

            typing_start = current_time
            typing_end = typing_start + typing_dur
            bubble_appear = typing_end
            voice_start = bubble_appear + 0.05
            voice_end = voice_start + voice_duration
            read_buffer = 0.08
            display_end = voice_end + read_buffer

            if msg.is_punchline:
                display_end += pause_after_punch

            events.append(TimelineEvent(
                message_id=msg.id,
                character_id=msg.character_id,
                text=msg.text,
                typing_start_sec=round(typing_start, 3),
                typing_end_sec=round(typing_end, 3),
                bubble_appear_sec=round(bubble_appear, 3),
                voice_start_sec=round(voice_start, 3),
                voice_end_sec=round(voice_end, 3),
                display_end_sec=round(display_end, 3),
                is_punchline=msg.is_punchline,
            ))
            current_time = display_end + pause_between

    # Total duration: last event's display_end + final buffer
    total_duration = events[-1].display_end_sec + 0.4 if events else 5.0
    total_frames = int(total_duration * fps)

    timeline = Timeline(
        events=events,
        total_duration_sec=round(total_duration, 3),
        total_frames=total_frames,
        fps=fps,
    )

    console.print(f"[green]✓[/green] Timeline built: {total_duration:.1f}s, "
                  f"{total_frames} frames, {len(events)} events")

    return timeline


def get_visible_messages_at(timeline: Timeline, time_sec: float) -> list[TimelineEvent]:
    """Return all messages that should be visible at a given time."""
    visible = []
    for event in timeline.events:
        if event.bubble_appear_sec <= time_sec:
            visible.append(event)
    return visible


def get_active_typing_at(timeline: Timeline, time_sec: float) -> TimelineEvent | None:
    """Return the message whose typing indicator should be visible at time_sec."""
    for event in timeline.events:
        if event.typing_start_sec <= time_sec < event.typing_end_sec:
            return event
    return None


def get_speaking_message_at(timeline: Timeline, time_sec: float) -> TimelineEvent | None:
    """Return the message being spoken at time_sec."""
    for event in timeline.events:
        if event.voice_start_sec <= time_sec < event.voice_end_sec:
            return event
    return None
