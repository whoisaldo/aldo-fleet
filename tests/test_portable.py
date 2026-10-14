import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import fleetlib
import portable

SPEC = importlib.util.spec_from_file_location("check_cache", fleetlib.ROOT / "scripts/check-cache.py")
cache = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cache)


class PortableTests(unittest.TestCase):
    def test_archive_round_trip_and_repeat_preserve_release(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            release = root / "source/1234567890abcdef1234"
            skill = release / "skills/example/SKILL.md"
            fleetlib.atomic_write(skill, "portable content")
            manifest = {"revision": release.name, "skills": {"example": fleetlib.tree_hash(skill.parent)}}
            fleetlib.atomic_write(release / "manifest.json", fleetlib.encode(manifest))
            archive = root / "release.zip"
            checksum = portable.export_release(release, archive)
            target = portable.install_release(archive, checksum, root / "destination")
            self.assertEqual((target / "skills/example/SKILL.md").read_text(), "portable content")
            self.assertEqual(portable.install_release(archive, checksum, root / "destination"), target)
            with self.assertRaisesRegex(ValueError, "checksum"):
                portable.install_release(archive, "0" * 64, root / "destination")

    def test_archive_cannot_escape_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive = root / "bad.zip"
            with zipfile.ZipFile(archive, "w") as source:
                source.writestr("1234567890abcdef1234/../../outside", "bad")
            checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
            with self.assertRaisesRegex(ValueError, "Unsafe"):
                portable.install_release(archive, checksum, root / "destination")
            self.assertFalse((root / "outside").exists())

    def test_cache_report_uses_last_request_not_cumulative_session(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            totals = {"input_tokens": 30097, "cached_input_tokens": 25600}
            last = {"input_tokens": 15067, "cached_input_tokens": 14848}
            event = {"payload": {"type": "token_count", "info": {"total_token_usage": totals, "last_token_usage": last}}}
            (root / "rollout-own-session.jsonl").write_text(json.dumps(event) + "\n")
            self.assertEqual(cache.codex_last_request_usage("own-session", root), last)


if __name__ == "__main__":
    unittest.main()
