# Hermes VPS — Конфигурация (май 2026)

## Инфраструктура
- VPS: 85.234.100.31 (Debian, 2GB RAM, 50GB disk)
- Hermes v0.12.0 (рекомендован upgrade до v0.13.0)
- Gateway: systemd user service, Telegram bot
- Memory: mem0 cloud + built-in SQLite (mem0 имеет 500 ошибки)

## Модели на CloseRouter (23 доступны)
### Основные
- gpt-5.4-mini ($0.10/M) — default
- gpt-5.4 ($0.15/M)
- gpt-5.5 ($0.20/M)
- claude-sonnet-4.6 ($0.17/M)
- claude-opus-4.6/4.7 ($0.20/M)
- deepseek-v4-pro ($0.10/M)
- gemini-3.1-pro-preview ($0.13/M)

### Дешёвые (для субагентов)
- mimo-v2-pro ($0.10/M)
- minimax-m2.7 ($0.10/M)
- z-ai/glm-5.1 ($0.10/M)
- gemini-3.1-flash-lite ($0.10/M)
- google/nano-banana-2 ($0.10/M)

## SOUL.md — ключевые паттерны
1. Context Anchoring Protocol — каждую сессию читает LIFE_MAP + /root/projects/
2. Правило 15 строк — если подзадача > 15 строк → СТОП → возврат к проекту
3. Mandatory delegation — простое → дешёвые модели
4. Proactive behavior — напоминания, предложения
5. Anti-patterns: не теряй контекст, не задавай > 1 вопрос, не повторяй пользователя

## Cron-задачи (постоянные)
- 08:00 — КОРА утренний пульс
- 09:00/21:00 — Hermes поиск улучшений
- Пт 18:00 — Weekly Synthesis
- Вс 10:00 — Еженедельный запрос на улучшение
- Каждые 2 дня 09:00 — AI Monitor
- Пн 19:30 — Neural net learning (HTTP 402 на OpenRouter — нужно исправить)
- Сб 10:00 — Study plan review

## Известные проблемы
- mem0 sync: 500 errors (сторонняя проблема)
- OpenRouter кредиты закончились (HTTP 402)
- CVE-2026-7397 (symlink), CVE-2026-7112 (auth) — не новые, мониторить
