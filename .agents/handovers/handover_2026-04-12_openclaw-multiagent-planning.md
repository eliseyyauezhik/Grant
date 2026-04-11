# Handover: OpenClaw VPS — Готово к мультиагентной архитектуре
**Дата:** 2026-04-12 ~02:45 MSK  
**Для:** мощной coding/planning нейросети (следующая сессия)  
**Статус:** VPS работает, конфиг проверен, следующий этап — мультиагентность

---

## ✅ Что сделано (текущая сессия)

### Инфраструктура VPS — VERIFIED
- **VPS:** 147.45.67.249 (4vps.su, Ubuntu 22.04, root)
- **Сервис:** `openclaw-gateway.service` — systemd, `active (running)`
- **PID:** 1110525 / 1110538, порт `127.0.0.1:18789`
- **OpenClaw:** версия `2026.4.10 (44e5b62)`

### LLM-конфигурация — VERIFIED ✅
Путь к конфигу: `/root/.openclaw/openclaw.json` → `agents.defaults.model`

```json
{
  "primary": "openrouter/z-ai/glm-5.1",
  "fallbacks": [
    "openrouter/google/gemini-2.5-pro-preview",
    "openrouter/qwen/qwen3-coder:free",
    "openrouter/openai/gpt-oss-120b:free",
    "openrouter/nvidia/nemotron-3-super-120b-a12b:free",
    "openrouter/nvidia/nemotron-nano-12b-v2-vl:free"
  ]
}
```

### Telegram — RUNNING ✅
- Mode: `polling`
- Token: `8393655317:AAH1fLa6H8q3gHlNOasYfSsdr_7d9Jcd7C0` (в конфиге VPS)
- dmPolicy: `pairing`
- ⚠️ Финальный тест в Telegram (написать боту вручную) — НЕ выполнен, отложен

### API-ключи
| Провайдер | Статус |
|---|---|
| OpenRouter (`sk-or-v1-...32577c`) | ✅ Active |
| Anthropic (`sk-ant-...ZEOMOQAA`) | ⚠️ `disabled:billing` — не критично |

### Структура конфига (важно для следующей сессии)
```
~/.openclaw/
├── openclaw.json              ← главный конфиг
├── agents/
│   ├── main/agent/
│   │   ├── models.json        ← провайдеры и модели
│   │   ├── auth-profiles.json ← API ключи
│   │   └── auth-state.json
│   └── monitor/agent/         ← агент мониторинга (stepfun/step-3.5-flash)
├── credentials/
│   ├── telegram-default-allowFrom.json
│   └── telegram-pairing.json
└── workspace/
    └── skills/                ← установленные скиллы
        ├── memory/
        ├── web-search/
        ├── cron-scheduling/
        ├── obsidian/
        └── actionbook/
```

### Конфиг `agents.defaults` (ключевые поля)
```json
{
  "model": { "primary": "openrouter/z-ai/glm-5.1", "fallbacks": [...] },
  "workspace": "/root/.openclaw/workspace",
  "memorySearch": { "enabled": true },
  "contextPruning": { "mode": "cache-ttl", "ttl": "1h" },
  "sandbox": { "mode": "all", "workspaceAccess": "rw", "scope": "agent" },
  "heartbeat": { "every": "2h", "lightContext": true },
  "imageModel": { "primary": "openrouter/nvidia/nemotron-nano-12b-v2-vl:free" }
}
```

### Скиллы OpenClaw — ИЗУЧЕНО
- **Итого доступно:** 56 скиллов в каталоге, 13 готовы к использованию
- **Уже установлены в workspace:** memory, web-search, cron-scheduling, obsidian, actionbook
- **Ключевой для мультиагентности:** `coding-agent` (needs setup)
  - Умеет делегировать задачи: Codex, Claude Code, Pi-агентам
  - Запускает через background process
  - НЕ для: простых фиксов, read-only задач

---

## 🎯 Следующий этап: Мультиагентная архитектура

