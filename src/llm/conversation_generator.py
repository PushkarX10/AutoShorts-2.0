"""
AutoShorts 2.0 — LLM Conversation Generator.

Uses Ollama to generate original, funny chat conversations
with structured JSON output and automatic retries.
"""
from __future__ import annotations

import json
import random
import re
import time
from typing import Any

import httpx
from rich.console import Console

from src.config.settings import get, get_available_voices
from src.models.schemas import (
    BubbleStyle, Character, Conversation, DeliverySpeed,
    Emotion, Ending, EndingType, HumorStyle, Message,
)

console = Console()

# ── Comedy themes to rotate through ──────────────────────────────────────

THEMES = [
    "autocorrect_disaster",
    "funny_misunderstanding",
    "sibling_argument",
    "parent_vs_slang",
    "delivery_gone_wrong",
    "gaming_miscommunication",
    "school_group_chat",
    "friend_zone_moment",
    "cooking_catastrophe",
    "unexpected_shopping",
    "pet_chaos",
    "roommate_problems",
    "tech_support_confusion",
    "gym_misunderstanding",
    "vacation_planning_disaster",
]

HUMOR_DESCRIPTIONS = {
    HumorStyle.WHOLESOME: "light-hearted, family-friendly humor with warmth. No meanness.",
    HumorStyle.SARCASTIC: "witty, dry, sarcastic banter. Characters tease each other playfully.",
    HumorStyle.CHAOTIC: "absurd escalation, random tangents, chaotic energy. Things go off the rails.",
    HumorStyle.AWKWARD: "cringe-worthy, uncomfortable, socially awkward situations.",
    HumorStyle.DARK: "dark but non-graphic humor. Unexpected dark twists, gallows humor, nothing offensive.",
}


def generate_conversation(
    humor_style: HumorStyle = HumorStyle.WHOLESOME,
    num_characters: int = 2,
    min_messages: int = 10,
    max_messages: int = 18,
) -> Conversation:
    """
    Generate a complete funny chat conversation using the local LLM.

    Retries on invalid JSON or quality issues up to max_retries.
    """
    llm_cfg = get("llm")
    max_retries = llm_cfg.get("max_retries", 3)
    theme = random.choice(THEMES)

    console.print(f"[cyan]⏳[/cyan] Generating conversation — theme: [bold]{theme}[/bold], style: {humor_style.value}")

    last_error = ""
    for attempt in range(1, max_retries + 1):
        try:
            prompt = _build_prompt(humor_style, theme, num_characters, min_messages, max_messages, last_error)
            raw_json = _call_ollama(prompt)
            conversation = _parse_response(raw_json, num_characters)

            console.print(
                f"[green]✓[/green] Generated: [bold]{conversation.story_title}[/bold] "
                f"({len(conversation.messages)} messages, {len(conversation.characters)} characters)"
            )
            return conversation

        except Exception as e:
            last_error = str(e)
            console.print(f"[yellow]⚠[/yellow] Attempt {attempt}/{max_retries} failed: {last_error}")
            if attempt < max_retries:
                time.sleep(llm_cfg.get("retry_delay", 2))

    raise RuntimeError(f"Failed to generate conversation after {max_retries} attempts. Last error: {last_error}")


def _build_prompt(
    humor_style: HumorStyle,
    theme: str,
    num_characters: int,
    min_messages: int,
    max_messages: int,
    previous_error: str = "",
) -> str:
    """Build the LLM prompt for conversation generation."""

    voices = get_available_voices()
    voice_keys = list(voices.keys())
    # Pick voice assignments for characters
    female_voices = [k for k in voice_keys if "female" in k]
    male_voices = [k for k in voice_keys if "male" in k]

    humor_desc = HUMOR_DESCRIPTIONS.get(humor_style, HUMOR_DESCRIPTIONS[HumorStyle.WHOLESOME])

    error_note = ""
    if previous_error:
        error_note = f"""
IMPORTANT: Your previous response had this error: {previous_error}
Fix this issue in your new response. Make sure to return ONLY valid JSON.
"""

    prompt = f"""You are a comedy writer for viral YouTube Shorts. Generate a BRAND NEW, ORIGINAL funny text message conversation.

THEME: {theme.replace("_", " ")}
HUMOR STYLE: {humor_style.value} — {humor_desc}
CHARACTERS: {num_characters} people
MESSAGES: {min_messages} to {max_messages} messages total

RULES:
- Create a realistic texting conversation between friends/family/coworkers.
- Start with a natural opening message (not "hey" by itself).
- Build a misunderstanding, autocorrect disaster, or escalating situation.
- Keep each message SHORT and PUNCHY — 1 sentence, under 12 words max. Like real fast texting.
- The total conversation should be snappy and read in under 35-40 seconds.
- Build comedic tension with each reply.
- End with a STRONG punchline or hilarious reaction.
- Make it feel like real people texting, not AI writing.
- NO emojis overload. Max 1-2 emojis per message if any.
- NO offensive, political, or religious content.
- All characters and situations must be FICTIONAL.
- Every message must be different — no repeating the same joke.
- DO NOT use the "blueberry/balloon" example. Be ORIGINAL.
{error_note}
Return ONLY a valid JSON object with this EXACT structure (no markdown, no commentary):

{{
  "story_title": "Short catchy title",
  "theme": "{theme}",
  "characters": [
    {{
      "id": "person_a",
      "name": "A first name",
      "personality": "brief personality in 3-5 words",
      "voice_id": "{female_voices[0] if female_voices else voice_keys[0]}",
      "bubble_style": "incoming"
    }},
    {{
      "id": "person_b",
      "name": "A different first name",
      "personality": "brief personality in 3-5 words",
      "voice_id": "{male_voices[0] if male_voices else voice_keys[-1]}",
      "bubble_style": "outgoing"
    }}
  ],
  "messages": [
    {{
      "id": 1,
      "character_id": "person_a",
      "text": "First message text",
      "emotion": "casual",
      "delivery": "normal",
      "pause_after_ms": 350,
      "is_punchline": false
    }}
  ],
  "ending": {{
    "type": "punchline",
    "text": "The final punchline message text"
  }}
}}

Valid emotions: casual, confused, excited, sarcastic, embarrassed, angry, laughing, shocked, nervous, proud
Valid delivery: slow, normal, fast

Mark the last 1-2 messages with "is_punchline": true.
Set pause_after_ms to 700 right before the punchline for dramatic pause.
Generate exactly {random.randint(min_messages, max_messages)} messages.

RESPOND WITH ONLY THE JSON OBJECT. NO OTHER TEXT."""

    return prompt


