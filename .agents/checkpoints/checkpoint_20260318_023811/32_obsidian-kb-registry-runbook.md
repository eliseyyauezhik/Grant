---
type: runbook
status: ready
service: "[[notes/services/obsidian-kb-registry]]"
owner: Admin
last_reviewed: 2026-03-18
tags:
  - runbook
---

# Obsidian KB Registry Runbook

## Purpose

Поддержка сервисного каталога, source registry и runbook registry как согласованных `.base`-представлений.

## Preconditions

- Vault `workspace/` открыт в Obsidian.
- Core plugin `bases` включен.
- Сервисные заметки содержат обязательные properties.

## Standard Procedure

1. Проверить `obsidian vault=workspace bases`.
2. Открыть `projects/services.base`.
3. Проверить, что новые service/source/runbook notes видны в соответствующих views.
4. Для измененных карточек обновить `last_reviewed`.
5. Если схема изменилась, проверить соответствующие templates в `assets/`.

## Verification

- `projects/services.base`, `projects/sources.base` и `projects/runbooks.base` открываются без ошибок.
- Новые карточки появляются в таблицах и группировках.

## Recovery

- Если запись не видна, проверить folder, `type` и обязательные properties.
- Если view ломается, сравнить YAML `.base` с текущими property names в notes.

## Related

- Service: [[notes/services/obsidian-kb-registry]]
- Sources: [[notes/sources/obsidian-bases-help]]

