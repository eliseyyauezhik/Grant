# OpenClaw Corpus: Verified Knowledge Library and Roadmap

## Status

Собрано по состоянию на `2026-03-30` на базе:

- Telegram corpus `OpenClaw Lab Community`
- staged outputs `stage1_claims.json`, `stage2_topics.json`, `final_analysis.json`
- external verification pass по первичным источникам

## Primary Sources Checked

- OpenClaw Release Policy  
  `https://docs.openclaw.ai/reference/RELEASING`
- OpenClaw Telegram channel docs  
  `https://docs.openclaw.ai/channels/telegram`
- OpenClaw Doctor docs  
  `https://docs.openclaw.ai/gateway/doctor`
- OpenClaw FAQ on Anthropic subscription auth  
  `https://docs.openclaw.ai/help/faq`
- Telegram Business Bot recipients schema  
  `https://core.telegram.org/constructor/businessBotRecipients`

## What Is Actually Verified

### 1. Version-aware operations are mandatory

Bucket: `verified`

Почему:
- у OpenClaw есть публичные release lanes `stable`, `beta`, `dev`;
- stable tags именуются по схеме `YYYY.M.D`;
- значит советы из чатов и старых гайдов нельзя переносить без сверки по версии.

Implication:
- любой change-plan по `OpenClaw` надо читать через конкретную версию, а не через "в чате советовали".

### 2. Telegram surface is explicit, not implicit

Bucket: `verified`

Почему:
- Telegram в OpenClaw конфигурируется через явный `botToken` и channel config;
- DM pairing и group/topic behavior описаны явно;
- forum topics изолируются через session keys с `:topic:<threadId>`.

Implication:
- Telegram architecture надо проектировать как ACL/topic layer, а не как свободный чат без границ.

### 3. Runtime diagnostics matter as much as prompts

Bucket: `verified`

Почему:
- `doctor` проверяет runtime, портовые конфликты, Node environment и канал-зависимые prerequisites;
- docs отдельно предупреждают, что Telegram требует корректного Node-based gateway runtime.

Implication:
- silent failures сначала диагностируются через runtime/channel checks, а не через переписывание prompt files.

### 4. Workspace memory is a first-class operational layer

Bucket: `verified`

Почему:
- docs `doctor` прямо советуют workspace memory system;
- staged corpus и official docs сходятся в одном: файл-память важнее надежды на бесконечный live context.

Implication:
- базовый `OpenClaw` roadmap должен включать memory baseline как обязательный слой, а не как optional nice-to-have.

### 5. Anthropic subscription auth технически поддержан, но policy-risk никуда не исчезает

Bucket: `verified`

Почему:
- FAQ OpenClaw подтверждает поддержку `setup-token` и Anthropic API key;
- там же явно сказано: это technical compatibility, not a policy guarantee.

Implication:
- subscription-based auth нельзя считать твердым production-baseline без регулярной проверки текущих условий.

## What Looks Useful But Is Not Yet Fully Verified

### 1. Separate corpus ingest for long Telegram history

Bucket: `probable_but_unverified`

Signal:
- corpus устойчиво толкает в сторону отдельного ingest/retrieval pipeline для длинной истории.

Why not fully verified:
- официальный источник подтверждает важность workspace memory, но не дает прямой нормы "Telegram history -> separate vector ingest" как обязательный стандарт.

### 2. Silent-failure mitigation through explicit final reports and session pruning

Bucket: `probable_but_unverified`

Signal:
- corpus repeatedly links degraded behavior with session bloat and poor completion signaling.

Why not fully verified:
- это strong operational heuristic, но пока не подтвержден как явное official rule.

### 3. Business-bot access should be treated as a scoped surface, not a full inbox mirror

Bucket: `probable_but_unverified`

Signal:
- Telegram schema явно разделяет `existing_chats` и `new_chats`, то есть доступ к private chats granular;
- corpus правдоподобно трактует Business bot как отдельную governed surface.

Why not fully verified:
- для production-практики нужен живой end-to-end test на конкретном аккаунте и текущих Telegram settings.

## What Should Stay Experimental

