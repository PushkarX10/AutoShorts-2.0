"""
AutoShorts 2.0 — Custom Conversation Parser.

Allows users to provide their own chat conversations either as:
  • Plain text script (e.g., "Alice: Hey", "Bob (shocked): What?!")
  • JSON format matching the Conversation schema
  • Python dictionary
"""
from __future__ import annotations

import json
import re
from typing import Optional

from src.config.settings import get_available_voices
from src.models.schemas import (
    BubbleStyle, Character, Conversation, DeliverySpeed, Emotion, Ending,
    EndingType, Message,
)

# Common female / male name heuristics
FEMALE_NAMES = {
    "alice", "aria", "charlotte", "chloe", "clara", "elena", "emily", "emma",
    "grace", "hannah", "jenny", "jessica", "julia", "katie", "laura", "lucy",
    "maria", "mia", "olivia", "rachel", "sam", "sarah", "sophia", "zoe",
    "mom", "sister", "grandma", "girlfriend", "wife", "aunt", "girl", "daughter",
}
MALE_NAMES = {
    "adam", "alex", "andrew", "ben", "bob", "brian", "chris", "christopher",
    "dan", "david", "eric", "george", "guy", "jack", "jake", "james", "john",
    "leo", "lucas", "mark", "max", "mike", "noah", "ryan", "sam", "tom",
    "dad", "brother", "grandpa", "boyfriend", "husband", "uncle", "boss",
    "bro", "dude", "man", "son", "homie", "mate",
}


def parse_custom_conversation(
    raw_input: str | dict,
    default_title: str = "Chat Story",
    default_male_voice: str = "male_01",
    default_female_voice: str = "female_01",
) -> Conversation:
    """
    Parse a custom user script or JSON into a valid Conversation object.
    """
    # 1. If dictionary or JSON string, try direct schema parsing
    if isinstance(raw_input, dict):
        return Conversation(**raw_input)

    if isinstance(raw_input, str):
        trimmed = raw_input.strip()
        if (trimmed.startswith("{") and trimmed.endswith("}")) or (trimmed.startswith("[") and trimmed.endswith("]")):
            try:
                data = json.loads(trimmed)
                if isinstance(data, dict):
                    return Conversation(**data)
            except Exception:
                pass  # Fall back to line-by-line script parser

    # 2. Line-by-line text script parsing
    lines = raw_input.strip().splitlines()
    story_title = default_title
    parsed_messages: list[tuple[str, str, Emotion, bool]] = []  # (char_name, text, emotion, is_punchline)
    char_names_order: list[str] = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("//"):
            continue

        # Title detection: e.g. "Title: My Story"
        if re.match(r"^(title|story):\s*", line, re.IGNORECASE):
            story_title = re.sub(r"^(title|story):\s*", "", line, flags=re.IGNORECASE).strip()
            continue

        # Message format: "Name: message", "[Name]: message", "Name (emotion): message"
        match = re.match(r"^(?:\[([A-Za-z0-9_'\s]+?)\]|([A-Za-z0-9_'\s]+?))(?:\s*[\(\[](.*?)[\)\]])?\s*:\s*(.+)$", line)
        if match:
            raw_name = (match.group(1) or match.group(2)).strip()
            tag = (match.group(3) or "").strip().lower()
            text = match.group(4).strip()

            if not text:
                continue

            # Determine emotion and punchline
            emotion = Emotion.CASUAL
            is_punchline = False

            if "punchline" in tag:
                is_punchline = True
                tag = tag.replace("punchline", "").strip(", ")

            for emo in Emotion:
                if emo.value in tag:
                    emotion = emo
                    break

            if raw_name not in char_names_order:
                char_names_order.append(raw_name)

            parsed_messages.append((raw_name, text, emotion, is_punchline))
        else:
            # If no colon, but we have an active character, append to last message
            if parsed_messages:
                last_name, last_text, last_emo, last_punch = parsed_messages[-1]
                parsed_messages[-1] = (last_name, f"{last_text} {line}".strip(), last_emo, last_punch)

    if len(char_names_order) < 2:
        # If user only named 1 character or none, create default 2 characters
        if not char_names_order:
            char_names_order = ["Person A", "Person B"]
        else:
            char_names_order.append("Person B")

    # If no message was flagged as punchline, flag the last message
    if parsed_messages and not any(p[3] for p in parsed_messages):
        last_name, last_text, last_emo, _ = parsed_messages[-1]
        parsed_messages[-1] = (last_name, last_text, last_emo, True)

    # 3. Create Characters
    voices = get_available_voices()
    male_keys = [k for k in voices.keys() if "male" in k and "female" not in k] or ["male_01"]
    female_keys = [k for k in voices.keys() if "female" in k] or ["female_01"]

    characters: list[Character] = []
    char_id_map: dict[str, str] = {}

    for idx, name in enumerate(char_names_order[:3]):  # max 3 characters
        char_id = f"char_{idx + 1}"
        char_id_map[name.lower()] = char_id

        # Check direct voice match in available voices
        lower_name = name.lower()
        if lower_name in voices:
            voice_id = lower_name
        elif any(lower_name in k.lower() or k.lower() in lower_name for k in voices):
            match_k = [k for k in voices if lower_name in k.lower() or k.lower() in lower_name][0]
            voice_id = match_k
        elif "en-" in lower_name:
            voice_id = name
        elif any(fn in lower_name for fn in FEMALE_NAMES) and not any(mn in lower_name for mn in MALE_NAMES):
            voice_id = female_keys[idx % len(female_keys)]
        elif any(mn in lower_name for mn in MALE_NAMES):
            voice_id = male_keys[idx % len(male_keys)]
        else:
            # Alternate male/female
            voice_id = female_keys[0] if idx % 2 == 0 else male_keys[0]

        # First character is INCOMING (left), second character is OUTGOING (right, blue)
        bubble_style = BubbleStyle.INCOMING if idx == 0 else BubbleStyle.OUTGOING

        characters.append(
            Character(
                id=char_id,
                name=name,
                personality="custom",
                voice_id=voice_id,
                bubble_style=bubble_style,
                avatar_color_idx=idx,
            )
        )

    # 4. Create Messages
    messages: list[Message] = []
    for msg_idx, (name, text, emotion, is_punchline) in enumerate(parsed_messages, start=1):
        char_id = char_id_map.get(name.lower(), characters[0].id)
        pause = 700 if is_punchline else 350
        messages.append(
            Message(
                id=msg_idx,
                character_id=char_id,
                text=text,
                emotion=emotion,
                delivery=DeliverySpeed.NORMAL,
                pause_after_ms=pause,
                is_punchline=is_punchline,
            )
        )

    # Ensure minimum 4 messages if too short
    while len(messages) < 4:
        next_id = len(messages) + 1
        c_id = characters[next_id % len(characters)].id
        messages.append(
            Message(
                id=next_id,
                character_id=c_id,
                text="...",
                emotion=Emotion.CASUAL,
            )
        )

    return Conversation(
        story_title=story_title,
        theme="custom",
        characters=characters,
        messages=messages,
        ending=Ending(type=EndingType.PUNCHLINE, text=messages[-1].text if messages else ""),
    )
