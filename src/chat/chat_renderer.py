"""
AutoShorts 2.0 — Chat Interface Renderer.

Generates frame-by-frame animated chat overlays using Pillow:
  • Dark rounded message panel with header
  • Left/right aligned message bubbles with smooth pop-in animations
  • Typing indicator with animated dots
  • Automatic vertical scrolling
  • Transparent RGBA overlays for compositing over gameplay
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFont
from rich.console import Console

from src.config.settings import get
from src.models.schemas import BubbleStyle, Conversation, Timeline, TimelineEvent
from src.chat.animation_timeline import get_visible_messages_at, get_active_typing_at

console = Console()

# ── Font Cache ─────────────────────────────────────────────────────────────

_font_cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}


def _get_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    """Load a font with caching. Falls back through system fonts."""
    key = (name, size)
    if key in _font_cache:
        return _font_cache[key]

    candidates = [
        name,
        "segoeui.ttf", "segoeuib.ttf",
        "arial.ttf", "arialbd.ttf",
        "Roboto-Regular.ttf",
        "DejaVuSans.ttf",
    ]
    font = None
    for candidate in candidates:
        try:
            font = ImageFont.truetype(candidate, size)
            break
        except (OSError, IOError):
            continue

    if font is None:
        font = ImageFont.load_default(size=size)

    _font_cache[key] = font
    return font


def _get_emoji_font(size: int) -> ImageFont.FreeTypeFont:
    """Load an emoji font with caching (Segoe UI Emoji on Windows)."""
    key = ("emoji", size)
    if key in _font_cache:
        return _font_cache[key]

    candidates = [
        "C:/Windows/Fonts/seguiemj.ttf",
        "seguiemj.ttf",
        "NotoColorEmoji.ttf",
    ]
    font = None
    for candidate in candidates:
        try:
            font = ImageFont.truetype(candidate, size)
            break
        except (OSError, IOError):
            continue

    if font is None:
        font = _get_font("Segoe UI", size)

    _font_cache[key] = font
    return font


def _normalize_text(text: str) -> str:
    """Normalize spacing around punctuation to avoid extra gaps.
    Removes accidental spaces before ?  !  .  ,  while preserving emoji spacing."""
    import re
    # Collapse multiple spaces into one
    text = re.sub(r' {2,}', ' ', text)
    # Remove space immediately before common punctuation
    text = re.sub(r'\s+([?!.,;:])', r'\1', text)
    return text.strip()


def _is_emoji_char(ch: str) -> bool:
    """Check if a character is part of common emoji / symbol unicode ranges."""
    cp = ord(ch)
    return (
        0x1F300 <= cp <= 0x1FAFF or  # Misc Symbols, Pictographs, Emoticons, Symbols & Pictographs Ext
        0x2600 <= cp <= 0x27BF or    # Misc Symbols, Dingbats
        0x1F900 <= cp <= 0x1F9FF or  # Supplemental Symbols
        0x1F600 <= cp <= 0x1F64F or  # Emoticons
        0x1F680 <= cp <= 0x1F6FF or  # Transport and Map
        cp == 0x200D or              # Zero Width Joiner
        cp == 0xFE0F                 # Emoji Variation Selector (keep with emoji)
    )


def _split_runs(text: str) -> list[tuple[str, bool]]:
    """Split text into alternating runs of (substring, is_emoji).
    Variation selectors (U+FE0F) stay attached to the preceding emoji."""
    runs: list[tuple[str, bool]] = []
    if not text:
        return runs
    curr = ""
    is_em = _is_emoji_char(text[0])
    for ch in text:
        # Keep variation selector with preceding content
        if ord(ch) == 0xFE0F:
            curr += ch
            continue
        # Skip variation selector range in mode decision
        if 0xFE00 <= ord(ch) <= 0xFE0E:
            curr += ch
            continue
        c_em = _is_emoji_char(ch)
        if c_em != is_em:
            if curr:
                runs.append((curr, is_em))
            curr = ch
            is_em = c_em
        else:
            curr += ch
    if curr:
        runs.append((curr, is_em))
    return runs


def _measure_run_width(text: str, font_text: ImageFont.FreeTypeFont, font_emoji: ImageFont.FreeTypeFont) -> int:
    """Accurately measure text width accounting for both standard and emoji runs.
    Uses font_emoji.size + 4 for emoji runs, exactly matching _draw_bubble."""
    w = 0
    for chunk, is_em in _split_runs(text):
        if is_em:
            em_count = len([c for c in chunk if ord(c) not in (0xFE0F, 0x200D) and not (0xFE00 <= ord(c) <= 0xFE0E)])
            w += max(1, em_count) * (font_emoji.size + 4)
        else:
            w += int(font_text.getlength(chunk))
    return w


# ── Data Structures ────────────────────────────────────────────────────────

def _draw_default_avatar(size: int = 50) -> Image.Image:
    """Render a clean Instagram-style circular user avatar icon."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([0, 0, size - 1, size - 1], fill=(220, 220, 225, 255))
    sil_color = (130, 130, 135, 255)
    head_r = int(size * 0.20)
    head_cx = size // 2
    head_cy = int(size * 0.36)
    d.ellipse([head_cx - head_r, head_cy - head_r, head_cx + head_r, head_cy + head_r], fill=sil_color)
    body_rx = int(size * 0.40)
    body_ry = int(size * 0.32)
    body_cy = int(size * 0.90)
    d.ellipse([head_cx - body_rx, body_cy - body_ry, head_cx + body_rx, body_cy + body_ry], fill=sil_color)
    circle_mask = Image.new("L", (size, size), 0)
    cmd = ImageDraw.Draw(circle_mask)
    cmd.ellipse([0, 0, size - 1, size - 1], fill=255)
    final_av = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    final_av.paste(img, (0, 0), circle_mask)
    return final_av


