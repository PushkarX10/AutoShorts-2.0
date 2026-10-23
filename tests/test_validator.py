"""
Unit tests for Quality Assurance & Video Validator.
"""
import unittest
from pathlib import Path

from src.validation.video_validator import validate_video


class TestValidator(unittest.TestCase):

    def test_validator_on_sample(self):
        sample_path = Path("input/sample_parkour.mp4")
        if not sample_path.exists():
            self.skipTest("Sample parkour video not generated yet")

        report = validate_video(sample_path, job_id="test_qa")
        self.assertIsNotNone(report)
        self.assertEqual(report.resolution, "1080x1920")
        self.assertGreater(report.file_size_mb, 0.5)


if __name__ == "__main__":
    unittest.main()
