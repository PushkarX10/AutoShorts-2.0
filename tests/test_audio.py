"""
Unit tests for SFX Generator and Audio Assets.
"""
import unittest
from pathlib import Path

from src.audio.sfx_generator import (
    ensure_default_audio_assets, generate_bubble_pop, generate_typing_click,
    generate_punchline_sting,
)
from src.config.settings import get_temp_dir


class TestAudio(unittest.TestCase):

    def test_sfx_generation(self):
        tmp = get_temp_dir() / "test_sfx"
        tmp.mkdir(parents=True, exist_ok=True)

        pop_path = tmp / "pop.wav"
        generate_bubble_pop(pop_path)
        self.assertTrue(pop_path.exists())
        self.assertGreater(pop_path.stat().st_size, 100)

        type_path = tmp / "typing.wav"
        generate_typing_click(type_path)
        self.assertTrue(type_path.exists())
        self.assertGreater(type_path.stat().st_size, 100)

        sting_path = tmp / "sting.wav"
        generate_punchline_sting(sting_path)
        self.assertTrue(sting_path.exists())
        self.assertGreater(sting_path.stat().st_size, 100)

    def test_audio_assets_loader(self):
        assets = ensure_default_audio_assets()
        self.assertIn("pop", assets)
        self.assertIn("typing", assets)
        self.assertIn("punchline", assets)
        self.assertIn("music", assets)
        for name, p in assets.items():
            self.assertTrue(Path(p).exists())


if __name__ == "__main__":
    unittest.main()
