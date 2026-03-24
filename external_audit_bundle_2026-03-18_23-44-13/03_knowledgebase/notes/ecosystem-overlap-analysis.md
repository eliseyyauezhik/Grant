---
type: analysis
status: active
last_reviewed: 2026-03-18
tags:
  - analysis
  - architecture
  - ecosystem
---
мо
# Ecosystem Overlap Analysis

## Summary

Текущая экосистема уже содержит сильные части будущей системы, но многие из них пересекаются по функции. Главная проблема не в том, что у вас слишком много проектов, а в том, что часть из них пока существует как параллельные интерфейсы к одной и той же задаче: обзор, память, исследование, мониторинг и агентное исполнение.

Ключевой вывод: `My Dashboard`, `Obsidian`, `NotebookLM`, чаты и workflows не нужно развивать как равноправные продукты. Их нужно жестко разнести по слоям одной общей системы.

## Verified Facts

- В `My Dashboard` сейчас отражено `22` проекта, `37` чатов и `21` workflow.
- Из 22 проектов `11` находятся в слое `manual`, то есть значительная часть системы пока живет как ручная или полуинфраструктурная надстройка.
- Все 37 чатов в текущем экспортированном индексе остаются не привязанными к project ID.
- В vault уже зафиксирована целевая схема `My Dashboard -> Agent -> Vault`.
- NotebookLM уже подключен через MCP и работает как внешний knowledge tool, а не как основная база памяти.

## Functional Overlap

### 1. Overview and navigation

Сейчас эту функцию одновременно тянут:

- `Мой Дашборд`
- `workspace/notes/dashboard`
- `Системная карта интересов`
- `Контур мониторинга интересной информации`
- `Карта технологий`

Пересечение реальное, но не все из этого дублирование. Здесь смешаны как минимум три разные задачи:

- пользовательский обзор проектов;
- фильтрация и маршрутизация нового входящего;
- карта знаний и технологических решений.

### 2. Knowledge and memory

Сейчас память распределена между:

- `Obsidian vault`
- `NotebookLM`
- чатами
- заметками и карточками внутри проектов

Здесь как раз есть риск дублирования. Если не закрепить единый центр памяти, одна и та же мысль будет жить в чате, в NotebookLM, в заметке vault и в карточке проекта на dashboard.

### 3. Agent and automation layer

Сейчас сюда относятся:

- `Самосовершенствующиеся агенты`
- `Основное рабочее пространство ИИ-агента`
- `Навыки`
- `Навык Tech Radar`
- workflows из dashboard

Это не разные продукты для пользователя. Это один execution layer, разрезанный по техническим артефактам.

### 4. Monitoring and discovery

Сейчас сюда относятся:

- `Telegram-агрегатор`
- `Контур мониторинга интересной информации`
- `Разведка приложений`
- части `Tech Radar`

Это одна сенсорная подсистема: сбор, triage, enrichment и routing входящей информации.

## Role Distribution

### My Dashboard

Это должен быть главный пользовательский интерфейс.

Он должен владеть:

- списком проектов;
- inbox;
- ежедневным обзором;
- сигналами и alerts;
- запуском агентных сценариев;
- mobile-friendly режимом.

Он не должен становиться главной базой знаний.

### Obsidian Vault

Это должна быть каноническая долговременная память.

Vault должен владеть:

- проектной памятью;
- заметками;
- summaries;
- решениями;
- связями между сущностями;
- архитектурными и операционными знаниями.

Если что-то важно и должно пережить чат, сессию и смену инструмента, это должно оказаться в vault.

### NotebookLM

Это не главный интерфейс и не главный store.

NotebookLM должен использоваться как:

- deep-reading workspace;
- bounded research space по теме или проекту;
- инструмент синтеза по большим корпусам документов, видео, ссылок и файлов;
- внешний аналитический co-processor для агента.

Ключевая роль NotebookLM: быстро понимать сложный корпус. Ключевая ошибка была бы сделать его главным местом хранения истины.

### Chats

Чаты не должны быть системой знания.

Их роль:

- временная рабочая память;
- журнал размышлений;
- промежуточные task traces;
- сырой материал для последующей выжимки.

То, что важно, должно извлекаться из чатов в vault.

### Workflows and subagents

Это operational layer.

Они должны:

- забирать входящее;
- обогащать данные;
- обновлять статусы проектов;
- запускать мониторинги;
- создавать summaries и draft-notes;
- готовить материал для review человеком.

## Recommended Architecture

### Human-facing stack

`My Dashboard -> Project Mode -> Agent Actions -> Vault-backed outputs`

Пользователь живет в dashboard. При выборе проекта он не прыгает по хаосу инструментов, а входит в конкретный `project mode`.

### Knowledge stack

`Inbox -> Agent processing -> Vault note/artifact/project update -> Dashboard summary`

Сначала входящее. Потом обработка агентом. Потом запись в память. Потом показ пользователю.

### External tools

`NotebookLM`, Telegram, YouTube, web sources, n8n, Supabase и другие сервисы должны быть подключены как adapters, а не как параллельные центры управления.

## Computer In Computer Model

Практически это означает такую систему:

1. Один верхний интерфейс: `My Dashboard`
2. Один слой долговременной памяти: `Obsidian vault`
3. Один агентный слой: orchestration + subagents + skills + workflows
4. Один слой внешних инструментов: `NotebookLM`, Telegram, YouTube, web, databases
5. Один общий project registry, по которому все это связывается

## What Is Missing

### 1. Canonical project registry

Нужен единый stable `project_id`, который используется:

