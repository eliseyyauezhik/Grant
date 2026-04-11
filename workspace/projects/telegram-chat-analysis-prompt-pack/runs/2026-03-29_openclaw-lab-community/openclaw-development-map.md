# OpenClaw: карта развития, траектория и библиотека

Компактная витрина для быстрого чтения. Детали и доказательная база лежат в:

- [[projects/telegram-chat-analysis-prompt-pack/runs/2026-03-29_openclaw-lab-community/verified_knowledge_roadmap]]
- [[notes/analytical-node-architecture]]

## Коротко

- `OpenClaw` в этом корпусе нужен как security-first, file-driven, version-sensitive исполнительный node.
- Его не стоит читать как plug-and-play chatbot.
- Базовая траектория развития идет от `operational correctness` к `managed surface`, затем к `file-memory`, потом к `corpus intelligence`.

## Карта развития

| Этап | Фокус | Что должно быть true | Итоговый артефакт |
|---|---|---|---|
| 0 | Версионная дисциплина | Любой совет читается через конкретную release policy и версию | `version-aware runbook` |
| 1 | Операционная корректность | Сначала `doctor`, runtime, ports и env, потом prompt-tuning | troubleshooting baseline |
| 2 | Управляемый Telegram | Явный `botToken`, ACL/topics, Business только как ограниченная поверхность | Telegram surface spec |
| 3 | File-memory baseline | `daily notes` + `MEMORY.md` + retrieval over curated files | memory baseline |
| 4 | Corpus intelligence | `corpus -> verification -> triage -> ranking -> roadmap` | verified knowledge library |
| 5 | Контролируемые эксперименты | Provider diversification и ingest-эксперименты только после стабилизации | experiment backlog |

## Траектория

### Сейчас

- Не доверять старым setup recipes без проверки версии.
- Проверять runtime и каналы до любых правок prompt layer.
- Держать Telegram как ACL/topic surface, а не как свободный чат без границ.

### Следующий шаг

- Зафиксировать file-memory baseline как минимальный стандарт.
- Делать write-back из corpus runs в vault.
- Вести проектный реестр проверенных знаний.
- Держать Business-bot, long-history ingest и semantic memory как controlled experiments.

### После стабилизации

- Расширять provider set только если economics это оправдывают.
- Подключать local-model fallback только после локальной проверки.
- Связывать signals с личным ИИ-оркестратором, а не оставлять их внутри одного чата.

## Библиотека проверенных знаний

### Проверено

| Знание | Почему это важно | Практический вывод |
|---|---|---|
| Версионная дисциплина обязательна | Старые советы быстро ломаются на другой версии | Всегда сверять release policy и tag |
| Telegram в `OpenClaw` устроен явно | Канал, pairing и topics не должны быть магией | Проектировать Telegram как ACL-layer |
| Runtime-first diagnostics важнее prompt tweaking | Ложные проблемы часто сидят в runtime/config | Сначала `doctor`, потом промпты |
| File-memory baseline — практический default | Файловая память устойчивее, чем надежда на контекст | Держать `daily notes` и `MEMORY.md` |
| Subscription auth policy-sensitive | Техническая поддержка не равна стабильному baseline | Регулярно перепроверять условия |
| Telegram Business — ограниченная поверхность | Это управляемый доступ, а не полный mirror личных чатов | Использовать только с явным scope |

### Вероятно, но не проверено

| Знание | Почему еще не считается опорным | Что делать дальше |
|---|---|---|
| Отдельный long-horizon ingest для Telegram history | Сильный сигнал из корпуса, но не норма из primary sources | Держать как backlog experiment |
| Явные финальные отчеты и pruning как hygiene-layer | Хорошая operational heuristic, но не подтвержденная норма | Проверить на локальном прогоне |

### Эксперименты

| Идея | Почему пока только эксперимент | Когда возвращаться |
|---|---|---|
| Small local models as default fallback | Слабый и неповторенный сигнал | После стабилизации базовой архитектуры |
| `memU + pgvector + Telegram Business` bundle | Перспективно, но недостаточно подтверждено | После базового memory-layer |

## Как пользоваться библиотекой

- `Проверено` можно брать в operating rule.
- `Вероятно, но не проверено` можно держать только в backlog экспериментов.
- `Эксперименты` не стоит поднимать до стандартов без новой проверки.

## Где читать дальше

- Подробная библиотека и roadmap: [[projects/telegram-chat-analysis-prompt-pack/runs/2026-03-29_openclaw-lab-community/verified_knowledge_roadmap]]
- Архитектура Аналитического Узла: [[notes/analytical-node-architecture]]
- Framework для будущих corpus runs: [[projects/telegram-chat-analysis-prompt-pack/verified_corpus_to_roadmap_framework]]

## Следующая полезная форма

- Этот файл можно держать как front page.
- [[projects/telegram-chat-analysis-prompt-pack/runs/2026-03-29_openclaw-lab-community/verified_knowledge_roadmap]] остается подробной библиотекой.
- [[notes/analytical-node-architecture]] остается системной рамкой для write-back и proactive signals.
