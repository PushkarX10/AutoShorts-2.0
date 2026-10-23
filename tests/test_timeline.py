"""
Unit tests for Animation Timeline Builder.
"""
import unittest

from src.chat.animation_timeline import (
    build_timeline, get_active_typing_at, get_visible_messages_at,
)
from src.models.schemas import (
    AudioClip, AudioManifest, BubbleStyle, Character, Conversation, Message,
)


class TestTimeline(unittest.TestCase):

    def test_timeline_timing(self):
        chars = [
            Character(id="a", name="Alice", personality="witty", voice_id="female_01", bubble_style=BubbleStyle.OUTGOING),
            Character(id="b", name="Bob", personality="chill", voice_id="male_01", bubble_style=BubbleStyle.INCOMING),
        ]
        msgs = [
            Message(id=1, character_id="a", text="Hey Bob"),
            Message(id=2, character_id="b", text="What's up Alice"),
            Message(id=3, character_id="a", text="Look outside"),
            Message(id=4, character_id="b", text="Bro why is there a goat on my car", is_punchline=True),
        ]
        convo = Conversation(
            story_title="Goat on car",
            characters=chars,
            messages=msgs,
        )
        manifest = AudioManifest(
            clips=[
                AudioClip(message_id=1, character_id="a", text="Hey Bob", audio_path="a1.wav", duration_sec=1.0, voice_id="f1"),
                AudioClip(message_id=2, character_id="b", text="What's up Alice", audio_path="b2.wav", duration_sec=1.2, voice_id="m1"),
                AudioClip(message_id=3, character_id="a", text="Look outside", audio_path="a3.wav", duration_sec=0.8, voice_id="f1"),
                AudioClip(message_id=4, character_id="b", text="Bro why is there a goat on my car", audio_path="b4.wav", duration_sec=2.0, voice_id="m1"),
            ],
            total_voice_duration=5.0,
        )

        timeline = build_timeline(convo, manifest, fps=30)

        self.assertEqual(len(timeline.events), 4)
        self.assertGreater(timeline.total_duration_sec, 5.0)
        self.assertEqual(timeline.total_frames, int(timeline.total_duration_sec * 30))

        # First message typing start
        self.assertGreaterEqual(timeline.events[0].typing_start_sec, 0.5)
        # Punchline extra pause
        self.assertTrue(timeline.events[3].is_punchline)

        # Visibility helper
        vis = get_visible_messages_at(timeline, timeline.events[1].bubble_appear_sec + 0.1)
        self.assertGreaterEqual(len(vis), 2)


if __name__ == "__main__":
    unittest.main()
