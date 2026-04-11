# Owner Profile

## Context and Roles

Entrepreneur. Building projects in education and EdTech.
Simultaneously building an AI infrastructure for automating personal
workflows (Antigravity system).
Based in Naberezhnye Chelny, Russia. Projects target the Russian market.

## Technical Level

Non-technical: limited understanding of architecture, cannot read or write code,
requires clear explanations. Can evaluate solutions on common sense but not on
syntax or implementation details.

## Working Style With Agents

Vibe-coding: provides ideas and success criteria, does not engage in implementation details.
Prefers autonomous agent work until completion.
Wants to participate only in key decisions and points of no return.
Values interactive checkpoints: periodic choice-based pauses where the agent
offers 2–3 clear, contrasting options for the user to pick from.

## Decision Priorities

1. A working MVP fast is more important than perfect architecture
2. Ease of maintenance is more important than feature completeness
3. Local deployment is preferred over cloud where possible
4. Minimize external dependencies and paid services
5. Russian-language documentation stack where there is a choice
6. If cloud — prefer Russian providers

## Active Projects

- SmartMeeting: meeting recording and processing service (backend ~60% ready)
- Phantom Davydov: AI assistant for a gymnasium, educational materials search engine
- Antigravity: personal AI operating system, knowledge base + agents
- Gymnasium landing: school website (maintenance)
- TGAggregator: Telegram channel news aggregator (paused)

## Domains and Interests

EdTech, education, AI agents, workflow automation,
local AI solutions, Telegram bots, B2B services for organizations.

## Hard Rules

- Do not refactor working code without explicit request
- Do not change stack or architecture without discussion at a point of no return
- Do not add features beyond what is described in the spec
- Do not create git commits without explicit permission
- Do not use paid external APIs without warning about cost
- Do not touch `.obsidian/` files or generated artifacts during agent sessions

## What the Agent Should Do Proactively

- Suggest a simpler solution if one exists before starting implementation
- Report risks and pitfalls before starting, not during
- For new projects, run the intake protocol (5 questions) before any code
- Stop at points of no return with 2 options + recommendation
- Signal T1–T3 protocol triggers directly in chat

## Current State (updated: 2026-03-27)

### 🔥 Активные задачи

#### 🤖 Настройка OpenClaw на сервере 4vps

- Статус: **НЕ НАЧАТО — требует действий**
- Приоритет: Высокий
- Описание: Развернуть OpenClaw (AI-оркестратор) на VPS-сервере (4vps.ru) под управлением Linux Ubuntu.
- Задачи:
  - [ ] Подключиться к серверу 4vps по SSH (получить данные доступа)
  - [ ] Установить Node.js (среда выполнения для OpenClaw)
  - [ ] Установить OpenClaw через npm: `npm install -g openclaw@latest`
  - [ ] Запустить первичную конфигурацию: `openclaw onboard --install-daemon`
  - [ ] Добавить API-ключ (Claude Sonnet или GPT-4o — на выбор)
  - [ ] Подключить Telegram-канал как интерфейс управления агентом
  - [ ] Настроить базовые навыки (Skills): веб-поиск, работа с файлами
  - [ ] Протестировать: дать агенту первую задачу через Telegram
  - [ ] (Бонус, день 2) Установить NVIDIA NemoClaw — защитный слой поверх OpenClaw: `curl -fsSL https://www.nvidia.com/nemoclaw.sh | bash`
  - [ ] (Опционально) Подключить GigaChat/YandexGPT как альтернативу западным API
  - [ ] (Опционально) Добавить навыки для Яндекс 360 (Диск, Почта, Календарь)
- Источник: Анализ `D:\ЯндексДиск\Yandex.Disk\ПРОЕКТЫ\KnowledgeBase\Inbox\OpenClaw\Российские сервисы OpenClaw_ анализ.txt`
- Инструкция: `D:\ЯндексДиск\Yandex.Disk\ПРОЕКТЫ\KnowledgeBase\Projects\AI Workspace\openclaw-4vps-setup-guide.md`

### 🗂 Parking Lot (отложенные идеи)

- Интеграция OpenClaw с российскими AI (GigaChat через gpt2giga прокси, YandexGPT)
- Навык yax для Яндекс 360 (Диск, Почта, Telemost)
- Marketplace-ru навык (Wildberries, Ozon, Яндекс Маркет)

---

## Communication Preferences

- Language: Russian by default in this workspace
- Format: concise, no fluff, structured
- Code: minimal comments only where non-obvious
- When uncertain: offer 2–3 options with a clear recommendation, do not guess silently
- Interactive pauses: periodically offer choice-based checkpoints
  (e.g., "Option A / Option B / Option C — which do you prefer?")
  to maintain alignment with the owner
