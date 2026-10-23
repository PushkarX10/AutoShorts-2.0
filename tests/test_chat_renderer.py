"""
Unit tests for Chat Renderer.
"""
import unittest

from PIL import Image

from src.chat.animation_timeline import build_timeline
from src.chat.chat_renderer import ChatRenderer
from src.models.schemas import (
    AudioClip, AudioManifest, BubbleStyle, Character, Conversation, Message,
)


class TestChatRenderer(unittest.TestCase):

    def test_chat_renderer_frame_generation(self):
        chars = [
            Character(id="a", name="Sarah", personality="funny", voice_id="female_01", bubble_style=BubbleStyle.OUTGOING),
            Character(id="b", name="Mike", personality="chill", voice_id="male_01", bubble_style=BubbleStyle.INCOMING),
        ]
        msgs = [
            Message(id=1, character_id="a", text="Did you lock the front door?"),
            Message(id=2, character_id="b", text="I thought you locked it..."),
            Message(id=3, character_id="a", text="Mike we are in another country."),
            Message(id=4, character_id="b", text="Oh.", is_punchline=True),
        ]
        convo = Conversation(story_title="Front Door", characters=chars, messages=msgs)
        manifest = AudioManifest(
            clips=[
                AudioClip(message_id=1, character_id="a", text="Did you lock the front door?", audio_path="a1.wav", duration_sec=1.2, voice_id="f1"),
                AudioClip(message_id=2, character_id="b", text="I thought you locked it...", audio_path="b2.wav", duration_sec=1.1, voice_id="m1"),
                AudioClip(message_id=3, character_id="a", text="Mike we are in another country.", audio_path="a3.wav", duration_sec=1.5, voice_id="f1"),
                AudioClip(message_id=4, character_id="b", text="Oh.", audio_path="b4.wav", duration_sec=0.5, voice_id="m1"),
            ],
            total_voice_duration=4.3,
        )
        timeline = build_timeline(convo, manifest, fps=30)
        renderer = ChatRenderer(convo, timeline)

        # Render frame at 2.0s
        frame = renderer.render_frame(2.0)
        self.assertIsInstance(frame, Image.Image)
        self.assertEqual(frame.size, (1080, 1920))
        self.assertEqual(frame.mode, "RGBA")


if __name__ == "__main__":
    unittest.main()