### Видение (от пользователя)
```
Оркестратор (GLM 5.1 / main agent)
├── Агент "Документы" — OCR/PDF обработка
├── Агент "Медиа" — vision, изображения
├── Агент "Контент" — тексты, копирайтинг
├── Агент "Код" — Qwen3-Coder для разработки
└── Агент "Данные" — аналитика, структурированные данные
```

### Что нужно выяснить и спланировать
1. **`openclaw skills setup coding-agent`** — первый шаг, установить скилл-оркестратор
2. Изучить `openclaw agents --help` — нативная поддержка мультиагентности
3. Изучить `openclaw mcp --help` — MCP-серверы для расширения возможностей
4. Решить: использовать встроенный `coding-agent` скилл ИЛИ добавлять агентов через `agents.list` в конфиге
5. Для агента "Код" — `openrouter/qwen/qwen3-coder:free` уже в fallbacks, вынести как отдельный агент
6. Для агента "Медиа" — `openrouter/nvidia/nemotron-nano-12b-v2-vl:free` уже настроен как imageModel

### Конкретные команды для изучения на VPS
```bash
ssh root@147.45.67.249  # пароль: ZaC8tUI0fg302
openclaw agents --help
openclaw skills setup coding-agent
openclaw mcp --help 2>&1 | head -40
openclaw skills list --ready   # только готовые скиллы
cat ~/.openclaw/workspace/skills/memory/_meta.json  # посмотреть структуру скилла
```

---

## 📁 Локальные файлы проекта (на Windows машине)

| Файл | Содержимое |
|---|---|
| `D:\...\openclaw\4vps.txt` | IP, пароль root VPS |
| `D:\...\openclaw\API OPENCLAW.txt` | API ключи |
| `D:\...\openclaw\telegram bot openclaw.txt` | Токен Telegram бота |
| `D:\...\openclaw\OPENCLAW KNOWLEDGE BASE.md` | Большой KB (39KB) |
| `D:\...\openclaw\Новая папка\skills openclaw.rtf` | Вывод `openclaw skills list` (290KB RTF) |
| `KnowledgeBase/.../openclaw-llm-strategy-2026.md` | Стратегия LLM выбора |
| `KnowledgeBase/.../openclaw-4vps-setup-guide.md` | Гайд установки |

---

## ⚠️ Технические нюансы

1. **SSH через Windows PowerShell**: НЕ принимает пароль через stdin/pipe — только интерактивный ввод. Каждую SSH-команду нужно подтверждать вручную. Решение: настроить SSH-ключи (публичный ключ уже есть в `C:\Users\Admin\.ssh\id_ed25519.pub`)
2. **Конфиг-путь**: `agents.defaults` (с `s`), не `agents.default` — типичная ловушка
3. **Порт gateway**: loopback-only (`127.0.0.1:18789`), не доступен снаружи напрямую
4. **Два агента**: `main` (GLM 5.1) и `monitor` (stepfun/step-3.5-flash) уже настроены

---

## 🟡 Pending tasks (не сделано)

- [ ] Написать боту в Telegram — убедиться что GLM 5.1 отвечает
- [ ] `openclaw skills setup coding-agent` — настроить мультиагентный скилл  
- [ ] Спроектировать и задокументировать мультиагентную архитектуру
- [ ] Настроить SSH-ключи на VPS (избавиться от паролей)
- [ ] Изучить возможности MCP на OpenClaw

---

## 💡 Контекст для планировщика

Пользователь строит персонального AI-ассистента на базе OpenClaw на VPS. Основная идея — **один оркестраторный агент (GLM 5.1)** маршрутизирует задачи специализированным субагентам в зависимости от типа запроса. Telegram — основной интерфейс. VPS дешёвый (4vps.su), поэтому работаем в рамках бесплатных/дешёвых моделей через OpenRouter.

Пользователь технически подкован, работает в связке Windows + VPS Ubuntu, предпочитает конкретные команды и краткие объяснения.
