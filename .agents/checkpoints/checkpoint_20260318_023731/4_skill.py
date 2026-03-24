"""
╔══════════════════════════════════════════════════════════════════════╗
║          YT_Analyzer_v1 — Antigravity YouTube Monitor Skill          ║
║          Part of: Antigravity Vibe-Programming System                ║
║          Version: 1.0.0  |  Author: Claude Opus 4.6                 ║
╚══════════════════════════════════════════════════════════════════════╝

USAGE:
    from skill import YT_Analyzer_v1
    await YT_Analyzer_v1(
        "https://youtube.com/playlist?list=...",
        criteria="ИИ-агенты и vibe-программирование"
    )
"""

import asyncio
import json
import os
import re
import subprocess
import logging
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional
try:
    import anthropic
except ImportError:
    anthropic = None

try:
    from google import genai as google_genai
except ImportError:
    google_genai = None

# ─────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"
AUDIO_DIR = BASE_DIR / "audio"

for d in [KNOWLEDGE_BASE_DIR, REPORTS_DIR, LOGS_DIR, AUDIO_DIR]:
    d.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOGS_DIR / f"yt_analyzer_{datetime.now():%Y%m%d}.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("YT_Analyzer_v1")

DEFAULT_LLM_PROVIDER = "gemini"
DEFAULT_ANTHROPIC_MODEL = "claude-opus-4-6"
DEFAULT_GEMINI_MODEL = "gemini-2.5-pro"
MAX_RETRIES = 3
CHUNK_SIZE = 80_000   # chars per transcript chunk


# ─────────────────────────────────────────────
#  DATA MODELS
# ─────────────────────────────────────────────
@dataclass
class VideoMeta:
    url: str
    video_id: str
    title: str
    channel: str
    duration: int
    view_count: int
    like_count: int
    upload_date: str
    description: str
    transcript: str = ""
    comments: list = field(default_factory=list)
    tags: list = field(default_factory=list)


@dataclass
class AnalysisResult:
    video_id: str
    title: str
    url: str
    relevance_score: int          # 0-100
    relevance_reason: str
    categories: list              # multi-label
    key_insights: list
    actionable_ideas: list
    trends: list
    summary: str
    mindmap: dict
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


# ─────────────────────────────────────────────
#  STEP 1-2: yt-dlp DOWNLOAD ENGINE
# ─────────────────────────────────────────────
class YTDownloader:
    """Downloads transcripts, metadata, comments via yt-dlp"""

    def __init__(self, output_dir: Path):
        self.out = output_dir
        self.out.mkdir(parents=True, exist_ok=True)

    def _run(self, cmd: list, retries=MAX_RETRIES) -> tuple[str, str]:
        for attempt in range(retries):
            try:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                if r.returncode == 0:
                    return r.stdout, r.stderr
                log.warning(f"yt-dlp attempt {attempt+1} failed: {r.stderr[:200]}")
            except subprocess.TimeoutExpired:
                log.warning(f"Timeout on attempt {attempt+1}")
            time.sleep(2 ** attempt)
        raise RuntimeError(f"yt-dlp failed after {retries} attempts")

    def get_playlist_urls(self, url: str) -> list[str]:
        """Extract all video URLs from playlist/channel/single video"""
        cmd = ["yt-dlp", "--flat-playlist", "-J", "--no-warnings", url]
        stdout, _ = self._run(cmd)
        data = json.loads(stdout)

        if data.get("_type") == "playlist":
            entries = data.get("entries", [])
            return [f"https://www.youtube.com/watch?v={e['id']}"
                    for e in entries if e.get("id")]
        elif data.get("_type") == "video" or "id" in data:
            return [url]
        return []

    def download_video_data(self, url: str) -> Optional[VideoMeta]:
        """Download metadata + transcript for a single video"""
        vid_id = self._extract_id(url)
        if not vid_id:
            return None

        # --- Metadata ---
        cmd = ["yt-dlp", "-J", "--no-warnings", url]
        stdout, _ = self._run(cmd)
        meta = json.loads(stdout)

        # --- Transcript (auto-subs preferred, then manual) ---
        transcript = self._get_transcript(url, vid_id)

        # --- Comments (top 100) ---
        comments = self._get_comments(url)

        return VideoMeta(
            url=url,
            video_id=vid_id,
            title=meta.get("title", ""),
            channel=meta.get("channel", meta.get("uploader", "")),
            duration=meta.get("duration", 0),
            view_count=meta.get("view_count", 0),
            like_count=meta.get("like_count", 0),
            upload_date=meta.get("upload_date", ""),
            description=(meta.get("description") or "")[:2000],
            transcript=transcript,
            comments=comments,
            tags=meta.get("tags", [])[:30],
        )

    def _get_transcript(self, url: str, vid_id: str) -> str:
        sub_path = self.out / f"{vid_id}.vtt"
        # Try auto-generated subtitles first
        for lang in ["ru", "en"]:
            cmd = [
                "yt-dlp", "--write-auto-subs", "--sub-lang", lang,
                "--sub-format", "vtt", "--skip-download",
                "-o", str(self.out / "%(id)s"), url
            ]
            self._run(cmd)
            if sub_path.exists():
                raw = sub_path.read_text(encoding="utf-8", errors="ignore")
                return self._clean_vtt(raw)
        return ""

    def _get_comments(self, url: str) -> list[str]:
        cmd = [
            "yt-dlp", "--write-comments", "--skip-download",
            "--extractor-args", "youtube:comment_sort=top;max_comments=100",
            "-o", str(self.out / "%(id)s_comments"), url
        ]
        try:
            self._run(cmd)
        except Exception:
            pass
        comments_files = list(self.out.glob("*_comments.info.json"))
        if comments_files:
            data = json.loads(comments_files[-1].read_text())
            return [c.get("text", "") for c in data.get("comments", [])[:50]]
        return []

    @staticmethod
    def _extract_id(url: str) -> Optional[str]:
        m = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", url)
        return m.group(1) if m else None

    @staticmethod
    def _clean_vtt(raw: str) -> str:
        lines = []
        seen = set()
        for line in raw.split("\n"):
            line = line.strip()
            if "-->" in line or not line or line.startswith("WEBVTT"):
                continue
            # Strip VTT tags
            clean = re.sub(r"<[^>]+>", "", line)
            if clean and clean not in seen:
                seen.add(clean)
                lines.append(clean)
        return " ".join(lines)


