---
type: backlog
status: active
last_updated: 2026-04-26
tags:
  - backlog
  - reminders
  - goals
---

# 📋 My Backlog — Реестр задач, идей и целей

> ⚡ **Агент читает этот файл в начале каждой сессии** и напоминает о срочных/важных пунктах.
> Сюда вносятся: цели, идеи, задачи, блокеры — всё что нельзя потерять.

---

## 🔴 Срочно / На этой неделе

<!-- Задачи с конкретными дедлайнами или высоким приоритетом -->

- [ ] Рассмотреть и утвердить план модернизации Antigravity ([[projects/modernization-plan-review]]) — *обсуждено 2026-03-27*
- [ ] Рассмотреть и утвердить план модернизации Antigravity ([[projects/modernization-plan-review]]) — *обсуждено 2026-03-27*

---

## 🟡 Важно / Скоро (следующие 2–4 недели)

<!-- Решённые идеи, ожидающие реализации -->

- [ ] **Система памяти**: установить LightRAG на VPS, загрузить Obsidian KB в индекс — *добавлено 2026-04-24*
- [ ] **Brain Store Extractor**: извлечь знания из 1142 UUID-сессий `C:\Users\Admin\.gemini\antigravity\brain\` — *добавлено 2026-04-24*
- [ ] **Watchdog-демон**: автосинхронизация vault → dashboard при изменении .md файлов — *добавлено 2026-04-24*
- [ ] Добавить блок `## Current State` в `owner.md` (живой журнал состояния проектов)
- [ ] Написать `context_guide.md` — гайд как правильно давать задачу агенту
- [ ] Создать шаблон постобработки встречи (`.agents/templates/meeting-debrief-template.md`)
- [ ] Подготовить лаконичную инструкцию по работе с `OpenClaw` и `NemoClaw` после стабилизации инфраструктуры VPS
- [ ] `OpenClaw`: если понадобится внешний UI, настроить reverse proxy или Tailscale + `gateway.trustedProxies`
- [ ] `OpenClaw`: отправить тестовое голосовое сообщение и подтвердить voice pipeline после миграции `tools.media.audio`
- [ ] `OpenClaw`: визуально подтвердить в Telegram, что persistent menu button вернулся и owner-команды отображаются как ожидается
- [ ] `OpenClaw`: вручную проверить в Telegram `/model`, `/model haiku`, `/model sonnet` и убедиться, что новый диалог реально стартует на `Haiku`
- [ ] `Telegram DB analysis`: в новом чате прогнать сохранённый prompt-pack на экспорт Telegram-базы и собрать аналитический документ
- [ ] `OpenClaw`: проверить выводы из Telegram-анализа по официальным источникам (docs, changelog, issues, provider policies) и обновить итоговые тезисы
- [ ] Публикация статических страниц: закрепить fallback через GitHub Pages или Яндекс.Диск на случай упора в лимиты Netlify
- [ ] `Knowledge pipeline`: оформить reusable skill для верификации, triage, приоритизации и плана внедрения по Telegram/chat/database corpora
- [ ] `Knowledge pipeline`: разработать rubric ранжирования знаний по достоверности, применимости к проектам и ценности для `OpenClaw`
- [ ] `Аналитический Узел`: оформить единый pipeline `inbox -> corpus -> verification -> triage -> ranking -> write-back -> proactive signals`
- [ ] `Личный ИИ-ассистент`: читать обновления из vault/Obsidian, собирать сигналы развития по проектам и областям, предлагать следующие шаги и нужных агентов

---

## ✅ Выполнено

- [x] **Hermes: mem0 память** — mem0 cloud (91.6% accuracy) + redact_pii анонимизация — *выполнено 2026-04-26*
- [x] **Hermes VPS**: установка + Telegram gateway + auxiliary LLM fix — *выполнено 2026-04-26*
- [x] **SSH-ключ на VPS 85.234.100.31**: автономный доступ настроен — *выполнено 2026-04-26*

- [x] **BUG-1 sync_workspace_data.py**: circular dependency в projects.json разделён (input ≠ output) — *выполнено 2026-04-24*
- [x] **BUG-2 sync_workspace_data.py**: дедупликация notes segments — *выполнено 2026-04-24*
- [x] **BUG-3 sync_workspace_data.py**: нормализация workflow paths перед дедупликацией — *выполнено 2026-04-24*
- [x] **BUG-4 sync_workspace_data.py**: notebooklm теперь gated по env-флагу NOTEBOOKLM_AVAILABLE — *выполнено 2026-04-24*
- [x] **BUG-5 AGENTS.md**: priority cross-reference уже на месте (строка 1) — *проверено 2026-04-24*
- [x] **Codex инструкция**: создан `codex_instructions_2026-04-24.md` для VPS мультиагентности — *выполнено 2026-04-24*
- [x] **OpenClaw семантическая память**: решено использовать LightRAG (не чистый RAG), по рекомендации сообщества — *решено 2026-04-24*

---

## 💡 Parking Lot (идеи на потом)

- [ ] Weekly synthesis через n8n: каждую пятницу 18:00 → sync → `weekly_project_brief.md` → Telegram
- [ ] FastAPI Brain API (REST/WebSocket для Dashboard mutations)
- [ ] Smart Inbox Router через n8n
- [ ] Self-improving agents (только после стабильного write-back)
- [ ] **OpenAI Privacy Filter** — изучить и внедрить: https://github.com/openai/privacy-filter — *2026-04-25*
- [ ] **Обновить Linux на старом ноуте** + перенос данных на основной ПК + Яндекс Диск — *2026-04-25*
- [ ] **Hermes: Inbox Agent** — скилл для обработки сырых материалов из Telegram (Claude Haiku 4.5) — *2026-04-25*
- [ ] **Hermes: Monitor Agent** — cron мониторинг AI новостей каждые 2-3 дня → Telegram — *2026-04-25*
- [ ] **Hermes: Silero TTS** — голосовые ответы по-русски в Telegram — *2026-04-25*
- [ ] **GigaAM финализация** — добавить HuggingFace token для pyannote/segmentation-3.0 — *2026-04-25*
- [ ] **Hermes: субагенты** — code (Kimi K2), content (Qwen3 235B), data (DeepSeek R1) — *2026-04-25*
- [ ] **Ollama fallback** — локальная LLM на VPS (Qwen2.5-7B) как 3й уровень fallback — *2026-04-25*

---

## 🛠️ Как работать с бэклогом

| Действие | Как |
|---|---|
| Добавить идею | Написать агенту «запомни идею: ...» |
| Добавить задачу | Написать агенту «добавь в backlog: ...» с приоритетом |
| Пометить выполненным | Сказать агенту «закрой задачу [название]» |
| Просмотреть список | Открыть этот файл в Obsidian или спросить агента «что у меня в backlog?» |
