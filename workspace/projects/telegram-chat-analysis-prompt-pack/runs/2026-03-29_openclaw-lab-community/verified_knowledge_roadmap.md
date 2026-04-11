# OpenClaw Corpus: Библиотека проверенных знаний и roadmap

## Статус

Собрано по состоянию на `2026-03-30` на базе:

- Telegram corpus `OpenClaw Lab Community`
- staged outputs `stage1_claims.json`, `stage2_topics.json`, `final_analysis.json`
- внешнего verification-pass по первичным источникам

## Проверенные первичные источники

- OpenClaw Release Policy  
  `https://docs.openclaw.ai/reference/RELEASING`
- OpenClaw Telegram docs  
  `https://docs.openclaw.ai/channels/telegram`
- OpenClaw Doctor docs  
  `https://docs.openclaw.ai/gateway/doctor`
- OpenClaw FAQ по Anthropic subscription auth  
  `https://docs.openclaw.ai/help/faq`
- Telegram Business docs  
  `https://core.telegram.org/api/business`
- Telegram Connected Business Bots docs  
  `https://core.telegram.org/api/bots/connected-business-bots`
- Telegram Business Bot Recipients schema  
  `https://core.telegram.org/constructor/businessBotRecipients`

## Что подтверждено

### 1. Работа с версиями обязательна

Статус корзины: `проверено`
Отметка по нашей среде: `проверено по первичным источникам`

Почему:
- у OpenClaw есть публичные release lanes `stable`, `beta`, `dev`;
- stable tags именуются по схеме `YYYY.M.D`;
- значит советы из чатов и старых гайдов нельзя переносить без сверки по версии.

Практический вывод:
- любой change-plan по `OpenClaw` надо читать через конкретную версию, а не через "в чате советовали".

### 2. Telegram в OpenClaw устроен явно, а не «сам как-нибудь поймет»

Статус корзины: `проверено`
Отметка по нашей среде: `проверено по первичным источникам`

Почему:
- Telegram в OpenClaw конфигурируется через явный `botToken` и channel config;
- DM pairing и group/topic behavior описаны явно;
- forum topics изолируются через session keys с `:topic:<threadId>`.

Практический вывод:
- Telegram architecture надо проектировать как слой ACL/topics, а не как свободный чат без границ.

### 3. Runtime-диагностика так же важна, как prompt layer

Статус корзины: `проверено`
Отметка по нашей среде: `проверено по первичным источникам`

Почему:
- `doctor` проверяет runtime, портовые конфликты, Node environment и канал-зависимые prerequisites;
- docs отдельно предупреждают, что Telegram требует корректного Node-based gateway runtime.

Практический вывод:
- silent failures сначала диагностируются через runtime/channel checks, а не через переписывание prompt files.

### 4. Workspace memory — это часть операционной архитектуры, а не косметика

Статус корзины: `проверено`
Отметка по нашей среде: `проверено по первичным источникам`

Почему:
- docs `doctor` прямо советуют workspace memory system;
- staged corpus и official docs сходятся в одном: файл-память важнее надежды на бесконечный live context.

Практический вывод:
- базовый roadmap по `OpenClaw` должен включать memory baseline как обязательный слой, а не как optional nice-to-have.

### 5. Anthropic subscription auth технически поддержан, но policy-risk никуда не исчезает

Статус корзины: `проверено`
Отметка по нашей среде: `проверено по первичным источникам`

Почему:
- FAQ OpenClaw подтверждает поддержку `setup-token` и Anthropic API key;
- там же явно сказано: это technical compatibility, not a policy guarantee.

Практический вывод:
- subscription-based auth нельзя считать твердым production-baseline без регулярной проверки текущих условий.

### 6. Telegram Business — это ограниченная и явно настраиваемая поверхность доступа, а не полное зеркало личных чатов

Статус корзины: `проверено`
Отметка по нашей среде: `не проверено в нашей среде`

Почему:
- официальная Telegram Business docs говорит, что business features сейчас доступны Premium-подписчикам;
- official Connected Business Bots docs говорит, что к user account сейчас может быть подключен только один business bot;
- schema `businessBotRecipients` явно задает охват private chats через `existing_chats`, `new_chats`, `contacts`, `non_contacts`, `users`, `exclude_users`.

Практический вывод:
- Telegram Business нужно проектировать как управляемый канал с явным охватом чатов и прав, а не как автоматический доступ ко всей личной переписке.
- Локальный end-to-end smoke test в нашей среде пока не проводился, поэтому operational details для нашего аккаунта ещё не подтверждены на практике.

## Что выглядит полезным, но пока не подтверждено полностью

### 1. Отдельный ingest для длинной истории Telegram

Статус корзины: `вероятно, но не проверено`
Отметка по нашей среде: `не проверено в нашей среде`

Сигнал из корпуса:
- corpus устойчиво толкает в сторону отдельного ingest/retrieval pipeline для длинной истории.

Почему ещё не считается подтвержденным:
- официальный источник подтверждает важность workspace memory, но не дает прямой нормы "Telegram history -> separate vector ingest" как обязательный стандарт.

