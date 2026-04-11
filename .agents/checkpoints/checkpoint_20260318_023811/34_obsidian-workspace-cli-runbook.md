---
type: runbook
status: ready
service: "[[notes/services/obsidian-workspace-cli]]"
owner: Admin
last_reviewed: 2026-03-18
tags:
  - runbook
---

# Obsidian Workspace CLI Runbook

## Purpose

Поддержка локальной связки Obsidian Desktop + CLI для vault `workspace/`.

## Preconditions

- Установлен Obsidian Desktop `1.12.4+`.
- CLI включен.
- Obsidian запущен и открыл vault `workspace/`.

## Standard Procedure

1. Проверить `obsidian version`.
2. Проверить `obsidian vault`.
3. Проверить `obsidian bases`.
4. Открыть `projects/services.base`, затем проверить `obsidian base:views`.
5. Проверить `obsidian plugins:enabled filter=community versions`.
6. Проверить `obsidian daily:path`.
7. Для граф-навигации использовать `obsidian links <note>` и `obsidian backlinks <note>`.
8. Для работы вне папки vault использовать `vault=workspace`.

## Verification

- `obsidian version` возвращает текущую версию приложения.
- `obsidian vault` показывает `workspace`.
- `obsidian files total` и `obsidian bases` завершаются без ошибок.
- После `obsidian open path=projects/services.base` команда `obsidian base:views` показывает ожидаемые представления.
- `obsidian plugins:enabled filter=community versions` показывает `terminal` и `obsidian-kanban`.
- `obsidian daily:path` возвращает путь в `projects/daily/YYYY/MM/YYYY-MM-DD.md`.

## Recovery

- Если `obsidian` не найден, открыть новый терминал или проверить `PATH`.
- Если текущая сессия PowerShell не видит `obsidian`, использовать прямой путь `C:\Users\Admin\AppData\Local\Programs\Obsidian\Obsidian.com` или открыть новый терминал.
- Если CLI выключен, проверить `%APPDATA%\\Obsidian\\obsidian.json`.
- Если vault не найден, проверить запись в `%APPDATA%\\Obsidian\\obsidian.json` и открыть `workspace/` в приложении.

## Related

- Service: [[notes/services/obsidian-workspace-cli]]
- Sources: [[notes/sources/obsidian-cli-help]], [[notes/sources/obsidian-bases-help]]
