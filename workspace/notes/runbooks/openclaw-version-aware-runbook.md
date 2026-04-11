---
type: runbook
status: active
service: OpenClaw
owner: owner
last_reviewed: "2026-04-03"
tags:
  - runbook
  - openclaw
  - operations
  - versioning
---

# OpenClaw Version-Aware Runbook

## Purpose

Этот runbook фиксирует базовое правило: любые изменения `OpenClaw` сначала проверяются по текущей версии и состоянию runtime, и только потом применяются.

## Preconditions

- Известна текущая версия `OpenClaw`.
- Понятно, где именно работает система:
  - VPS `4vps`
  - gateway на `127.0.0.1:18789`
  - основной канал: Telegram
- Изменение не начинается с советов из старых чатов без сверки с docs и локальным состоянием.

## Standard Procedure

1. Сначала зафиксировать текущую версию и текущий live-state.
   - Проверить `openclaw status`
   - Проверить `openclaw doctor`
   - Проверить `openclaw security audit --json`

2. Перед любой правкой определить тип изменения:
   - операционная правка
   - Telegram / channel правка
   - memory / knowledge правка
   - эксперимент

3. Сверить изменение с текущей версией `OpenClaw`.
   - Не переносить команды и советы из старых гайдов без проверки
   - Особо осторожно относиться к release-sensitive зонам:
     - channels
     - auth
     - sandbox
     - memory

4. Сначала лечить runtime, потом поведение.
   - Если есть ошибка, сначала разбирать:
     - runtime
     - ports
     - env
     - channel prerequisites
   - Не начинать с правки prompt/config-поведения, пока не подтверждено, что runtime здоров

5. Разделять baseline и experiments.
   - Baseline:
     - version discipline
     - Telegram ACL/topic surface
     - runtime-first diagnostics
     - file-memory baseline
   - Experiments:
     - Telegram Business
     - long-history ingest
     - embeddings / semantic memory
     - local-model fallback

6. После правки снова проверить live-state.
   - `openclaw config validate`
   - `openclaw status`
   - `openclaw security audit --json`

7. После успешной проверки сделать короткий write-back.
   - Что изменили
   - Что подтвердили
   - Что осталось риском

## Verification

Считать результат успешным, если:

- правка читается через текущую версию, а не через старые советы;
- `status`, `doctor` и `security audit` не ухудшились без осознанной причины;
- Telegram-канал остался рабочим;
- новое изменение записано в проектный контекст.

## Recovery

- Если после правки поведение стало хуже, откат делать к последнему известному рабочему config backup.
- Если проблема непонятна, возвращаться не к prompt-тюнингу, а к:
  - runtime
  - channel config
  - port/state checks
- Если шаг относится к experimental зоне, не продвигать его в baseline без отдельной повторной проверки.

## Related

- Service: `OpenClaw` on `4vps`
- Sources:
  - `openclaw_project_dossier_2026-03-28.md`
  - `workspace/projects/telegram-chat-analysis-prompt-pack/runs/2026-03-29_openclaw-lab-community/openclaw-development-map.md`
  - `workspace/projects/telegram-chat-analysis-prompt-pack/runs/2026-03-29_openclaw-lab-community/verified_knowledge_roadmap.md`