@dataclass
class RenderedBubble:
    """Pre-calculated layout for a single message bubble."""
    message_id: int
    character_id: str
    text: str
    is_outgoing: bool
    is_punchline: bool
    # Layout (relative to content area)
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    # Wrapped text lines
    lines: list[str] = field(default_factory=list)
    # Animation state
    appear_time: float = 0.0
    is_last_in_group: bool = False
    has_avatar: bool = False


# ── Main Renderer ──────────────────────────────────────────────────────────

class ChatRenderer:
    """
    Renders animated chat conversation frames.
    Supports modern borderless Instagram DM theme and classic panel theme.

    Usage:
        renderer = ChatRenderer(conversation, timeline)
        frame = renderer.render_frame(time_sec)  # → PIL RGBA Image
    """

    def __init__(self, conversation: Conversation, timeline: Timeline):
        self.conversation = conversation
        self.timeline = timeline

        # Load chat config
        cfg = get("chat", default={})
        self.canvas_w = get("video", "width", 1080)
        self.canvas_h = get("video", "height", 1920)

        self.theme = cfg.get("theme", "instagram")
        self.draw_panel = cfg.get("draw_panel", False)
        self.draw_header = cfg.get("draw_header", False)
        self.canvas_margin_top = cfg.get("canvas_margin_top", 260)

        # Panel dimensions (only used if draw_panel is True)
        self.panel_w = cfg.get("panel_width", 920)
        self.panel_margin_top = cfg.get("panel_margin_top", 180)
        self.panel_margin_x = cfg.get("panel_margin_x", 80)
        self.panel_h_max = cfg.get("panel_height_max", 1400)
        self.panel_corner_r = cfg.get("panel_corner_radius", 28)

        # Colors
        self.panel_bg = tuple(cfg.get("panel_bg_color", [28, 28, 30, 235]))
        self.header_bg = tuple(cfg.get("header_bg_color", [44, 44, 46, 255]))
        self.header_text_color = tuple(cfg.get("header_text_color", [255, 255, 255]))
        self.bubble_in_color = tuple(cfg.get("bubble_incoming_color", [38, 38, 40, 245]))
        self.bubble_out_color = tuple(cfg.get("bubble_outgoing_color", [124, 58, 237, 255]))
        self.text_in_color = tuple(cfg.get("bubble_incoming_text_color", [255, 255, 255]))
        self.text_out_color = tuple(cfg.get("bubble_outgoing_text_color", [255, 255, 255]))
        self.avatar_colors = cfg.get("avatar_colors", [[0, 122, 255], [255, 59, 48], [52, 199, 89]])

        # Sizing
        self.header_h = cfg.get("header_height", 90)
        self.bubble_corner_r = cfg.get("bubble_corner_radius", 22)
        self.bubble_max_w = cfg.get("bubble_max_width", 720)
        self.bubble_spacing_same = cfg.get("bubble_spacing_same", 8)
        self.bubble_spacing_diff = cfg.get("bubble_spacing_diff", 24)
        self.bubble_spacing = cfg.get("bubble_spacing", 12)
        self.bubble_margin_x = cfg.get("bubble_margin_x", 45)
        self.msg_pad_x = cfg.get("message_padding_x", 24)
        self.msg_pad_y = cfg.get("message_padding_y", 14)
        self.avatar_size = cfg.get("avatar_size", 50)
        self.avatar_margin_x = cfg.get("avatar_margin_x", 45)

        # Fonts
        font_name = cfg.get("font_family", "Segoe UI")
        font_bold = cfg.get("font_bold", "Segoe UI Bold")
        self.text_font_size = cfg.get("text_font_size", 32)
        self.emoji_font_size = cfg.get("emoji_font_size", 34)
        self.header_font_size = cfg.get("header_font_size", 34)
        self.ts_font_size = cfg.get("timestamp_font_size", 20)

        self.font_text = _get_font(font_name, self.text_font_size)
        self.font_bold = _get_font(font_bold, self.header_font_size)
        self.font_small = _get_font(font_name, self.ts_font_size)
        self.font_emoji = _get_emoji_font(self.emoji_font_size)
        self.header_icon_font = _get_emoji_font(28)
        self.avatar_img = _draw_default_avatar(self.avatar_size)

        # Compute exact vertical offset for emoji alignment with text cap-height center
        text_bbox = self.font_text.getbbox("H")
        text_ascent = self.font_text.getmetrics()[0]
        emoji_bbox = self.font_emoji.getbbox("\U0001F600")
        if text_bbox and emoji_bbox:
            self.emoji_y_offset = ((text_bbox[1] + text_ascent) - (emoji_bbox[1] + emoji_bbox[3])) // 2
        else:
            self.emoji_y_offset = 10

        # Animation
        self.appear_dur = cfg.get("message_appear_duration_ms", 220) / 1000.0
        self.scroll_speed = cfg.get("scroll_pixels_per_frame", 8)
        self.typing_dot_size = cfg.get("typing_dot_size", 10)

        # Positioning layout
        if self.draw_panel:
            self.panel_x = (self.canvas_w - self.panel_w) // 2
            self.panel_y = self.panel_margin_top
            self.content_x = self.panel_x
            self.content_y = self.panel_y + self.header_h
            self.content_w = self.panel_w
            self.content_h = self.panel_h_max - self.header_h
        else:
            self.panel_x = 0
            self.panel_y = 0
            self.content_x = 0
            self.content_y = 0
            self.content_w = self.canvas_w
            self.content_h = self.canvas_h

        # Build character lookup
        self._char_map = {c.id: c for c in conversation.characters}
        incoming_chars = [c for c in conversation.characters if c.bubble_style == BubbleStyle.INCOMING]
        self._header_char = incoming_chars[0] if incoming_chars else conversation.characters[0]

        # Pre-calculate all bubble layouts
        self._bubbles: list[RenderedBubble] = []
        self._total_content_height = 0
        self._precalculate_bubbles()

    # ── Pre-calculation ────────────────────────────────────────────────────

    def _precalculate_bubbles(self):
        """Pre-calculate layout for all message bubbles."""
        self._bubbles = []
        y_cursor = self.canvas_margin_top if not self.draw_panel else 12

        events = [e for e in self.timeline.events if self._find_message(e.message_id) is not None]

        for idx, event in enumerate(events):
            char = self._char_map.get(event.character_id)
            is_outgoing = char.bubble_style == BubbleStyle.OUTGOING if char else False

            # Check if this message is the last in a consecutive group from same character
            next_event = events[idx + 1] if idx + 1 < len(events) else None
            is_last_in_group = (next_event is None or next_event.character_id != event.character_id)

            # Normalize and word-wrap text
            clean_text = _normalize_text(event.text)
            max_text_w = self.bubble_max_w - 2 * self.msg_pad_x
            lines = self._wrap_text(clean_text, self.font_text, max_text_w)

            # Calculate bubble dimensions
            line_height = self.text_font_size + 8
            text_height = line_height * len(lines)
            bubble_h = text_height + 2 * self.msg_pad_y

            # Calculate bubble width (fit to content)
            max_line_w = 0
            for line in lines:
                lw = _measure_run_width(line, self.font_text, self.font_emoji)
                max_line_w = max(max_line_w, lw)
            bubble_w = min(self.bubble_max_w, max_line_w + 2 * self.msg_pad_x + 20)
            bubble_w = max(bubble_w, 90)  # minimum width

            # X position
            if is_outgoing:
                x = self.content_w - self.bubble_margin_x - bubble_w
            else:
                if not self.draw_panel:
                    x = self.avatar_margin_x + self.avatar_size + 14
                else:
                    x = self.bubble_margin_x

            bubble = RenderedBubble(
                message_id=event.message_id,
                character_id=event.character_id,
                text=event.text,
                is_outgoing=is_outgoing,
                is_punchline=event.is_punchline,
                x=x,
                y=y_cursor,
                width=bubble_w,
                height=bubble_h,
                lines=lines,
                appear_time=event.bubble_appear_sec,
                is_last_in_group=is_last_in_group,
                has_avatar=(not is_outgoing and is_last_in_group and not self.draw_panel),
            )
            self._bubbles.append(bubble)

            spacing = self.bubble_spacing_diff if is_last_in_group else self.bubble_spacing_same
            y_cursor += bubble_h + spacing

        self._total_content_height = y_cursor

    def _find_message(self, message_id: int):
        for m in self.conversation.messages:
            if m.id == message_id:
                return m
        return None

    # ── Frame Rendering ────────────────────────────────────────────────────

    def render_frame(self, time_sec: float) -> Image.Image:
        """
        Render a single frame at the given time.
        Returns a 1080×1920 RGBA image (transparent where no chat UI).
        """
        frame = Image.new("RGBA", (self.canvas_w, self.canvas_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame)

        # Determine visible messages at this time
        visible_events = get_visible_messages_at(self.timeline, time_sec)
        visible_ids = {e.message_id for e in visible_events}

        # Calculate scroll offset
        scroll_offset = self._calculate_scroll(visible_ids, time_sec)

        # Draw panel background (if panel mode enabled)
        if self.draw_panel:
            self._draw_panel_bg(draw)

        # Create clipping mask for content area
        content_img = Image.new("RGBA", (self.content_w, self.content_h), (0, 0, 0, 0))
        content_draw = ImageDraw.Draw(content_img)

        # Draw visible bubbles
        for bubble in self._bubbles:
            if bubble.message_id not in visible_ids:
                continue

            # Animation progress (0.0 → 1.0)
            elapsed = time_sec - bubble.appear_time
            progress = min(1.0, elapsed / self.appear_dur) if self.appear_dur > 0 else 1.0

            # Ease-out cubic
            progress = 1.0 - (1.0 - progress) ** 3

            if progress <= 0:
                continue

            self._draw_bubble(content_img, content_draw, bubble, scroll_offset, progress)

        # Draw typing indicator
        typing_event = get_active_typing_at(self.timeline, time_sec)
        if typing_event and typing_event.message_id not in visible_ids:
            self._draw_typing_indicator(content_img, content_draw, typing_event, scroll_offset, time_sec)

        # Paste content onto frame
        frame.paste(content_img, (self.content_x, self.content_y), content_img)

        # Draw header if enabled
        if self.draw_header:
            self._draw_header(frame)

        return frame

    # ── Drawing Helpers ────────────────────────────────────────────────────

    def _draw_panel_bg(self, draw: ImageDraw.Draw):
        """Draw the dark rounded panel background."""
        if not self.draw_panel:
            return
        x1 = self.panel_x
        y1 = self.panel_y
        x2 = self.panel_x + self.panel_w
        y2 = self.panel_y + self.panel_h_max
        draw.rounded_rectangle(
            [x1, y1, x2, y2],
            radius=self.panel_corner_r,
            fill=self.panel_bg,
        )

    def _draw_header(self, frame: Image.Image):
        """Draw the contact header bar matching iMessage/reference YouTube Short style."""
        if not self.draw_header:
            return
        header_img = Image.new("RGBA", (self.panel_w, self.header_h), (0, 0, 0, 0))
        hd = ImageDraw.Draw(header_img)

        # Header background (with top rounded corners)
        hd.rounded_rectangle(
            [0, 0, self.panel_w, self.header_h + 15],
            radius=self.panel_corner_r,
            fill=self.header_bg,
        )
        hd.rectangle(
            [0, self.header_h - 15, self.panel_w, self.header_h],
            fill=self.header_bg,
        )

        # Thin separator line at bottom of header
        hd.line([(0, self.header_h - 1), (self.panel_w, self.header_h - 1)],
                fill=(60, 60, 62, 255), width=1)

        # Back arrow — iOS-style chevron
        arrow_x = 18
        arrow_cy = self.header_h // 2
        arrow_color = (0, 122, 255, 255)
        hd.text((arrow_x, arrow_cy - 16), "‹", fill=arrow_color,
                font=_get_font("Segoe UI", 38))

        # Centered avatar circle (gray, like reference)
        char = self._header_char
        avatar_cx = self.panel_w // 2
        avatar_cy_pos = self.header_h // 2 - 6
        avatar_r = self.avatar_size // 2
        color_idx = char.avatar_color_idx % len(self.avatar_colors)
        avatar_color = tuple(self.avatar_colors[color_idx]) + (255,)

        hd.ellipse(
            [avatar_cx - avatar_r, avatar_cy_pos - avatar_r,
             avatar_cx + avatar_r, avatar_cy_pos + avatar_r],
            fill=avatar_color,
        )
        initial = char.name[0].upper() if char.name else "?"
        init_font = _get_font("Segoe UI Bold", 20)
        ibbox = init_font.getbbox(initial)
        iw = ibbox[2] - ibbox[0]
        ih = ibbox[3] - ibbox[1]
        hd.text(
            (avatar_cx - iw // 2, avatar_cy_pos - ih // 2 - 2),
            initial, fill=(255, 255, 255, 255), font=init_font,
        )

        # Name centered below avatar
        name_font = _get_font("Segoe UI", 22)
        name_bbox = name_font.getbbox(char.name)
        name_w = name_bbox[2] - name_bbox[0] if name_bbox else 80
        name_x = avatar_cx - name_w // 2
        name_y = avatar_cy_pos + avatar_r + 2
        hd.text((name_x, name_y), char.name, fill=self.header_text_color,
                font=name_font)

        # Right side icon — video camera
        icon_x = self.panel_w - 60
        icon_y = self.header_h // 2 - 14
        hd.text((icon_x, icon_y), "📹", font=self.header_icon_font, embedded_color=True)

        frame.paste(header_img, (self.panel_x, self.panel_y), header_img)

    def _draw_bubble(
        self,
        content_img: Image.Image,
        draw: ImageDraw.Draw,
        bubble: RenderedBubble,
        scroll_offset: int,
        progress: float,
    ):
        """Draw a single message bubble with animation."""
        y = bubble.y - scroll_offset

        slide_offset = int((1.0 - progress) * 16)
        y += slide_offset
        alpha = int(progress * 255)

        if y + bubble.height < 0 or y > self.content_h:
            return

        # Draw avatar on left if incoming and last in group
        if bubble.has_avatar and 0 <= y + bubble.height <= self.content_h + 100:
            av_x = self.avatar_margin_x
            av_y = y + bubble.height - self.avatar_size
            content_img.paste(self.avatar_img, (av_x, av_y), self.avatar_img)

        # Bubble colors
        if bubble.is_outgoing:
            c = self.bubble_out_color
            bg_color = (c[0], c[1], c[2], min(c[3] if len(c) > 3 else 255, alpha))
            text_color = self.text_out_color + (alpha,)
        else:
            c = self.bubble_in_color
            bg_color = (c[0], c[1], c[2], min(c[3] if len(c) > 3 else 245, alpha))
            text_color = self.text_in_color + (alpha,)

        # Draw rounded rectangle bubble
        x1 = bubble.x
        y1 = y
        x2 = bubble.x + bubble.width
        y2 = y + bubble.height

        draw.rounded_rectangle(
            [x1, y1, x2, y2],
            radius=self.bubble_corner_r,
            fill=bg_color,
        )

        # Draw text lines — use common vertical center for text and emoji
        line_height = self.text_font_size + 8
        text_x = x1 + self.msg_pad_x
        text_y = y1 + self.msg_pad_y

        for line in bubble.lines:
            if 0 <= text_y < self.content_h:
                curr_x = text_x
                for chunk, is_em in _split_runs(line):
                    if is_em:
                        ey = text_y + self.emoji_y_offset
                        draw.text((curr_x, ey), chunk, font=self.font_emoji, embedded_color=True)
                        em_count = len([c for c in chunk if ord(c) not in (0xFE0F, 0x200D) and not (0xFE00 <= ord(c) <= 0xFE0E)])
                        curr_x += max(1, em_count) * (self.font_emoji.size + 4)
                    else:
                        draw.text((curr_x, text_y), chunk, fill=text_color, font=self.font_text)
                        curr_x += int(self.font_text.getlength(chunk))
            text_y += line_height

    def _draw_typing_indicator(
        self,
        content_img: Image.Image,
        draw: ImageDraw.Draw,
        event: TimelineEvent,
        scroll_offset: int,
        time_sec: float,
    ):
        """Draw the animated typing indicator (three bouncing dots)."""
        char = self._char_map.get(event.character_id)
        is_outgoing = char.bubble_style == BubbleStyle.OUTGOING if char else False

        y = self._get_typing_y(event.message_id) - scroll_offset

        if y + 44 < 0 or y > self.content_h:
            return

        indicator_w = 90
        indicator_h = 48

        if is_outgoing:
            x = self.content_w - self.bubble_margin_x - indicator_w
        else:
            x = self.avatar_margin_x + self.avatar_size + 14 if not self.draw_panel else self.bubble_margin_x
            if not self.draw_panel:
                content_img.paste(self.avatar_img, (self.avatar_margin_x, y + indicator_h - self.avatar_size), self.avatar_img)

        # Background
        bg_color = self.bubble_out_color if is_outgoing else self.bubble_in_color
        draw.rounded_rectangle(
            [x, y, x + indicator_w, y + indicator_h],
            radius=self.bubble_corner_r,
            fill=bg_color,
        )

        # Animated dots
        dot_r = self.typing_dot_size // 2
        dot_y_base = y + indicator_h // 2
        dot_start_x = x + 24
        dot_spacing = 20

        elapsed = time_sec - event.typing_start_sec
        for i in range(3):
            dot_x = dot_start_x + i * dot_spacing
            phase = elapsed * 4.0 - i * 0.5
            bounce = abs(math.sin(phase)) * 6
            dot_y = int(dot_y_base - bounce)

            dot_alpha = 180 + int(bounce * 10)
            draw.ellipse(
                [dot_x - dot_r, dot_y - dot_r, dot_x + dot_r, dot_y + dot_r],
                fill=(180, 180, 185, min(255, dot_alpha)),
            )

    def _get_typing_y(self, message_id: int) -> int:
        """Get the Y position where the typing indicator should appear."""
        for bubble in self._bubbles:
            if bubble.message_id == message_id:
                return bubble.y
        if self._bubbles:
            last = self._bubbles[-1]
            return last.y + last.height + self.bubble_spacing_same
        return self.canvas_margin_top

    def _calculate_scroll(self, visible_ids: set[int], time_sec: float) -> int:
        """Calculate vertical scroll offset so newest messages stay visible."""
        if not visible_ids:
            return 0

        newest_bottom = 0
        for bubble in self._bubbles:
            if bubble.message_id in visible_ids:
                bottom = bubble.y + bubble.height + self.bubble_spacing_diff
                newest_bottom = max(newest_bottom, bottom)

        limit_h = self.content_h - 260 if not self.draw_panel else self.content_h
        if newest_bottom <= limit_h:
            return 0

        target_scroll = newest_bottom - limit_h
        return max(0, target_scroll)

    # ── Text Wrapping ──────────────────────────────────────────────────────

    def _wrap_text(self, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
        """Word-wrap text to fit within max_width pixels."""
        words = text.split()
        if not words:
            return [text]

        lines: list[str] = []
        current_line = ""

        for word in words:
            test = f"{current_line} {word}".strip() if current_line else word
            text_w = _measure_run_width(test, font, self.font_emoji)

            if text_w <= max_width:
                current_line = test
            else:
                if current_line:
                    lines.append(current_line)
                # Handle very long words
                if _measure_run_width(word, font, self.font_emoji) > max_width:
                    # Force break the word
                    current_line = ""
                    for char in word:
                        test = current_line + char
                        if _measure_run_width(test, font, self.font_emoji) > max_width:
                            lines.append(current_line)
                            current_line = char
                        else:
                            current_line = test
                else:
                    current_line = word

        if current_line:
            lines.append(current_line)

        return lines if lines else [text]
