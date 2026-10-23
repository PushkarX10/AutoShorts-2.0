"""
Unit tests for custom conversation script parser.
"""
import unittest

from src.llm.custom_convo_parser import parse_custom_conversation
from src.models.schemas import Emotion


class TestCustomConvoParser(unittest.TestCase):

    def test_parse_plain_script(self):
        script = """
Title: Midnight Pizza
Emily: Are you awake?
Mike: No, I'm sleep-texting.
Emily (excited): Look what I just ordered!
Mike (shocked): Is that 4 whole pizzas?!
Emily [punchline]: One for each of my personalities.
"""
        convo = parse_custom_conversation(script)
        self.assertEqual(convo.story_title, "Midnight Pizza")
        self.assertEqual(len(convo.characters), 2)
        self.assertEqual(convo.characters[0].name, "Emily")
        self.assertEqual(convo.characters[1].name, "Mike")
        self.assertEqual(len(convo.messages), 5)
        self.assertEqual(convo.messages[2].emotion, Emotion.EXCITED)
        self.assertEqual(convo.messages[3].emotion, Emotion.SHOCKED)
        self.assertTrue(convo.messages[4].is_punchline)


if __name__ == "__main__":
    unittest.main()
