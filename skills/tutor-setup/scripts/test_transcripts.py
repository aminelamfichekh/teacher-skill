"""Behavior checks with synthetic media only; no network or dependencies."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("transcripts.py")


class TranscriptTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def run_cli(self, *args, success=True):
        result = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                                capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0 if success else 1, result.stderr)
        return json.loads(result.stdout) if success else result.stderr

    def ingest(self, path, source="v01", **kwargs):
        args = ["ingest", "--input", path, "--output", self.root / "sources" / source,
                "--source-id", source]
        return self.run_cli(*args, **kwargs)

    def test_ten_two_hour_videos_retrievable_to_exact_cues(self):
        for i in range(10):
            path = self.root / f"v{i}.json"
            rows = [{"start": s, "end": s + 30, "text": f"topic{i} segment {s}"}
                    for s in range(0, 7200, 30)]
            path.write_text(json.dumps(rows), encoding="utf-8")
            result = self.run_cli("ingest", "--input", path, "--output",
                                  self.root / "sources" / f"v{i}", "--source-id", f"v{i}",
                                  "--duration", "7200")
            self.assertEqual(result["cues"], 240)
            self.assertEqual(result["chunks"], 24)
            self.assertEqual(result["coverage"]["covered_seconds"], 7200)
            self.assertEqual(result["coverage"]["timestamp_gaps"], [])
        self.assertEqual(self.run_cli("check", "--root", self.root / "sources")["validated_indexes"], 10)
        found = self.run_cli("search", "--root", self.root / "sources", "--query", "topic7", "--limit", 1)
        self.assertEqual(found[0]["source_id"], "v7")
        cues = json.loads((Path(found[0]["index_path"]).parent / "cues.json").read_text())
        cited = {c["cue_id"]: c for c in cues}
        self.assertTrue(all(cid in cited for cid in found[0]["cue_ids"]))
        self.assertEqual(found[0]["start"], cited[found[0]["cue_ids"][0]]["start"])

    def test_srt_hours_overlap_and_gap_union(self):
        path = self.root / "test.srt"
        path.write_text("1\n01:00:00,000 --> 01:00:10,000\nα &amp; β\n\n"
                        "2\n01:00:05,000 --> 01:00:20,000\nOverlap\n", encoding="utf-8")
        result = self.ingest(path)
        self.assertEqual(result["coverage"]["covered_seconds"], 20)
        self.assertEqual(result["coverage"]["overlapping_cues"], 1)
        self.assertEqual(result["coverage"]["timestamp_gaps"], [[0, 3600]])
        cues = json.loads((self.root / "sources/v01/cues.json").read_text(encoding="utf-8"))
        self.assertEqual(cues[0]["text"], "α & β")
        found = self.run_cli("search", "--root", self.root / "sources", "--query", "α")
        self.assertIn("α & β", found[0]["text"])
        self.ingest(path, success=False)  # immutable existing revision

    def test_vtt_settings_and_notes(self):
        path = self.root / "test.vtt"
        path.write_text("WEBVTT\n\nNOTE generated fixture\nnot a cue\n\n"
                        "cue-A\n00:01.000 --> 00:03.500 align:start\n<b>Hello</b>\n", encoding="utf-8")
        self.ingest(path)
        result = self.run_cli("search", "--root", self.root / "sources", "--query", "hello")
        self.assertEqual(result[0]["start"], 1)
        self.assertEqual(result[0]["end"], 3.5)

    def test_reject_invalid_and_untimed_without_outputs(self):
        for i, data in enumerate(([{"start": 9, "end": 3, "text": "bad"}],
                                  [{"start": -1, "end": 3, "text": "bad"}],
                                  [{"start": 0, "end": float("nan"), "text": "bad"}],
                                  [{"start": 0, "end": 1, "text": ""}],
                                  [{"start": 5, "end": 7, "text": "a"},
                                   {"start": 2, "end": 3, "text": "b"}])):
            path = self.root / f"bad{i}.json"
            path.write_text(json.dumps(data))
            self.ingest(path, source=f"bad{i}", success=False)
            self.assertFalse((self.root / "sources" / f"bad{i}").exists())
        path = self.root / "untimed.txt"
        path.write_text("Text without times")
        self.ingest(path, success=False)

    def test_duration_tampering_and_partial_ingestion(self):
        path = self.root / "test.json"
        path.write_text('[{"start":0,"end":10,"text":"valid"}]')
        self.run_cli("ingest", "--input", path, "--output", self.root / "too-short",
                     "--source-id", "short", "--duration", 5, success=False)
        self.ingest(path)
        chunks_path = self.root / "sources/v01/chunks.json"
        chunks = json.loads(chunks_path.read_text())
        chunks[0]["end"] = 500
        chunks_path.write_text(json.dumps(chunks))
        self.assertIn("chunk mismatch", self.run_cli("check", "--root", self.root / "sources", success=False))
        self.ingest(path, source="v02")
        (self.root / "sources/v02/index.json").unlink()
        self.assertIn("incomplete", self.run_cli("check", "--root", self.root / "sources", success=False))

    def test_original_hash_and_raw_only_interruption(self):
        path = self.root / "test.json"
        path.write_text('[{"start":0,"end":10,"text":"valid"}]')
        self.ingest(path)
        original = self.root / "sources/v01/original.json"
        original.write_text('[{"start":0,"end":10,"text":"changed"}]')
        self.assertIn("hash mismatch", self.run_cli("check", "--root", self.root / "sources", success=False))
        self.ingest(path, source="v02")
        (self.root / "sources/v02/index.json").unlink()
        (self.root / "sources/v02/cues.json").unlink()
        (self.root / "sources/v02/chunks.json").unlink()
        self.assertIn("incomplete", self.run_cli("check", "--root", self.root / "sources", success=False))


if __name__ == "__main__":
    unittest.main()