# ─────────────────────────────────────────────
#  STEP 3-6: AI ANALYSIS ENGINE (Claude Opus)
# ─────────────────────────────────────────────
class AIAnalyzer:
    """Multi-step analysis pipeline using a configured LLM provider."""

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", DEFAULT_LLM_PROVIDER).strip().lower()
        self.client = None
        self.model = None

        if self.provider == "anthropic":
            if anthropic is None:
                raise RuntimeError(
                    "LLM_PROVIDER=anthropic but the 'anthropic' package is not installed."
                )
            self.client = anthropic.Anthropic()
            self.model = os.getenv("ANTHROPIC_MODEL", DEFAULT_ANTHROPIC_MODEL)
            return

        if self.provider == "gemini":
            if google_genai is None:
                raise RuntimeError(
                    "LLM_PROVIDER=gemini but the 'google-genai' package is not installed."
                )
            api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise RuntimeError(
                    "Missing GEMINI_API_KEY (or GOOGLE_API_KEY) for Gemini provider."
                )
            self.model = os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)
            self.client = google_genai.Client(api_key=api_key)
            return

        raise RuntimeError(
            f"Unsupported LLM_PROVIDER='{self.provider}'. Use 'gemini' or 'anthropic'."
        )

    def _call_gemini(self, system: str, user: str, max_tokens: int) -> str:
        prompt = f"{system}\n\n{user}".strip()
        resp = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={"max_output_tokens": max_tokens},
        )
        text = getattr(resp, "text", None)
        if text:
            return text
        raise RuntimeError("Gemini returned an empty response")

    def _call(self, system: str, user: str, max_tokens=4096) -> str:
        for attempt in range(MAX_RETRIES):
            try:
                if self.provider == "anthropic":
                    msg = self.client.messages.create(
                        model=self.model,
                        max_tokens=max_tokens,
                        system=system,
                        messages=[{"role": "user", "content": user}],
                    )
                    return msg.content[0].text
                return self._call_gemini(system, user, max_tokens)
            except Exception as e:
                log.warning(f"{self.provider} API call attempt {attempt+1} failed: {e}")
                time.sleep(2 ** attempt)
        raise RuntimeError(f"{self.provider} API failed after retries")

    def analyze_video(self, meta: VideoMeta, criteria: str) -> AnalysisResult:
        """Run all analysis steps for one video"""
        log.info(f"  Analyzing: {meta.title[:60]}...")

        # Chunk transcript if too large
        transcript_chunks = self._chunk_text(meta.transcript)
        transcript_summary = self._summarize_chunks(transcript_chunks, meta.title)

        # STEP 3: Categories
        categories = self._categorize(meta, criteria)

        # STEP 4: Relevance score
        score, reason = self._score_relevance(meta, criteria, transcript_summary)

        # STEP 5: Insights, trends, ideas
        insights, trends, ideas = self._extract_insights(
            meta, criteria, transcript_summary
        )

        # STEP 6: Summary + mind-map
        summary = self._generate_summary(meta, transcript_summary, criteria)
        mindmap = self._generate_mindmap(meta.title, insights, trends, ideas)

        return AnalysisResult(
            video_id=meta.video_id,
            title=meta.title,
            url=meta.url,
            relevance_score=score,
            relevance_reason=reason,
            categories=categories,
            key_insights=insights,
            actionable_ideas=ideas,
            trends=trends,
            summary=summary,
            mindmap=mindmap,
        )

    # ── Chunking ───────────────────────────────
    @staticmethod
    def _chunk_text(text: str) -> list[str]:
        if not text:
            return []
        return [text[i:i+CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]

    def _summarize_chunks(self, chunks: list[str], title: str) -> str:
        if not chunks:
            return ""
        if len(chunks) == 1:
            return chunks[0]
        summaries = []
        for i, chunk in enumerate(chunks):
            s = self._call(
                "Ты — суммаризатор транскриптов YouTube. Кратко (3-5 предложений) изложи ключевые идеи этого фрагмента.",
                f"Видео: {title}\nФрагмент {i+1}/{len(chunks)}:\n{chunk}"
            )
            summaries.append(s)
        return "\n\n".join(summaries)

    # ── Analysis steps ─────────────────────────
    def _categorize(self, meta: VideoMeta, criteria: str) -> list[str]:
        resp = self._call(
            "Ты — классификатор контента. Отвечай ТОЛЬКО JSON-массивом строк. Без пояснений.",
            f"""Критерии интереса: {criteria}
Видео: {meta.title}
Описание: {meta.description[:500]}
Теги: {', '.join(meta.tags[:15])}

Выдай JSON-массив категорий из критериев, которым соответствует видео. Пример: ["ИИ-агенты", "Claude API"]"""
        )
        try:
            return json.loads(resp.strip())
        except Exception:
            return [criteria.split(",")[0].strip()]

    def _score_relevance(self, meta: VideoMeta, criteria: str, transcript: str) -> tuple[int, str]:
        resp = self._call(
            'Ты — эксперт по оценке релевантности. Отвечай ТОЛЬКО JSON: {"score": 0-100, "reason": "..."}',
            f"""Критерии интереса: {criteria}
Заголовок: {meta.title}
Канал: {meta.channel}
Просмотры: {meta.view_count:,}
Транскрипт (краткое): {transcript[:2000]}

Оцени релевантность видео для указанных критериев от 0 до 100. Объясни ПОЧЕМУ именно такой score."""
        )
        try:
            data = json.loads(resp.strip())
            return int(data["score"]), data["reason"]
        except Exception:
            return 50, "Не удалось определить точную релевантность"

    def _extract_insights(self, meta: VideoMeta, criteria: str, transcript: str) -> tuple[list, list, list]:
        resp = self._call(
            'Отвечай ТОЛЬКО JSON: {"insights": [...], "trends": [...], "ideas": [...]}',
            f"""Критерии интереса: {criteria}
Видео: {meta.title}

Транскрипт:
{transcript[:6000]}

Комментарии (топ):
{chr(10).join(meta.comments[:10])}

Извлеки:
- insights: 5-7 ключевых инсайтов (конкретные факты/концепции)
- trends: 3-5 трендов, упомянутых в видео
- ideas: 3-5 actionable идей, которые можно применить

Каждый элемент — строка на русском языке.""",
            max_tokens=2048
        )
        try:
            data = json.loads(resp.strip())
            return data.get("insights", []), data.get("trends", []), data.get("ideas", [])
        except Exception:
            return [], [], []

    def _generate_summary(self, meta: VideoMeta, transcript: str, criteria: str) -> str:
        return self._call(
            "Ты — аналитик AI-контента. Пиши кратко, по делу, на русском языке.",
            f"""Критерии мониторинга: {criteria}
Видео: {meta.title} | Канал: {meta.channel}
Дата: {meta.upload_date} | Просмотры: {meta.view_count:,}

Транскрипт (краткое):
{transcript[:4000]}

Напиши исполнительское резюме (executive summary) на 150-200 слов.
Структура: [Тема] → [Главные идеи] → [Почему важно для {criteria}] → [Вывод]""",
            max_tokens=1024
        )

    def _generate_mindmap(self, title: str, insights: list, trends: list, ideas: list) -> dict:
        return {
            "root": title,
            "branches": {
                "🔍 Ключевые инсайты": insights,
                "📈 Тренды": trends,
                "💡 Actionable идеи": ideas,
            }
        }


# ─────────────────────────────────────────────
#  STEP 7: REPORT GENERATOR
# ─────────────────────────────────────────────
class ReportGenerator:
    def __init__(self, reports_dir: Path):
        self.dir = reports_dir

    def generate(self, results: list[AnalysisResult], criteria: str, source_url: str) -> dict:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_id = f"YT_Report_{ts}"

        # Sort by relevance
        sorted_results = sorted(results, key=lambda r: r.relevance_score, reverse=True)
        top = [r for r in sorted_results if r.relevance_score >= 60]

        report = {
            "report_id": report_id,
            "generated_at": datetime.now().isoformat(),
            "source_url": source_url,
            "criteria": criteria,
            "total_videos": len(results),
            "high_relevance_count": len(top),
            "average_score": round(sum(r.relevance_score for r in results) / max(len(results), 1), 1),
            "top_videos": [asdict(r) for r in sorted_results[:10]],
            "all_trends": self._aggregate_trends(results),
            "all_insights": self._aggregate_insights(results),
            "skill_version": "YT_Analyzer_v1",
        }

        # Save JSON
        json_path = self.dir / f"{report_id}.json"
        json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2))

        # Save Markdown
        md_path = self.dir / f"{report_id}.md"
        md_path.write_text(self._to_markdown(report, sorted_results), encoding="utf-8")

        log.info(f"✅ Report saved: {json_path}")
        return report

    def _aggregate_trends(self, results: list[AnalysisResult]) -> list[str]:
        all_trends = []
        for r in results:
            all_trends.extend(r.trends)
        # Deduplicate similar
        seen, out = set(), []
        for t in all_trends:
            key = t[:40].lower()
            if key not in seen:
                seen.add(key)
                out.append(t)
        return out[:20]

    def _aggregate_insights(self, results: list[AnalysisResult]) -> list[str]:
        all_insights = []
        for r in results:
            all_insights.extend(r.key_insights)
        seen, out = set(), []
        for i in all_insights:
            key = i[:40].lower()
            if key not in seen:
                seen.add(key)
                out.append(i)
        return out[:30]

    def _to_markdown(self, report: dict, results: list[AnalysisResult]) -> str:
        lines = [
            f"# 📊 YT Monitor Report: {report['report_id']}",
            f"> **Критерии:** {report['criteria']}  ",
            f"> **Источник:** {report['source_url']}  ",
            f"> **Дата:** {report['generated_at'][:19]}  ",
            f"> **Видео:** {report['total_videos']} | **Релевантных (60+):** {report['high_relevance_count']} | **Ср. score:** {report['average_score']}",
            "",
            "---",
            "",
            "## 🔥 Топ видео по релевантности",
            "",
        ]
        for i, r in enumerate(results[:10], 1):
            score_bar = "█" * (r.relevance_score // 10) + "░" * (10 - r.relevance_score // 10)
            lines += [
                f"### {i}. {r.title}",
                f"**Relevance:** `{r.relevance_score}/100` `{score_bar}`  ",
                f"**URL:** {r.url}  ",
                f"**Категории:** {', '.join(r.categories)}  ",
                "",
                f"**📝 Summary:**  ",
                r.summary,
                "",
                f"**🔍 Ключевые инсайты:**",
            ]
            for ins in r.key_insights[:5]:
                lines.append(f"- {ins}")
            lines += [
                "",
                f"**💡 Actionable идеи:**",
            ]
            for idea in r.actionable_ideas[:3]:
                lines.append(f"- {idea}")
            lines.append("\n---\n")

        lines += [
            "## 📈 Агрегированные тренды",
            "",
        ]
        for t in report["all_trends"][:15]:
            lines.append(f"- {t}")

        lines += [
            "",
            "## 🧠 Лучшие инсайты из всего контента",
            "",
        ]
        for ins in report["all_insights"][:20]:
            lines.append(f"- {ins}")

        lines += [
            "",
            "---",
            f"*Сгенерировано: YT_Analyzer_v1 powered by Claude Opus 4.6*",
        ]
        return "\n".join(lines)


# ─────────────────────────────────────────────
#  STEP 8: KNOWLEDGE BASE
# ─────────────────────────────────────────────
class KnowledgeBase:
    def __init__(self, kb_dir: Path):
        self.path = kb_dir / "knowledge_base.json"
        self.data: dict = self._load()

    def _load(self) -> dict:
        if self.path.exists():
            return json.loads(self.path.read_text())
        return {"videos": {}, "trends": [], "insights": [], "last_updated": ""}

    def save(self, results: list[AnalysisResult], report_id: str):
        for r in results:
            self.data["videos"][r.video_id] = {
                "title": r.title,
                "url": r.url,
                "score": r.relevance_score,
                "categories": r.categories,
                "summary": r.summary,
                "report_id": report_id,
                "added_at": r.timestamp,
            }
        # Merge trends / insights
        for t in results:
            self.data["trends"].extend(t.trends)
            self.data["insights"].extend(t.key_insights)

        # Deduplicate
        self.data["trends"] = list(dict.fromkeys(self.data["trends"]))[:500]
        self.data["insights"] = list(dict.fromkeys(self.data["insights"]))[:500]
        self.data["last_updated"] = datetime.now().isoformat()

        self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=2))
        log.info(f"📚 Knowledge base updated: {len(self.data['videos'])} videos total")


