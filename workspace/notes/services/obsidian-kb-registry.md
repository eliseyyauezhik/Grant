---
type: service
service_id: obsidian-kb-registry
status: active
owner: Admin
team: knowledge-base
category: data-catalog
criticality: high
environment:
  - local
repository: "D:/ЯндексДиск/Yandex.Disk/ПРОЕКТЫ/Грант для гимназии Давыдова/Инженерный грант"
entrypoint: projects/services.base
interfaces:
  - Obsidian Bases
  - Markdown properties
inputs:
  - Service notes
  - Source notes
  - Runbook notes
outputs:
  - Service catalog views
  - Source registry views
  - Runbook views
storage:
  - workspace/notes/services/
  - workspace/notes/sources/
  - workspace/notes/runbooks/
  - workspace/projects/
sources:
  - "[[notes/sources/obsidian-bases-help]]"
runbook: "[[notes/runbooks/obsidian-kb-registry-runbook]]"
last_reviewed: 2026-03-18
tags:
  - service
---

# Obsidian KB Registry

## Purpose

Структурирует базу знаний как набор связанных Markdown-заметок с `.base`-представлениями поверх properties.

## Current State

- Status: active
- Main user: владелец knowledge base и локальные AI-агенты
- Main workflow: поддержка карточек сервисов, источников и runbooks с обзором через Bases

## Interfaces

- Inbound: заметки из `notes/services/`, `notes/sources/`, `notes/runbooks/`
- Outbound: таблицы и представления в `projects/services.base`, `projects/sources.base`, `projects/runbooks.base`

## Operational Notes

- Deployment: локальный vault `workspace/`
- Monitoring: проверка `obsidian bases`, `obsidian open path=projects/services.base`, `obsidian base:views`
- Failure modes: пропущенные properties, неверные wikilinks, дрейф схемы между notes и `.base`

## Related

- Sources: [[notes/sources/obsidian-bases-help]]
- Runbook: [[notes/runbooks/obsidian-kb-registry-runbook]]
- Decisions:

