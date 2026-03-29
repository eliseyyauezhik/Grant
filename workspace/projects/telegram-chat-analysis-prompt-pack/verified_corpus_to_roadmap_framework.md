# Verified Corpus-to-Roadmap Framework

## Purpose

Этот framework превращает Telegram/chat/database corpus не просто в summary, а в проверяемый набор знаний и план внедрения. Логика одна и та же:

1. извлечь claims и high-signal patterns;
2. проверить их по первичным источникам;
3. разложить по evidence-buckets;
4. проранжировать по практической ценности;
5. собрать удобный roadmap и список внедренческих шагов.

## Source Priority

Использовать источники по убыванию доверия:

1. official docs, specs, API references;
2. official changelog, releases, release policy;
3. official issues, maintainer comments, provider policy pages;
4. first-party blog posts and FAQ;
5. corpus itself;
6. secondary summaries and forum retellings.

Правило: источники уровней `5-6` не могут опровергать `1-3`. Они только подсказывают, что именно нужно проверить.

## Evidence Buckets

### `verified`

Критерий:
- claim подтвержден хотя бы одним первичным источником;
- нет актуального официального противоречия;
- формулировка очищена от лишней интерпретации.

Использование:
- можно включать в roadmap как опорную практику;
- можно переносить в reusable skill/reference.

### `probable_but_unverified`

Критерий:
- claim выглядит правдоподобным и полезным;
- есть повторяемый сигнал в corpus;
- но первичная проверка пока неполная, косвенная или устаревающая.

Использование:
- можно держать в backlog экспериментов;
- нельзя продвигать как твердый operating rule.

### `volatile_or_contradicted`

Критерий:
- claim time-sensitive, спорный, конфликтный или опирается на слабые источники;
- или официальные источники подтверждают только часть формулировки.

Использование:
- хранить как зону осторожности;
- не делать основой архитектурных решений без новой проверки.

## Scoring Rubric

Каждый item оценивается по шкале `1..5`.

### Positive axes

- `evidence_strength`
  - `5`: verified
  - `3`: probable but unverified
  - `1`: volatile or contradicted
- `applicability`
  - насколько знание применимо к нашему текущему `OpenClaw` и смежным проектам
- `impact`
  - насколько сильно item меняет стабильность, качество или стоимость работы

### Negative axes

- `volatility`
  - насколько быстро item устаревает
- `effort`
  - насколько дорого внедрять или проверять item в реальной среде

## Priority Formula

```text
priority_score =
  (evidence_strength * 0.30 +
   applicability     * 0.25 +
   impact            * 0.25 +
   (6 - volatility)  * 0.10 +
   (6 - effort)      * 0.10) * 20
```

Интерпретация:

- `85-100`: делать в первую очередь, это почти опорный слой
- `70-84`: важный следующий слой
- `50-69`: осмысленный backlog или controlled experiment
- `<50`: не делать default-практикой без новой проверки

## Required Outputs

Минимальный набор артефактов:

1. `verification ledger`
   - claim
   - source tier
   - primary source
   - bucket
   - implication
2. `ranked knowledge register`
   - score
   - applicability
   - impact
   - volatility
   - effort
3. `human-readable roadmap`
   - what is stable
   - what is useful but still experimental
   - what sequence of changes follows from this
4. `open questions`
   - что еще нужно проверить позже

## Recommended Sequence

1. Reuse existing structured outputs if they already exist.
2. Verify only roadmap-relevant claims first, not every sentence in the corpus.
3. Bucket before ranking.
4. Rank before writing implementation steps.
5. Only after the ranked register is stable, package the workflow as a skill or KB artifact.