# ─────────────────────────────────────────────
#  SELF-IMPROVEMENT LOOP (STEP 13+)
# ─────────────────────────────────────────────
class SelfImprovementEngine:
    """Analyzes past performance and suggests prompt/pipeline improvements"""

    def __init__(self):
        self.analyzer = AIAnalyzer()
        self.log_path = LOGS_DIR / "improvement_suggestions.md"

    def reflect(self, results: list[AnalysisResult], criteria: str):
        """After each run, reflect on quality and suggest improvements"""
        scores = [r.relevance_score for r in results]
        low_score_titles = [r.title for r in results if r.relevance_score < 40]

        reflection_prompt = f"""Ты — self-improvement агент для YT_Analyzer_v1.

Статистика текущего прогона:
- Всего видео: {len(results)}
- Средний score: {sum(scores)/max(len(scores),1):.1f}
- Видео с низким score (<40): {len(low_score_titles)}
- Примеры низко-оцененных: {low_score_titles[:3]}
- Критерии: {criteria}

Проанализируй:
1. Могут ли критерии быть неточными или слишком широкими?
2. Какие промпты нужно улучшить?
3. Какие шаги пайплайна можно оптимизировать?
4. Предложи конкретные изменения (3-5 пунктов).

Формат: Markdown список улучшений."""

        suggestion = self.analyzer._call(
            "Ты — эксперт по улучшению пайплайнов анализа YouTube-контента.",
            reflection_prompt,
            max_tokens=1024,
        )

        entry = f"\n\n## {datetime.now().isoformat()} | Criteria: {criteria}\n\n{suggestion}"
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(entry)
        log.info("🔄 Self-improvement suggestions saved")
        return suggestion