### 1. Small local models as default operational fallback

Bucket: `volatile_or_contradicted`

Причина:
- corpus дает слабый и неповторенный сигнал;
- официальных подтверждений, что это хороший default именно для нашего `OpenClaw`, нет.

### 2. Production-ready bundle around memU + pgvector + Telegram Business

Bucket: `volatile_or_contradicted`

Причина:
- идея выглядит перспективно, но в текущем verification-pass она не собрана из достаточного числа первичных подтверждений.

## Ranking

Formula:

```text
(evidence * 0.30 + applicability * 0.25 + impact * 0.25 + (6 - volatility) * 0.10 + (6 - effort) * 0.10) * 20
```

| Rank | Item | Bucket | Score | Why it matters |
|---|---|---|---:|---|
| 1 | Version-aware operations and release discipline | verified | 98 | Без этого любой чужой совет может оказаться поломанным по версии. |
| 2 | Explicit Telegram channel, pairing, topics and ACL | verified | 96 | Это базовая граница безопасности и предсказуемости канала. |
| 3 | Runtime-first diagnostics before prompt tweaking | verified | 91 | Быстро сокращает ложные гипотезы и экономит время на triage. |
| 4 | Workspace memory baseline (`daily notes` + `MEMORY.md` + retrieval) | verified | 89 | Это самая практичная устойчивая память для реальной эксплуатации. |
| 5 | Treat subscription OAuth as policy-sensitive surface | verified | 82 | Снижает риск построить критичный workflow на нестабильной auth-схеме. |
| 6 | Explicit final reports and session pruning for silent-failure hygiene | probable_but_unverified | 72 | Похоже на сильный operational multiplier, но требует локальной проверки. |
| 7 | Separate ingest layer for long-horizon Telegram corpus | probable_but_unverified | 68 | Вероятно нужен, но это уже следующий слой, а не первый шаг. |
| 8 | Small local models as default fallback | volatile_or_contradicted | 32 | Пока это эксперимент, а не рабочее правило. |

## Concept Trajectory for OpenClaw

### Phase 1. Operational correctness

Сначала закрепить то, что уже подтверждено:

- version-aware runbook;
- `status` / `doctor` / port diagnostics as default triage;
- отказ от доверия старым setup recipes без проверки.

### Phase 2. Governed Telegram surface

Сделать Telegram не просто подключенным, а управляемым:

- clear DM policy;
- topic isolation where needed;
- explicit ACL instead of hidden assumptions;
- отдельное понимание, где заканчивается обычный bot surface и где начинается Business-bot scope.

### Phase 3. File memory baseline

До любых "умных" memory-экспериментов:

- daily operational notes;
- curated `MEMORY.md`;
- retrieval over curated files;
- только потом оценка более тяжелого ingest/search слоя.

### Phase 4. Corpus intelligence layer

После стабилизации runtime:

- прогонять corpora через verified corpus-to-roadmap workflow;
- обновлять knowledge register;
- собирать не сырые инсайты, а ranked implementation backlog.

### Phase 5. Controlled experiments

Только после первых четырех фаз:

- provider diversification;
- subscription auth where economics justify the risk;
- local-model fallback experiments;
- Business-bot or long-history ingest expansions.

## Recommended Next Actions

1. Закрепить `version-aware runbook` как обязательный operating rule для всех будущих правок `OpenClaw`.
2. Считать Telegram topics/ACL опорной архитектурной единицей, а не UX-деталью.
3. Оформить file-memory baseline как минимальный стандарт.
4. Держать OAuth/subscription-провайдеров в зоне контролируемого риска с регулярной повторной проверкой.
5. Отдельно спланировать future experiment по corpus ingest только после завершения фаз `1-3`.

## Open Questions

- Нужен ли нам реально отдельный long-horizon ingest уже сейчас, или текущего file-memory baseline пока достаточно?
- Нужен ли Business-bot сценарий вообще, или owner Telegram DM/topic workflow уже покрывает основной use case?
- Хотим ли мы позже нормализовать этот knowledge register в KB notes, а не хранить только внутри run folder?
