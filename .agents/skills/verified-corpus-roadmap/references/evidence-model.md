# Evidence Model

## Source Priority

Use sources in this order:

1. official docs, specs, API references
2. official releases, changelog, release policy
3. official issues, maintainer comments, provider policy pages
4. first-party blog posts and FAQ
5. the corpus itself
6. secondary summaries

Rule: `5-6` may suggest a lead, but they do not overrule `1-3`.

## Baskets

### `verified`

- Primary source exists.
- No active official contradiction.
- Safe to use as a roadmap premise.

### `probable_but_unverified`

- Strong signal in the corpus.
- Partial or indirect primary evidence.
- Useful for backlog and experiments, not for hard rules.

### `volatile_or_contradicted`

- Time-sensitive, weakly supported, contradicted, or heavily version-dependent.
- Keep visible, but do not use as a default operating rule.

## Scoring

Use `1..5` on each axis:

- `evidence_strength`
- `applicability`
- `impact`
- `volatility`
- `effort`

Formula:

```text
(evidence_strength * 0.30 +
 applicability     * 0.25 +
 impact            * 0.25 +
 (6 - volatility)  * 0.10 +
 (6 - effort)      * 0.10) * 20
```

Interpretation:

- `85-100`: top priority
- `70-84`: important next layer
- `50-69`: controlled experiment or backlog
- `<50`: do not promote to default practice yet

## Minimum Ledger Fields

- claim
- corpus source or topic
- primary source
- source tier
- basket
- implication
- score