# ─────────────────────────────────────────────
#  MAIN ENTRY POINT
# ─────────────────────────────────────────────
async def YT_Analyzer_v1(
    url: str,
    criteria: str = "ИИ-агенты, vibe-программирование, Claude, Gemini, автоматизация",
    min_score: int = 0,
    max_videos: int = 50,
    self_improve: bool = True,
) -> dict:
    """
    🎯 Main entry point for YT_Analyzer_v1

    Args:
        url: YouTube video / playlist / channel URL
        criteria: Comma-separated topics of interest (in any language)
        min_score: Only include results with score >= this value
        max_videos: Max videos to process (for large playlists)
        self_improve: Run self-improvement reflection after analysis

    Returns:
        Full report dict
    """
    start_time = time.time()
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    log.info(f"\n{'='*60}")
    log.info(f"🚀 YT_Analyzer_v1 START | run_id={run_id}")
    log.info(f"   URL: {url}")
    log.info(f"   Criteria: {criteria}")
    log.info(f"{'='*60}\n")

    work_dir = BASE_DIR / "downloads" / run_id
    work_dir.mkdir(parents=True, exist_ok=True)

    downloader = YTDownloader(work_dir)
    analyzer = AIAnalyzer()
    reporter = ReportGenerator(REPORTS_DIR)
    kb = KnowledgeBase(KNOWLEDGE_BASE_DIR)

    results = []
    errors = []

    try:
        # ── STEP 1: Get URLs ──────────────────────────
        log.info("📥 STEP 1: Collecting video URLs...")
        video_urls = downloader.get_playlist_urls(url)
        if not video_urls:
            video_urls = [url]
        video_urls = video_urls[:max_videos]
        log.info(f"   Found {len(video_urls)} videos")

        # ── STEP 2: Download each video ───────────────
        log.info("📥 STEP 2: Downloading transcripts & metadata...")
        metas = []
        for i, vurl in enumerate(video_urls, 1):
            log.info(f"  [{i}/{len(video_urls)}] Downloading: {vurl}")
            try:
                meta = downloader.download_video_data(vurl)
                if meta:
                    metas.append(meta)
            except Exception as e:
                log.error(f"  ❌ Download failed for {vurl}: {e}")
                errors.append({"url": vurl, "step": "download", "error": str(e)})

        # ── STEPS 3-6: Analyze each video ─────────────
        log.info(f"\n🧠 STEPS 3-6: AI Analysis of {len(metas)} videos...")
        for i, meta in enumerate(metas, 1):
            log.info(f"  [{i}/{len(metas)}] {meta.title[:50]}...")
            try:
                result = analyzer.analyze_video(meta, criteria)
                if result.relevance_score >= min_score:
                    results.append(result)
                    log.info(f"    ✅ Score: {result.relevance_score}/100 | Categories: {result.categories}")
                else:
                    log.info(f"    ⏭ Score {result.relevance_score} below min_score {min_score}, skipped")
            except Exception as e:
                log.error(f"  ❌ Analysis failed: {e}")
                errors.append({"url": meta.url, "step": "analysis", "error": str(e)})

        # ── STEP 7: Generate report ────────────────────
        log.info("\n📊 STEP 7: Generating report...")
        report = reporter.generate(results, criteria, url)
        report["errors"] = errors

        # ── STEP 8: Save to knowledge base ────────────
        log.info("📚 STEP 8: Saving to knowledge base...")
        kb.save(results, report["report_id"])

        # ── STEPS 9-12: Logging & notifications ───────
        elapsed = time.time() - start_time
        log.info(f"\n{'='*60}")
        log.info(f"✅ COMPLETE | {len(results)} videos analyzed | {elapsed:.1f}s")
        log.info(f"   Report: {REPORTS_DIR / report['report_id']}.json")
        log.info(f"   Avg relevance score: {report['average_score']}")
        log.info(f"   High relevance (60+): {report['high_relevance_count']}")
        if errors:
            log.warning(f"   ⚠️  Errors: {len(errors)}")
        log.info(f"{'='*60}\n")

        report["elapsed_seconds"] = round(elapsed, 2)
        report["run_id"] = run_id

        # ── STEP 13: Self-improvement ──────────────────
        if self_improve and results:
            log.info("🔄 STEP 13: Running self-improvement reflection...")
            try:
                engine = SelfImprovementEngine()
                suggestions = engine.reflect(results, criteria)
                report["improvement_suggestions"] = suggestions
            except Exception as e:
                log.warning(f"Self-improvement skipped: {e}")

        return report

    except Exception as e:
        log.critical(f"💥 CRITICAL ERROR: {e}", exc_info=True)
        raise


# ─────────────────────────────────────────────
#  CLI RUNNER
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    criteria = sys.argv[2] if len(sys.argv) > 2 else "ИИ-агенты, vibe-программирование, автоматизация"

    report = asyncio.run(YT_Analyzer_v1(url, criteria=criteria))
    print(f"\n🎯 Report ID: {report['report_id']}")
    print(f"📊 Analyzed: {report['total_videos']} videos")
    print(f"⭐ Avg Score: {report['average_score']}")
