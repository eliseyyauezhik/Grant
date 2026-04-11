---
type: service
service_id: obsidian-terminal-shell
status: active
owner: Admin
team: knowledge-base
category: operator-console
criticality: medium
environment:
  - local
repository: "D:/ЯндексДиск/Yandex.Disk/ПРОЕКТЫ/Грант для гимназии Давыдова/Инженерный грант"
entrypoint: terminal
interfaces:
  - Obsidian Terminal plugin
  - PowerShell / cmd
inputs:
  - Vault context
  - Local shell commands
outputs:
  - Terminal sessions from Obsidian
  - Local operational checks
storage:
  - workspace/.obsidian/plugins/terminal/data.json
sources:
  - "[[notes/sources/obsidian-terminal-plugin]]"
runbook: "[[notes/runbooks/obsidian-terminal-shell-runbook]]"
last_reviewed: 2026-03-18
tags:
  - service
---

# Obsidian Terminal Shell

## Purpose

Дает оператору быстрый доступ к shell-командам прямо из Obsidian без выхода из vault workflow.

## Current State

- Status: active
- Main user: оператор knowledge base
- Main workflow: открыть terminal pane, запускать CLI-проверки и локальные команды по vault

## Interfaces

- Inbound: локальные shell-команды и vault context
- Outbound: terminal output, ad hoc verification, быстрые operational checks

## Operational Notes

- Deployment: plugin `terminal` установлен и включен
- Monitoring: наличие plugin в `community-plugins.json`, доступность ribbon/command palette actions
- Failure modes: отсутствующий подходящий terminal profile, конфликты hotkeys, shell session без нужного PATH

## Related

- Sources: [[notes/sources/obsidian-terminal-plugin]]
- Runbook: [[notes/runbooks/obsidian-terminal-shell-runbook]]
- Decisions:

