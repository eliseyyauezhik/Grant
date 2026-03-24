import os
import sys
import types
import unittest
from unittest import mock
from pathlib import Path

# Stub anthropic before importing the skill module.
ant_stub = types.SimpleNamespace(Anthropic=lambda *args, **kwargs: None)
sys.modules.setdefault("anthropic", ant_stub)

TEST_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = (TEST_DIR / ".." / "scripts").resolve()
sys.path.insert(0, str(SCRIPTS_DIR))

import skill  # noqa: E402
import logging  # noqa: E402

# Disable logging to avoid UnicodeEncodeError on cp1251 during tests.
logging.disable(logging.CRITICAL)


class TestYTDownloader(unittest.TestCase):
    def test_extract_id_watch(self):
        url = "https://www.youtube.com/watch?v=abcdefghijk"
        self.assertEqual(skill.YTDownloader._extract_id(url), "abcdefghijk")

    def test_extract_id_short(self):
        url = "https://youtu.be/ZYXWVUTSRQP"
        self.assertEqual(skill.YTDownloader._extract_id(url), "ZYXWVUTSRQP")

    def test_extract_id_invalid(self):
        url = "https://example.com/watch?v=notyoutube"
        self.assertIsNone(skill.YTDownloader._extract_id(url))

    def test_clean_vtt(self):
        raw = """WEBVTT\n\n00:00:00.000 --> 00:00:01.000\n<00:00:00.000><c>hello</c>\n\n00:00:01.000 --> 00:00:02.000\n<00:00:01.000><c>hello</c>\n<00:00:01.500><c>world</c>\n"""
        cleaned = skill.YTDownloader._clean_vtt(raw)
        self.assertIn("hello", cleaned)
        self.assertIn("world", cleaned)
        self.assertNotIn("WEBVTT", cleaned)
        self.assertNotIn("-->", cleaned)


class TestReportAggregation(unittest.TestCase):
    def _result(self, vid, trends, insights):
        return skill.AnalysisResult(
            video_id=vid,
            title="t",
            url="u",
            relevance_score=80,
            relevance_reason="r",
            categories=["c"],
            key_insights=insights,
            actionable_ideas=["a"],
            trends=trends,
            summary="s",
            mindmap={},
        )

    def test_aggregate_trends_dedup(self):
        rg = skill.ReportGenerator(Path("."))
        r1 = self._result("1", ["trend one", "trend two"], ["i1"])
        r2 = self._result("2", ["trend one extra"], ["i2"])
        out = rg._aggregate_trends([r1, r2])
        self.assertTrue(any("trend one" in t for t in out))
        self.assertTrue(any("trend two" in t for t in out))

    def test_aggregate_insights_dedup(self):
        rg = skill.ReportGenerator(Path("."))
        r1 = self._result("1", ["t1"], ["insight alpha"])
        r2 = self._result("2", ["t2"], ["insight alpha extended"])
        out = rg._aggregate_insights([r1, r2])
        self.assertTrue(any("insight alpha" in i for i in out))


class TestKnowledgeBase(unittest.TestCase):
    def test_kb_save_and_dedup(self):
        base = TEST_DIR / "tmp_kb"
        base.mkdir(parents=True, exist_ok=True)
        kb = skill.KnowledgeBase(base)

        r1 = skill.AnalysisResult(
            video_id="v1",
            title="t1",
            url="u1",
            relevance_score=70,
            relevance_reason="r",
            categories=["c"],
            key_insights=["insight"],
            actionable_ideas=["a"],
            trends=["trend"],
            summary="s",
            mindmap={},
        )
        r2 = skill.AnalysisResult(
            video_id="v2",
            title="t2",
            url="u2",
            relevance_score=75,
            relevance_reason="r",
            categories=["c"],
            key_insights=["insight"],
            actionable_ideas=["a"],
            trends=["trend"],
            summary="s",
            mindmap={},
        )
        kb.save([r1, r2], "report1")

        data = (base / "knowledge_base.json").read_text(encoding="utf-8")
        self.assertIn("v1", data)
        self.assertIn("v2", data)


class TestProviderConfig(unittest.TestCase):
    def test_invalid_provider_raises(self):
        with mock.patch.dict(os.environ, {"LLM_PROVIDER": "invalid-provider"}, clear=False):
            with self.assertRaises(RuntimeError):
                skill.AIAnalyzer()

    def test_gemini_missing_key_raises(self):
        fake_google_genai = types.SimpleNamespace(
            Client=lambda *args, **kwargs: object(),
        )
        with mock.patch.object(skill, "google_genai", fake_google_genai):
            with mock.patch.dict(
                os.environ,
                {"LLM_PROVIDER": "gemini"},
                clear=False,
            ):
                os.environ.pop("GEMINI_API_KEY", None)
                os.environ.pop("GOOGLE_API_KEY", None)
                with self.assertRaises(RuntimeError):
                    skill.AIAnalyzer()

if __name__ == "__main__":
    unittest.main()
