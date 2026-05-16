# Hermes Improvement Plan — May 2026

## Контекст
Hermes v0.12.0 на VPS 85.234.100.31 (2GB RAM, Debian). Основной LLM: gpt-5.4-mini через CloseRouter.
Баланс CloseRouter: $2.58. 71 сессия за 30 дней, ~58.8M токенов.

---

## 🔴 ПРИОРИТЕТ 1: Качество ответов (решено сегодня)

### Проблема: потеря контекста проекта
- ✅ **SOUL.md переписан** → Context Anchoring Protocol, анти-дрифт
- ✅ **LIFE_MAP обновлён** → проекты с приоритетами
- ✅ **КОРА skill** создан → Hermes знает как работать с проектом
- ⏳ **Проверить в бою** → Дмитрий тестирует через Telegram

### Что ещё нужно для качества
- [ ] Настроить fallback_providers для auxiliary tasks (compression, session_search)
- [ ] Проверить reasoning_effort=medium — может нужно high для проектных задач
- [ ] Добавить explicit project-context injection в gateway hooks (если поддерживается)

---

## 🟡 ПРИОРИТЕТ 2: Бюджетная эффективность

### Текущие расходы (оценка за 30 дней)
```
gpt-5.4-mini:     18.7M tokens → ~$1.87 (основная модель)
nemotron-3-super: 27.4M tokens → ~$2.74 (субагенты? или auxiliary?)
gpt-5.5:           2.2M tokens → ~$0.44
claude-opus-4.7:   2.7M tokens → ~$0.54 (specialist)
deepseek-v4-flash: 4.1M tokens → ~$0.41
kimi-k2.6:         2.6M tokens → ~$0.26
```
**Итого: ~$6.26 за 30 дней** (грубо)

### Рекомендации
- [ ] nemotron-3-super потребляет 47% всех токенов — проверить зачем, может заменить на mimo-v2-pro или glm-5.1
- [ ] Установить бюджетные лимиты на cron-задачи (max_tokens)
- [ ] Для классификатора: использовать gemini-3.1-flash-lite-preview (самая дешёвая мультимодальная)
- [ ] Для субагентов: попробовать minimax-m2.7 вместо gpt-5.4-mini

---

## 🟢 ПРИОРИТЕТ 3: Инфраструктурные улучшения

### Upgrade до v0.13.0
По данным upgrade-reports, v0.13.0 включает:
- Durable Multi-Agent Kanban
- `/goal` command
- MCP SSE/OAuth forwarding
- Session persistence
- Redaction-by-default
- Pluggable providers
- `X-Hermes-Session-Key`

**Рекомендация:** upgrade после проверки SOUL.md в бою (через 2-3 дня).

### Безопасность
- [ ] CVE-2026-7397: symlink-following — проверить, закрыто ли в v0.13.0
- [ ] CVE-2026-7112: improper auth — то же
- [ ] Включить redaction-by-default

### mem0
- Текущая проблема: 500 errors на sync (read-only transaction)
- Это на стороне mem0.ai — мониторить, не чинить
- Альтернатива: усилить built-in SQLite память

---

## 📊 Метрики для отслеживания

| Метрика | Текущее | Цель |
|---------|---------|------|
| Баланс CloseRouter | $2.58 | > $1.00 (пополнять при < $1) |
| Средняя стоимость сессии | ~$0.09 | < $0.10 |
| Удержание контекста проекта | низкое | высокое (проверить R-5 delivery) |
| Cron jobs с ошибками | 1 (HTTP 402) | 0 |
| RAM usage | 693MB / 1963MB | < 1000MB |
| Disk | 20GB / 50GB (43%) | < 60% |

---

## Расписание ревью
- **Через 2-3 дня:** проверить SOUL.md в бою, получить обратную связь
- **Через неделю:** решение по upgrade v0.13.0
- **Через 2 недели:** оптимизация бюджета на основе реальных данных
