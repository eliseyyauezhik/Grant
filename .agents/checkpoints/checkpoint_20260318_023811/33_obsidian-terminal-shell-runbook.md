---
type: runbook
status: ready
service: "[[notes/services/obsidian-terminal-shell]]"
owner: Admin
last_reviewed: 2026-03-18
tags:
  - runbook
---

# Obsidian Terminal Shell Runbook

## Purpose

Быстрый запуск terminal sessions из Obsidian для operational checks по vault.

## Preconditions

- Plugin `terminal` включен.
- Vault открыт в Obsidian Desktop.
- Нужная shell-среда доступна на машине.

## Standard Procedure

1. Открыть terminal через ribbon или command palette.
2. Запускать проверки из корня `workspace/`, если задача относится к KB.
3. Для CLI-операций по Obsidian использовать `obsidian` или прямой путь к `Obsidian.com`, если PATH в текущей shell-сессии не обновился.
4. Результаты, которые должны сохраниться как знание, переносить в Markdown notes, а не держать только в terminal history.

## Verification

- Terminal pane открывается.
- Shell принимает команды без ошибок запуска.
- Нужные проверки по vault выполняются из Obsidian UI.

## Recovery

- Если `obsidian` не находится, открыть новую shell-сессию или использовать `C:\\Users\\Admin\\AppData\\Local\\Programs\\Obsidian\\Obsidian.com`.
- Если integrated terminal неудобен, использовать external profile или обычный system terminal.

## Related

- Service: [[notes/services/obsidian-terminal-shell]]
- Sources: [[notes/sources/obsidian-terminal-plugin]]

