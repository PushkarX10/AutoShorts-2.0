"""
AutoShorts 2.0 — Conversation Quality Checker.

Runs heuristic checks on generated conversations before rendering:
  • Repetitive messages
  • Weak endings
  • Excessive length
  • Missing punchlines
  • Character imbalance
"""
from __future__ import annotations

from collections import Counter

from rich.console import Console

from src.models.schemas import Conversation

console = Console()


class QualityIssue:
    def __init__(self, severity: str, message: str):
        self.severity = severity  # "error" | "warning"
        self.message = message

    def __repr__(self):
        return f"[{self.severity.upper()}] {self.message}"


def check_conversation_quality(convo: Conversation) -> tuple[bool, list[QualityIssue]]:
    """
    Run quality checks on a conversation.
    Returns (passed, issues).
    """
    issues: list[QualityIssue] = []

    # 1. Check minimum message count
    if len(convo.messages) < 4:
        issues.append(QualityIssue("error", f"Too few messages: {len(convo.messages)} (need ≥ 4)"))

    # 2. Check for repetitive messages
    texts = [m.text.lower().strip() for m in convo.messages]
    dupes = [txt for txt, count in Counter(texts).items() if count > 1]
    if dupes:
        issues.append(QualityIssue("error", f"Duplicate messages found: {dupes[:3]}"))

    # 3. Check for very similar consecutive messages
    for i in range(1, len(texts)):
        if _similarity(texts[i], texts[i - 1]) > 0.8:
            issues.append(QualityIssue("warning",
                          f"Messages {i} and {i + 1} are very similar"))

    # 4. Check punchline exists
    has_punchline = any(m.is_punchline for m in convo.messages)
    if not has_punchline:
        issues.append(QualityIssue("warning", "No message marked as punchline"))

    # 5. Check punchline is near the end
    punchline_positions = [i for i, m in enumerate(convo.messages) if m.is_punchline]
    if punchline_positions:
        last_punch = max(punchline_positions)
        if last_punch < len(convo.messages) - 3:
            issues.append(QualityIssue("warning",
                          "Punchline is too far from the end of conversation"))

    # 6. Check character balance
    char_counts = Counter(m.character_id for m in convo.messages)
    if len(char_counts) > 1:
        counts = list(char_counts.values())
        ratio = min(counts) / max(counts)
        if ratio < 0.25:
            issues.append(QualityIssue("warning",
                          "Character participation is very unbalanced"))

    # 7. Check individual message length
    for msg in convo.messages:
        if len(msg.text) > 250:
            issues.append(QualityIssue("warning",
                          f"Message {msg.id} is very long ({len(msg.text)} chars)"))

    # 8. Check story title exists
    if not convo.story_title or convo.story_title.lower() == "untitled chat":
        issues.append(QualityIssue("warning", "Missing or generic story title"))

    # 9. Check all characters are used
    used_chars = set(m.character_id for m in convo.messages)
    defined_chars = set(c.id for c in convo.characters)
    unused = defined_chars - used_chars
    if unused:
        issues.append(QualityIssue("warning", f"Characters defined but never speak: {unused}"))

    # Determine pass/fail
    errors = [i for i in issues if i.severity == "error"]
    passed = len(errors) == 0

    if issues:
        console.print(f"[yellow]⚠[/yellow] Quality check: {len(issues)} issue(s)")
        for issue in issues:
            icon = "❌" if issue.severity == "error" else "⚠️"
            console.print(f"  {icon} {issue.message}")
    else:
        console.print("[green]✓[/green] Quality check passed")

    return passed, issues


def _similarity(a: str, b: str) -> float:
    """Simple word-overlap similarity between two strings."""
    words_a = set(a.split())
    words_b = set(b.split())
    if not words_a or not words_b:
        return 0.0
    intersection = words_a & words_b
    union = words_a | words_b
    return len(intersection) / len(union)
