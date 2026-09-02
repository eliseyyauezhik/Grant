# Handover: Донастройка AI-системы и переход OpenClaw → Hermes
**Дата:** 2026-04-25 | **Conversation ID:** `8621ed10-ebb4-41b2-b94d-ebbed30c8499`  
**Статус:** ⏸ PAUSED — ожидает действий пользователя  
**Следующий шаг:** Пользователь проверяет VPS на 4vps.su, после чего начинается установка Hermes

---

## 🔑 Сигнал для нового чата

> **Скажи в новом чате:** `продолжаем handover_2026-04-25_ai-system-upgrade` — агент прочитает этот файл и будет в курсе всего контекста.

---

## 📋 Что обсуждалось (хронология)

### Фаза 1: Анализ текущей системы
- Пользователь попросил проанализировать все источники и подготовить план донастройки AI-системы
- **Проанализировано:**
  - 10 файлов Telegram-экспорта OpenClaw Lab Community (17000+ сообщений)
  - Файлы KB из `workspace/` (~39 КБ)
  - Локальный конфиг VPS (`openclaw_vps.json`)
  - Инструкция `codex_instructions_2026-04-24.md`
  - Habr-статья с независимым обзором (https://habr.com/ru/articles/1026926/)
  - GitHub README Hermes Agent (116K ⭐)
  - 10 предыдущих conversation logs по теме OpenClaw

### Фаза 2: Обнаружение 4 багов в sync_workspace_data.py
Попутно обнаружены и **исправлены** 4 бага:

| # | Баг | Файл | Строки |
|---|-----|------|--------|
| BUG-1 | Circular dependency — projects.json использовался и как input и как output | `sync_workspace_data.py` | :798-823 |
| BUG-2 | Дублирование notes ×39 раз | `sync_workspace_data.py` | :2078-2090 |
| BUG-3 | Workflow paths без нормализации (ошибки в Windows) | `sync_workspace_data.py` | :2049-2060 |
| BUG-4 | NotebookLM вызов без проверки доступности → crash | `sync_workspace_data.py` | :585-592 |

### Фаза 3: Попытка настроить VPS
- SSH к `root@147.45.67.249` — **таймаут**
- Ping — 100% packet loss
- Port scan (22, 80, 443, 8080, 18789) — все порты закрыты
- **Вывод:** VPS выключен (оплаченный период истёк)

### Фаза 4: Стратегическое решение — OpenClaw vs Hermes
Пользователь выяснил, что VPS-оплата истекла, и попросил проанализировать альтернативы.

**Главное открытие:** массовый переход сообщества с OpenClaw на Hermes Agent (24-25 апреля 2026).

---

## 🎯 Принятые решения

### Решение 1: Переход на Hermes Agent
**Обоснование (факты, не хайп):**
- 116K ⭐ GitHub vs 35K у OpenClaw
- SQLite + FTS5 полнотекстовый поиск по памяти (vs текстовые файлы 2200 символов у OpenClaw)
- 8 memory-плагинов из коробки (mem0, honcho, holographic, openviking, retaindb, byterover, hindsight, supermemory)
- Автосоздание скиллов из опыта (self-improving learning loop)
- 15+ мессенджеров (vs 2 у OpenClaw)
- `delegate_task` — встроенные субагенты с разными моделями
- Встроенная миграция: `hermes claw migrate`
- Nous Research — серьёзная AI-лаборатория (авторы Hermes 3 модели)

**Минусы (объективные):**
- Нет нативного Windows (только WSL2)
- Только 1 fallback (нет цепочки primary → N fallbacks как у OpenClaw)
- Версия 0.11 — ещё MVP, баги возможны
- Сыроватость скиллов (дубликаты, странные имена)

### Решение 2: Вариант B — Hermes на VPS (always-on)
Бюджет: ~$14-20/мес

| Компонент | Решение | Стоимость |
|---|---|---|
| Агент | Hermes Agent | $0 |
| VPS | 4vps.su, 2 CPU / 2 GB RAM / Ubuntu 22.04 | ~$6-8/мес |
| Основная модель (оркестратор) | GPT Plus (GPT 5.5) | ~$4/мес |
| Субагенты | MiniMax Starter (M2.7) | ~$10/мес |
| Бэкап субагентов | Nemotron 3 Free (OpenRouter) | $0 |
| Telegram | Hermes gateway встроенный | $0 |
| Память | honcho (бесплатный, локальный) | $0 |

### Решение 3: Спасение данных с VPS (срочно!)
Оплата на 4vps.su истекла. Данные на диске хостер хранит обычно 3-7 дней.

---

## 📁 Что было на VPS (из `openclaw_vps.json`)

```
📁 /root/.openclaw/
├── openclaw.json              ← версия 2026.3.24 (старая!)
├── workspace/
│   ├── skills/
│   │   └── openai-whisper     ← Whisper для русского языка
│   └── ... 
└── agents/
    └── main (Claude Haiku 4.5 → Sonnet 4.6 fallback)
```

**Важные детали:**
- Primary модель: `anthropic/claude-haiku-4-5` (дорого, неэффективно)
- Telegram бот: `TELEGRAM_BOT_TOKEN_VYNESEN_SM_LOCAL_SECRETS`
- `memorySearch: false` ← память была ВЫКЛЮЧЕНА
- Субагенты (code, content, data) НЕ были созданы
- Инструкция `codex_instructions_2026-04-24.md` НЕ была выполнена

---

## ✅ Что сделано в этом чате

| # | Действие | Результат |
|---|----------|----------|
| 1 | Анализ 17000+ сообщений Telegram | Выявлен тренд OpenClaw → Hermes |
| 2 | 4 бага исправлены в sync_workspace_data.py | BUG-1..4 закрыты |
| 3 | Создана инструкция для Codex | `openclaw/codex_instructions_2026-04-24.md` |
| 4 | Диагностика VPS | Сервер мёртв (оплата истекла) |
| 5 | Анализ Habr + GitHub (независимые источники) | Переход на Hermes обоснован |
| 6 | Сравнение моделей (GPT Plus vs MiniMax vs DeepSeek) | Рекомендация: GPT Plus + MiniMax |
| 7 | План миграции VPS → Hermes | Пошаговый, см. ниже |
| 8 | Бэклог обновлён | `workspace/projects/my-backlog.md` |
| 9 | Handover создан | `.agents/handovers/handover_2026-04-25_ai-system-upgrade.md` |

---

## ❌ Что НЕ сделано (TODO для следующего чата)

### Критичное (в порядке приоритета):
1. **Спасти данные с VPS** — зайти на https://4vps.su/dashboard, продлить dk2013 хотя бы на день, скопировать `/root/.openclaw/`
2. **Создать новый VPS** — Ubuntu 22.04, 2 CPU, 2 GB RAM на 4vps.su
3. **Установить Hermes** на новый VPS (`curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash`)
4. **Мигрировать с OpenClaw** (`hermes claw migrate`)
5. **Подключить модели** — GPT Plus (оркестратор) + MiniMax Starter (субагенты)
6. **Настроить Telegram** (`hermes gateway setup`)
7. **Настроить память** (honcho или mem0 плагин)
8. **Тесты** — проверить маршрутизацию, память, субагенты

### Желательное:
- Установить Hermes WebUI (https://github.com/nesquena/hermes-webui, 4K⭐)
- Настроить cron для heartbeat
- Подключить MarkItDown для обработки документов
- Рассмотреть Multica для управления несколькими агентами

---

## 🔗 Ключевые файлы и ссылки

### Локальные файлы:
| Файл | Содержание |
|------|------------|
| `openclaw_vps.json` | Конфиг VPS (IP, пароли, Telegram-бот) |
| `openclaw/codex_instructions_2026-04-24.md` | Инструкция для Codex (устарела — была для OpenClaw) |
| `scripts/dashboard/sync_workspace_data.py` | Исправленный скрипт синхронизации |
| `workspace/projects/my-backlog.md` | Бэклог с задачами |

### Артефакты этого чата:
| Файл | Содержание |
|------|------------|
| `agent_strategy_2026-04-25.md` | План развития AI-агента (3 варианта, рекомендация) |
| `analysis_hermes_vs_openclaw.md` | Детальное сравнение OpenClaw vs Hermes + модели + VPS |

### Внешние ссылки:
- **Hermes Agent:** https://github.com/nousresearch/hermes-agent (116K ⭐)
- **Hermes Docs:** https://hermes-agent.nousresearch.com/docs/
- **Hermes WebUI:** https://github.com/nesquena/hermes-webui (4K ⭐)
- **Habr-обзор:** https://habr.com/ru/articles/1026926/
- **MiniMax:** https://platform.minimax.io
- **VPS:** https://4vps.su/dashboard/myservers

### VPS credentials:
- **IP:** 147.45.67.249 (ВЫКЛЮЧЕН)
- **SSH:** `root` / `ZaC8tUI0fg302`
- **Telegram bot:** `TELEGRAM_BOT_TOKEN_VYNESEN_SM_LOCAL_SECRETS`
- **Gateway token:** `d2a2953d0d726968767abb1610b43136052eeed7c8d39342`

---

## 🧠 Контекст из Telegram-сообщества (ключевые инсайты)

1. **Sergey** — 37 скиллов, Proxmox, OpenViking память, перешёл на Hermes за 2 часа
2. **Dmitry** — Hermes + Qwen3.5, delegate_task, honcho память, «всё сам помнит»
3. **Deniom** — GPT 5.2, «9 дней, ни разу не самоубился»
4. **Pepsykolya** — Hermes не умеет fallback-цепочки (ограничение)
5. **Алексей Корешков** — OpenRouter $10, сидит на free моделях
6. **SUBA** — «Пока только плюсы» после перехода
7. **rtut** — «Клешня ужасно медленная», переехал на Hermes

---

## ⚡ Пошаговый план для следующего чата

```
ЭТАП 1: СПАСЕНИЕ ДАННЫХ (5 минут)
├── Зайти на 4vps.su → проверить dk2013
├── Если жив → продлить → scp данные
└── Если мёртв → данные потеряны (не критично, субагенты не были созданы)

ЭТАП 2: НОВЫЙ VPS (10 минут)
├── Создать на 4vps.su: Ubuntu 22.04, 2 CPU, 2GB
└── Записать IP и пароль

ЭТАП 3: УСТАНОВКА HERMES (15 минут)
├── SSH на новый VPS
├── curl install
├── hermes setup (интерактивный)
├── hermes claw migrate (если данные спасены)
└── hermes model (выбрать MiniMax)

ЭТАП 4: TELEGRAM + ПАМЯТЬ (10 минут)
├── hermes gateway setup (Telegram бот)
├── hermes gateway start
├── hermes memory (настроить honcho)
└── Тест в Telegram

ЭТАП 5: МОДЕЛИ (5 минут)
├── GPT Plus подписка ($4/мес через @gpt_podpiska_bot)
├── MiniMax Starter ($10/мес)
└── Настроить ротацию в Hermes
```

---

*Handover подготовлен: 2026-04-25T16:47 | Автор: Antigravity | Для: следующий чат*