def _call_ollama(prompt: str) -> str:
    """Call the Ollama API and return the raw response text."""
    cfg = get("llm")
    base_url = cfg.get("base_url", "http://localhost:11434")
    model = cfg.get("model", "llama3.1:latest")
    temperature = cfg.get("temperature", 0.85)
    timeout = cfg.get("timeout", 240)

    url = f"{base_url}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": temperature,
            "num_predict": 1024,
        },
    }

    try:
        response = httpx.post(url, json=payload, timeout=timeout)
        response.raise_for_status()
    except httpx.ConnectError:
        raise RuntimeError(
            "Cannot connect to Ollama. Ensure Ollama is running: ollama serve"
        )
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"Ollama HTTP error {e.response.status_code}: {e.response.text[:500]}")

    data = response.json()
    return data.get("response", "")


def _parse_response(raw: str, expected_chars: int) -> Conversation:
    """Parse and validate the LLM JSON response into a Conversation."""
    # Try to extract JSON from the response
    raw = raw.strip()

    # Remove markdown code fences if present
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        # Try to find JSON object in the response
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group())
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON in LLM response: {e}. Raw start: {raw[:200]}")
        else:
            raise ValueError(f"No JSON found in LLM response. Raw start: {raw[:200]}")

    # Normalize and fix common issues
    data = _fix_data(data, expected_chars)

    # Parse into Pydantic model
    conversation = Conversation.model_validate(data)

    # Validate character references
    errors = conversation.validate_character_refs()
    if errors:
        raise ValueError(f"Character reference errors: {'; '.join(errors)}")

    # Validate message count
    if len(conversation.messages) < 4:
        raise ValueError(f"Too few messages: {len(conversation.messages)} (need at least 4)")

    return conversation


def _fix_data(data: dict, expected_chars: int) -> dict:
    """Fix common LLM output issues."""
    # Ensure characters exist
    if "characters" not in data or not data["characters"]:
        data["characters"] = _default_characters(expected_chars)

    # Assign bubble styles
    for i, char in enumerate(data.get("characters", [])):
        if "bubble_style" not in char:
            char["bubble_style"] = "incoming" if i == 0 else "outgoing"
        if "voice_id" not in char:
            voices = list(get_available_voices().keys())
            char["voice_id"] = voices[i % len(voices)] if voices else "female_01"
        char.setdefault("avatar_color_idx", i)

    # Fix messages
    messages = data.get("messages", [])
    char_ids = {c["id"] for c in data.get("characters", [])}

    for i, msg in enumerate(messages):
        msg["id"] = i + 1
        # Fix invalid character references
        if msg.get("character_id") not in char_ids:
            chars = list(char_ids)
            msg["character_id"] = chars[i % len(chars)]
        # Clamp pause
        msg.setdefault("pause_after_ms", 350)
        msg["pause_after_ms"] = max(200, min(3000, msg["pause_after_ms"]))
        # Fix emotion
        valid_emotions = {e.value for e in Emotion}
        if msg.get("emotion", "casual") not in valid_emotions:
            msg["emotion"] = "casual"
        # Fix delivery
        valid_deliveries = {d.value for d in DeliverySpeed}
        if msg.get("delivery", "normal") not in valid_deliveries:
            msg["delivery"] = "normal"
        # Default punchline flag
        msg.setdefault("is_punchline", False)

    # Ensure at least the last message is marked as punchline
    if messages and not any(m.get("is_punchline") for m in messages):
        messages[-1]["is_punchline"] = True

    # Fix ending
    data.setdefault("ending", {"type": "punchline", "text": ""})
    if not data["ending"].get("text") and messages:
        data["ending"]["text"] = messages[-1].get("text", "")

    data.setdefault("story_title", "Untitled Chat")
    data.setdefault("theme", "miscellaneous")

    return data


def _default_characters(count: int) -> list[dict]:
    """Generate default characters if the LLM didn't provide them."""
    voices = list(get_available_voices().keys())
    names = ["Alex", "Jordan", "Sam", "Taylor", "Morgan"]
    defaults = []
    for i in range(min(count, 3)):
        defaults.append({
            "id": f"person_{'abcde'[i]}",
            "name": names[i],
            "personality": "friendly and clueless",
            "voice_id": voices[i % len(voices)] if voices else "female_01",
            "bubble_style": "incoming" if i == 0 else "outgoing",
            "avatar_color_idx": i,
        })
    return defaults
