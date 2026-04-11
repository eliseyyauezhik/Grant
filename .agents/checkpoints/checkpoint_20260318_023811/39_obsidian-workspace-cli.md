---
type: service
service_id: obsidian-workspace-cli
status: active
owner: Admin
team: knowledge-base
category: vault-infrastructure
criticality: high
environment:
  - local
repository: "D:/ЯндексДиск/Yandex.Disk/ПРОЕКТЫ/Грант для гимназии Давыдова/Инженерный грант"
entrypoint: obsidian
interfaces:
  - "Obsidian CLI"
  - "Obsidian Desktop 1.12.4"
inputs:
  - Markdown notes
  - .base views
  - Obsidian commands
outputs:
  - Updated vault data
  - CLI-driven automation
storage:
  - workspace/
sources:
  - "[[notes/sources/obsidian-cli-help]]"
  - "[[notes/sources/obsidian-bases-help]]"
runbook: "[[notes/runbooks/obsidian-workspace-cli-runbook]]"
last_reviewed: 2026-03-18
tags:
  - service
---

# Obsidian Workspace CLI

## Purpose

Локальный сервисный слой вокруг Obsidian Desktop + CLI для работы агентного харнеса с vault `workspace/`.

## Current State

- Status: CLI установлен и включен.
- Main user: локальный агентный workflow и ручная работа в Obsidian.
- Main workflow: создавать, читать, обновлять и индексировать знания и `.base` views через CLI и Markdown.

## Interfaces

- Inbound: `obsidian` CLI команды, ручная работа в Obsidian UI, файловые изменения в `workspace/`.
- Outbound: обновление заметок, шаблонов, daily notes и базовых представлений.

## Operational Notes

- Deployment: локальная Windows-установка `Obsidian 1.12.4`.
- Monitoring: проверка `obsidian version`, `obsidian vault`, `obsidian bases`, `obsidian plugins:enabled`.
- Failure modes: сломанный `PATH`, выключенный CLI, поврежденный `.obsidian/obsidian.json`, несогласованные `.base` файлы.

## Related

- Sources: [[notes/sources/obsidian-cli-help]], [[notes/sources/obsidian-bases-help]]
- Runbook: [[notes/runbooks/obsidian-workspace-cli-runbook]]
- Decisions:
