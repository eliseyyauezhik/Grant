# KB Operating Model

Этот vault настроен как knowledge base и легкая база данных для сервисов, источников и runbooks поверх Markdown + Bases.

## Folder Roles

- `notes/inbox/` для сырого захвата и новых заметок по умолчанию.
- `notes/services/` для карточек сервисов.
- `notes/sources/` для source-of-truth заметок, ссылок на docs, repo и внешние системы.
- `notes/runbooks/` для операционных инструкций.
- `notes/decisions/` для архитектурных решений.
- `projects/` для активной работы, `.base` views и daily logs.

## Property Conventions

### Services

- `type: service`
- `service_id` короткий стабильный идентификатор.
- `status` жизненный цикл сервиса: `planned`, `active`, `paused`, `deprecated`.
- `owner` и `team` для ответственности.
- `category` для домена сервиса.
- `sources` для ссылок на source notes.
- `runbook` для ссылки на операционную инструкцию.

### Sources

- `type: source`
- `kind` например `doc`, `repo`, `api`, `video`, `dataset`.
- `url` или другой первичный locator.
- `last_verified` для контроля устаревания.
- `services` для обратной связи с сервисами.

### Runbooks

- `type: runbook`
- `service` ссылка на сервис.
- `status` как минимум `draft` или `ready`.

## Working Rules

- Новые знания сначала попадают в `notes/inbox/`, потом переводятся в нужный домен.
- Сервисы и источники связываются через wikilinks и properties, а обзор делается через `.base` файлы.
- Внешние документы не считаются частью KB, пока не появился Markdown-конспект в `notes/sources/`.
