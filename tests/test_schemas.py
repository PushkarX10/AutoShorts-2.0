"""
Unit tests for AutoShorts 2.0 schemas.
"""
import unittest

from src.models.schemas import (
    BubbleStyle, Character, Conversation, DeliverySpeed,
    Emotion, Ending, EndingType, HumorStyle, Message,
)


class TestSchemas(unittest.TestCase):

    def test_character_creation(self):
        c = Character(
            id="char_1",
            name="Alex",
            personality="sarcastic roommate",
            voice_id="female_01",
            bubble_style=BubbleStyle.INCOMING,
        )
        self.assertEqual(c.id, "char_1")
        self.assertEqual(c.name, "Alex")
        self.assertEqual(c.bubble_style, BubbleStyle.INCOMING)

    def test_message_cleaning(self):
        m = Message(
            id=1,
            character_id="char_1",
            text="   Hey there!   ",
            emotion=Emotion.EXCITED,
        )
        self.assertEqual(m.text, "Hey there!")

    def test_conversation_validation(self):
        chars = [
            Character(id="a", name="Alice", personality="witty", voice_id="female_01"),
            Character(id="b", name="Bob", personality="chill", voice_id="male_01"),
        ]
        msgs = [
            Message(id=1, character_id="a", text="Did you hear that?"),
            Message(id=2, character_id="b", text="Hear what?"),
            Message(id=3, character_id="a", text="The sound of my patience evaporating."),
            Message(id=4, character_id="b", text="classic.", is_punchline=True),
        ]
        convo = Conversation(
            story_title="Patience",
            theme="roommate",
            characters=chars,
            messages=msgs,
        )
        self.assertEqual(len(convo.messages), 4)
        self.assertEqual(convo.validate_character_refs(), [])


if __name__ == "__main__":
    unittest.main()
