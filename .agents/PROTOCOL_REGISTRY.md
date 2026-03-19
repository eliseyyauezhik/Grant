# PROTOCOL REGISTRY

last_review: 2026-03-19
next_review: 2026-06-19

## Antigravity AI System

### ТЕКУЩИЕ ВЕРСИИ (активные)

| Файл | Версия | Дата | Что изменилось | Статус |
|---|---|---|---|---|
| AGENTS.md | v2.1.0 | 2026-03-19 | Объединен основной протокол, добавлены GUIDED/AUTONOMOUS mode и section 11 | ACTIVE |
| .agents/protocols/session-protocol.md | v1.0.0 | 2026-03-19 | Новый файл с правилами context compaction и handover | ACTIVE |
| .agents/templates/context-handover-template.md | v1.0.0 | 2026-03-19 | Новый шаблон handover документа | ACTIVE |
| .agents/templates/adr-template.md | v1.0.0 | 2026-03-19 | Новый шаблон Architecture Decision Record | ACTIVE |

### ЗАФИКСИРОВАННЫЕ МОДЕЛИ

| Роль | Модель | Версия модели | Дата фиксации |
|---|---|---|---|
| Orchestrator | claude-opus-4-5 | latest | 2026-03-19 |
| Coder | gpt-5.4 | latest | 2026-03-19 |
| Interpreter | gpt-5.4-mini | latest | 2026-03-19 |

### ИСТОРИЯ ВЕРСИЙ

#### v2.1.0 (2026-03-19)

Причина изменения: объединение протоколов и запуск реестра протоколов
Что добавлено: GUIDED/AUTONOMOUS mode, session-protocol.md, context-handover-template.md, adr-template.md, section 11 review triggers
Что убрано: часть дублирования policy между AGENTS.md и procedural файлами
Тест перед применением: локальная проверка структуры AGENTS.md, наличия supporting files и корректности ссылок на шаблоны
Результат теста: AGENTS.md активен, supporting files существуют
Откат: использовать checkpoint `checkpoint_20260319_105850` для AGENTS.md и backup `AGENTS.md.backup_2026-03-20`

#### pre-registry baseline (2026-03-19)

Дорефакторинговая версия AGENTS.md сохранена отдельно в `AGENTS.md.backup_2026-03-20`