### 2. Явные финальные отчеты и pruning сессий как защита от silent failure

Статус корзины: `вероятно, но не проверено`
Отметка по нашей среде: `не проверено в нашей среде`

Сигнал из корпуса:
- corpus repeatedly links degraded behavior with session bloat and poor completion signaling.

Почему ещё не считается подтвержденным:
- это сильная operational heuristic, но пока не подтверждена как явное official rule.

## Что пока лучше держать в экспериментальной зоне

### 1. Малые локальные модели как default fallback

Статус корзины: `спорно или быстро устаревает`
Отметка по нашей среде: `не проверено в нашей среде`

Причина:
- corpus дает слабый и неповторенный сигнал;
- официальных подтверждений, что это хороший default именно для нашего `OpenClaw`, нет.

### 2. Production-ready bundle вокруг memU + pgvector + Telegram Business

Статус корзины: `спорно или быстро устаревает`
Отметка по нашей среде: `не проверено в нашей среде`

Причина:
- идея выглядит перспективно, но в текущем verification-pass она не собрана из достаточного числа первичных подтверждений.

## Ранжирование

Формула:

```text
(сила_подтверждения * 0.30 +
 применимость      * 0.25 +
 влияние           * 0.25 +
 (6 - устаревание) * 0.10 +
 (6 - затраты)     * 0.10) * 20
```

| Место | Знание | Корзина | Балл | Почему это важно |
|---|---|---|---:|---|
| 1 | Работа с версиями и release discipline | проверено | 98 | Без этого любой чужой совет может оказаться поломанным по версии. |
| 2 | Явные Telegram channel, pairing, topics и ACL | проверено | 96 | Это базовая граница безопасности и предсказуемости канала. |
| 3 | Runtime-first diagnostics перед prompt tweaking | проверено | 91 | Быстро сокращает ложные гипотезы и экономит время на triage. |
| 4 | File-memory baseline (`daily notes` + `MEMORY.md` + retrieval) | проверено | 89 | Это самая практичная устойчивая память для реальной эксплуатации. |
| 5 | Subscription auth надо считать policy-sensitive surface | проверено | 82 | Снижает риск построить критичный workflow на нестабильной auth-схеме. |
| 6 | Telegram Business как ограниченный и явно задаваемый канал | проверено | 76 | Это полезно для будущего расширения, но пока не является нашим главным рабочим каналом. |
| 7 | Явные финальные отчеты и pruning сессий как hygiene-layer | вероятно, но не проверено | 72 | Похоже на сильный multiplier, но требует локальной проверки. |
| 8 | Отдельный ingest layer для long-horizon Telegram corpus | вероятно, но не проверено | 68 | Вероятно нужен, но это уже следующий слой, а не первый шаг. |
| 9 | Малые локальные модели как default fallback | спорно или быстро устаревает | 32 | Пока это эксперимент, а не рабочее правило. |

## Концепция траектории развития OpenClaw

### Фаза 1. Операционная корректность

Сначала закрепить то, что уже подтверждено:

- version-aware runbook;
- `status` / `doctor` / port diagnostics как default triage;
- отказ от доверия старым setup recipes без проверки.

### Фаза 2. Управляемая Telegram-поверхность

Сделать Telegram не просто подключенным, а управляемым:

- clear DM policy;
- topic isolation where needed;
- explicit ACL вместо скрытых допущений;
- отдельное понимание, где заканчивается обычный bot surface и где начинается Business-bot scope.

### Фаза 3. Базовый memory-layer на файлах

До любых "умных" memory-экспериментов:

- daily operational notes;
- curated `MEMORY.md`;
- retrieval over curated files;
- только потом оценка более тяжелого ingest/search слоя.

### Фаза 4. Слой corpus intelligence

После стабилизации runtime:

- прогонять corpora через workflow `corpus -> проверка -> triage -> ranking -> roadmap`;
- обновлять реестр знаний;
- собирать не сырые инсайты, а ranked implementation backlog.

### Фаза 5. Контролируемые эксперименты

Только после первых четырех фаз:

- provider diversification;
- subscription auth там, где economics действительно оправдывают риск;
- experiments с local-model fallback;
- Business-bot или long-history ingest expansions.

## Рекомендуемые следующие шаги

1. Закрепить `version-aware runbook` как обязательное operating rule для всех будущих правок `OpenClaw`.
2. Считать Telegram topics/ACL опорной архитектурной единицей, а не UX-деталью.
3. Оформить file-memory baseline как минимальный стандарт.
4. Держать OAuth/subscription-провайдеров в зоне контролируемого риска с регулярной повторной проверкой.
5. Рассматривать Telegram Business как отдельный расширяемый канал, но не как already-approved baseline.
6. Отдельно планировать experiment по corpus ingest только после завершения фаз `1-3`.

## Открытые вопросы

- Нужен ли нам реально отдельный long-horizon ingest уже сейчас, или текущего file-memory baseline пока достаточно?
- Нужен ли Business-bot сценарий вообще, или owner Telegram DM/topic workflow уже покрывает основной use case?
- Хотим ли мы позже нормализовать этот реестр знаний в KB notes, а не хранить только внутри run folder?
