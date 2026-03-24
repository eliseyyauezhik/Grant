---
type: service
service_id: obsidian-kanban-ops-board
status: active
owner: Admin
team: knowledge-base
category: work-management
criticality: high
environment:
  - local
repository: "D:/ЯндексДиск/Yandex.Disk/ПРОЕКТЫ/Грант для гимназии Давыдова/Инженерный грант"
entrypoint: projects/ops-board.md
interfaces:
  - Obsidian Kanban plugin
  - Markdown board file
inputs:
  - Backlog items
  - Weekly priorities
  - Links to service and source notes
outputs:
  - Prioritized board state
  - Weekly execution focus
storage:
  - workspace/projects/ops-board.md
sources:
  - "[[notes/sources/obsidian-kanban-plugin]]"
  - "[[notes/sources/obsidian-cli-help]]"
runbook: "[[notes/runbooks/obsidian-kanban-ops-board-runbook]]"
last_reviewed: 2026-03-18
tags:
  - service
---

# Obsidian Kanban Ops Board

## Purpose

Дает один оперативный board для weekly execution внутри vault, чтобы задачи не расползались по разрозненным заметкам.

## Current State

- Status: active
- Main user: владелец проекта и агент, работающий с KB
- Main workflow: backlog triage -> weekly selection -> blocked tracking -> done archive

## Interfaces

- Inbound: новые задачи, follow-ups из daily notes, ссылки на knowledge notes
- Outbound: видимый weekly plan и markdown-backed история выполнения

## Operational Notes

- Deployment: `projects/ops-board.md` в том же vault
- Monitoring: открытие board файла, review карточек в `This Week`, archive completed cards
- Failure modes: переполненный backlog, несвязанные карточки без wikilinks, устаревшие weekly priorities

## Related

- Sources: [[notes/sources/obsidian-kanban-plugin]], [[notes/sources/obsidian-cli-help]]
- Runbook: [[notes/runbooks/obsidian-kanban-ops-board-runbook]]
- Decisions:

