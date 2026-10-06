"""Run inside the runner with python3 -m unittest discover -s tests -v."""

from datetime import datetime, timedelta
from pathlib import Path
import unittest
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]


class TimezoneTests(unittest.TestCase):
    def test_new_york_standard_time(self):
        zone = ZoneInfo("America/New_York")
        self.assertEqual(datetime(2026, 1, 15, tzinfo=zone).utcoffset(), timedelta(hours=-5))

    def test_new_york_daylight_time(self):
        zone = ZoneInfo("America/New_York")
        self.assertEqual(datetime(2026, 7, 15, tzinfo=zone).utcoffset(), timedelta(hours=-4))


class ImageContractTests(unittest.TestCase):
    def test_image_installs_timezone_data_and_keeps_runner_user(self):
        dockerfile = (ROOT / "Dockerfile").read_text()
        self.assertIn("FROM ghcr.io/actions/actions-runner:2.316.1", dockerfile)
        self.assertIn("--no-install-recommends python3 tzdata", dockerfile)
        self.assertIn("DEBIAN_FRONTEND=noninteractive", dockerfile)
        self.assertIn('ZoneInfo("America/New_York")', dockerfile)
        self.assertEqual(dockerfile.strip().splitlines()[-1], "USER runner")

    def test_compose_selects_derived_image(self):
        compose = (ROOT / "docker-compose.yml").read_text()
        self.assertIn("    build: .\n", compose)
        self.assertIn("    image: homelab-actions-runner:2.316.1-tzdata\n", compose)


if __name__ == "__main__":
    unittest.main()
