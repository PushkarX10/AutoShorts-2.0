"""
AutoShorts 2.0 — YouTube Metadata Generator.

Uses the local LLM to generate title, description, hashtags, and more
for each finished Short.
"""
from __future__ import annotations

import json
import re
import time

import httpx
from rich.console import Console

from src.config.settings import get
from src.models.schemas import Conversation, YouTubeMetadata

console = Console()


def generate_metadata(conversation: Conversation) -> YouTubeMetadata:
    """
    Generate YouTube-optimized metadata for a finished Short.
    Falls back to rule-based generation if LLM fails.
    """
    console.print("[cyan]⏳[/cyan] Generating YouTube metadata…")

    try:
        metadata = _generate_with_llm(conversation)
        console.print(f"[green]✓[/green] Metadata generated: [bold]{metadata.title}[/bold]")
        return metadata
    except Exception as e:
        console.print(f"[yellow]⚠[/yellow] LLM metadata failed ({e}), using fallback")
        return _fallback_metadata(conversation)


def _generate_with_llm(conversation: Conversation) -> YouTubeMetadata:
    """Use the LLM to create optimized metadata."""
    cfg = get("llm")
    base_url = cfg.get("base_url", "http://localhost:11434")
    model = cfg.get("model", "llama3.1:latest")

    # Summarize the conversation for the LLM
    dialog_summary = " | ".join(
        f"{conversation.get_character(m.character_id).name if conversation.get_character(m.character_id) else m.character_id}: {m.text}"
        for m in conversation.messages[:6]
    )

    prompt = f"""Generate YouTube Shorts metadata for a funny texting story video.

Story title: {conversation.story_title}
Theme: {conversation.theme}
Dialog preview: {dialog_summary}...

Return ONLY valid JSON with this structure:
{{
  "title": "Short catchy title under 60 chars that creates curiosity",
  "description": "2-3 sentence description, engaging, with a call to action",
  "hashtags": ["#Shorts", "#FunnyTexts", "plus 3-5 more relevant tags"],
  "suggested_filename": "lowercase_snake_case_filename",
  "pinned_comment": "A funny or engaging pinned comment suggestion"
}}

Make the title click-worthy but NOT misleading. No excessive caps or emoji spam."""

    url = f"{base_url}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.7, "num_predict": 512},
    }

    response = httpx.post(url, json=payload, timeout=60)
    response.raise_for_status()
    raw = response.json().get("response", "")
    raw = raw.strip()

    # Remove code fences
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

    data = json.loads(raw)

    # Ensure required hashtags
    hashtags = data.get("hashtags", [])
    if "#Shorts" not in hashtags:
        hashtags.insert(0, "#Shorts")
    # Limit hashtags
    hashtags = hashtags[:8]

    return YouTubeMetadata(
        title=data.get("title", conversation.story_title)[:100],
        description=data.get("description", "")[:5000],
        hashtags=hashtags,
        suggested_filename=data.get("suggested_filename", _slugify(conversation.story_title)),
        pinned_comment=data.get("pinned_comment", ""),
    )


def _fallback_metadata(conversation: Conversation) -> YouTubeMetadata:
    """Rule-based metadata when LLM is unavailable."""
    title = conversation.story_title
    if len(title) > 60:
        title = title[:57] + "..."

    char_names = [c.name for c in conversation.characters]
    names_str = " & ".join(char_names)

    description = (
        f"😂 {title}\n\n"
        f"Watch {names_str} in this hilarious texting conversation!\n\n"
        f"Like & subscribe for more funny chat stories! 📱\n\n"
        f"#Shorts #FunnyTexts #TextingStory"
    )

    hashtags = [
        "#Shorts", "#FunnyTexts", "#TextingStory",
        "#FunnyChat", "#Comedy", "#Viral",
    ]

    return YouTubeMetadata(
        title=title,
        description=description,
        hashtags=hashtags,
        suggested_filename=_slugify(title),
        pinned_comment=f"Who else would react like {char_names[-1] if char_names else 'this'}? 😂",
    )


def _slugify(text: str) -> str:
    """Convert text to a safe filename slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "_", text)
    return text[:50]