- в dashboard;
- в vault;
- в workflows;
- в chat routing;
- в NotebookLM mappings.

Сейчас проекты видны, но чаты уже не связаны с project IDs. Это признак отсутствия общей канонической модели.

### 2. Inbox contract

Нужен единый контракт входящего:

- откуда пришло;
- к какому проекту относится;
- требует ли ручного review;
- нужно ли создать notebook summary;
- нужно ли обновить vault;
- нужно ли показать alert на dashboard.

### 3. Launch contract for agents

Кнопка `Запустить агента` на dashboard должна запускать не абстрактного бота, а проектный режим с:

- project ID;
- linked notes;
- linked notebooks;
- linked workflows;
- текущим next step;
- разрешенными tool scopes.

### 4. Export contract from vault to dashboard

Нужен явный принцип публикации:

- `vault` хранит каноническое состояние проекта;
- `My Dashboard` читает не ручной JSON, а сгенерированный export;
- `projects.json` и сводные dashboard JSON должны формироваться скриптом из vault-entity notes;
- ручное редактирование dashboard JSON должно быть исключением, а не нормой.

### 5. Canonical entity schema

Нужна единая минимальная схема сущностей в frontmatter:

- `project`
- `agent`
- `idea`
- `artifact`
- `task`
- `report`

Без этого агентный слой будет постоянно тратить усилие на реконструкцию структуры из разрозненных полей.

## Recommendations

### Immediate

- Зафиксировать `My Dashboard` как единственный front door.
- Зафиксировать `Obsidian vault` как system of record для знания.
- Зафиксировать `NotebookLM` как исследовательский инструмент, а не хранилище истины.
- Зафиксировать чаты как временный слой, подлежащий выжимке.

### Next

- Ввести единый `project registry`.
- Ввести единый `inbox pipeline`.
- Сделать `project mode` на dashboard.
- Добавить write-back path: agent и NotebookLM создают summaries, которые ложатся в vault и отражаются на dashboard.
- Перевести `dashboard` на модель generated views from vault, а не parallel manual state.
- Ввести базовую YAML/frontmatter schema для project-like сущностей.

### Later

- Подключать полуавтономных агентов только после стабилизации registry и inbox.
- Вводить систему субагентов по ролям: monitor, researcher, synthesizer, planner, operator.
- Автоматизировать weekly review и обновление project status.
- Добавить weekly synthesis loop: агент делает сводку по обновившимся проектам и складывает ее в report layer vault.

## Links

- Related: [[notes/dashboard]]
- Related: [[notes/target-system-architecture]]
- Related: [[notes/project-status-summary]]
- Related: [[projects/ops-board]]

## Next Actions

- [x] Определить canonical project registry и обязательные поля `project_id`.
- [x] Спроектировать `project mode` для `My Dashboard`.
- [ ] Привязать чаты и workflows к project IDs.
- [x] Определить policy: какие summaries идут в NotebookLM, а какие сразу в vault.
- [x] Определить export contract: как `vault` генерирует `projects.json` и dashboard summaries.
- [x] Зафиксировать минимальную YAML/frontmatter schema для project, agent, idea, artifact, task и report.
- [x] Спроектировать weekly synthesis loop для project updates и reports.

## Implemented MVP (2026-03-18)

### Working runtime

- `sync_workspace_data.py` теперь читает канонические project/chat/workflow notes из `KnowledgeBase` как overlay, а не только экспортирует их вслепую.
- Сгенерирован отдельный `project_registry.json`, в котором на каждый проект есть `kbNote`, связанные чаты/workflows, `projectMode` и `launchContract`.
- `My Dashboard` загружает этот registry, подмешивает его в `projectsData` и показывает явный `Project mode` в карточке проекта и в модальном окне.
- Weekly synthesis теперь публикуется и в `docs/weekly_project_brief.md`, и в `KnowledgeBase/Dashboards/Weekly Project Brief.md`.

### Canonical registry fields

Минимальный рабочий контракт `project_registry.json`:

- `id`
- `title`
- `status`
- `topic`
- `kbNote`
- `relatedChats[]`
- `relatedWorkflows[]`
- `projectMode.nextStep`
- `projectMode.allowedTools[]`
- `projectMode.entryPoints.kb`
- `projectMode.entryPoints.dashboard`
- `launchContract.prompt`

### Write-back policy

- `vault` остаётся system of record.
- `Dashboard` читает generated views (`projects.json`, `project_registry.json`, weekly brief), а не хранит первичную истину.
- `NotebookLM` используется как внешний deep-reading/synthesis tool для объёмных корпусов документов.
- Любой агентный результат сначала должен лечь в Markdown/vault, и только потом попадать в дашборд через sync.

### Minimal frontmatter schema

Базовые обязательные поля для entity-notes:

- `project`: `type`, `id`, `title`, `status`, `topic`
- `agent`: `type`, `id`, `title`, `scope`
- `idea`: `type`, `id`, `title`, `status`
- `artifact`: `type`, `id`, `title`, `project`
- `task`: `type`, `id`, `title`, `status`, `project`
- `report`: `type`, `id`, `title`, `period`, `project`

### Remaining gap

- Полная и автоматическая привязка всех legacy-чатов к `project_id` ещё не завершена; это следующий слой нормализации данных, а не блокер для текущего MVP.
- После дополнительной нормализации 2026-03-18 остаточный хвост сократился до 4 неоднозначных legacy-chat sessions; их лучше добивать уже ручной или полу-ручной курацией, а не агрессивной автоэвристикой.

## Tags

#analysis #architecture #ecosystem
