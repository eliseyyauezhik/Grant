---
type: runbook
status: ready
service: "[[notes/services/obsidian-kanban-ops-board]]"
owner: Admin
last_reviewed: 2026-03-18
tags:
  - runbook
---

# Obsidian Kanban Ops Board Runbook

## Purpose

Поддержка weekly operations board в `projects/ops-board.md`.

## Preconditions

- Plugin `obsidian-kanban` включен.
- Файл `projects/ops-board.md` существует в vault.
- Новые задачи при необходимости оформляются через `[[assets/task-template]]`.

## Standard Procedure

1. Открыть `projects/ops-board.md`.
2. Просмотреть `Backlog` и перенести актуальные задачи в `This Week`.
3. Для заблокированных карточек добавить явную причину и wikilink на зависимость.
4. Для завершенных задач переносить карточки в `Done`.
5. После weekly review архивировать completed cards, если board начал разрастаться.

## Verification

- В `This Week` только ближайшие задачи.
- Карточки ссылаются на relevant notes или service records.
- `Done` содержит только завершенные и проверяемые результаты.

## Recovery

- Если board выглядит как обычный Markdown, открыть его в Obsidian и использовать команду Kanban view.
- Если карточки потеряли структуру, проверить frontmatter `kanban-plugin: board`.

## Related

- Service: [[notes/services/obsidian-kanban-ops-board]]
- Sources: [[notes/sources/obsidian-kanban-plugin]]

