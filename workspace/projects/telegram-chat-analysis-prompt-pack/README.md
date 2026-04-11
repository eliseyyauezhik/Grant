# Telegram Chat Analysis Prompt Pack

## Summary

Набор файлов для нового чата, в котором нейросеть будет анализировать базу Telegram-сообщений поэтапно: извлечение утверждений, объединение и тематизация, затем дополнительное исследование и инструкция по настройке агента. Пакет рассчитан на работу с русскоязычными данными при английских инструкциях.

## Key Points

- Source of truth:
  - `master_prompt.md` — полный методический каркас
  - `system_instruction.md` — короткие постоянные правила
  - `production_prompt_unified.md` — единый боевой промпт
  - `production_prompt_stage1_claim_extraction.md`
  - `production_prompt_stage2_consolidation_topics.md`
  - `production_prompt_stage3_research_and_agent_tuning.md`
  - `stage1_claims_schema.json`
  - `stage2_topics_schema.json`
  - `final_analysis_schema.json`
- Рекомендуемый входной формат базы:
  - основной — `JSON`
  - дополнительный reference — `HTML` при наличии
- Язык использования:
  - инструкции — английский
  - исходные данные — в оригинале
  - итоговые объясняющие поля — русский

## How To Use In A New Chat

1. Прикрепить экспорт Telegram-базы, предпочтительно `JSON`.
2. Дать нейросети сначала прочитать этот файл.
3. Передать `system_instruction.md` как постоянную инструкцию.
4. Запускать по порядку:
   - `production_prompt_stage1_claim_extraction.md` + `stage1_claims_schema.json`
   - `production_prompt_stage2_consolidation_topics.md` + `stage2_topics_schema.json`
   - `production_prompt_stage3_research_and_agent_tuning.md` + `final_analysis_schema.json`
5. Если нужен один прогон вместо трёх:
   - использовать `production_prompt_unified.md` + `final_analysis_schema.json`
6. Если нужно перепроверить качество логики:
   - сверяться с `master_prompt.md`

## Paste-Ready Instruction For The Next Model

```text
Read `workspace/projects/telegram-chat-analysis-prompt-pack/README.md` first.

Then use the files in `workspace/projects/telegram-chat-analysis-prompt-pack/` as the operating prompt pack for the attached Telegram chat database.

Working rules:
- Use `system_instruction.md` as the stable instruction layer.
- Use the stage prompts and matching JSON schemas in order.
- Prefer staged processing over one giant run.
- Analyze source messages in the original language.
- Do not translate quotes, URLs, commands, usernames, or filenames unless explicitly requested.
- Write explanatory output fields in Russian.
- Do not treat repeated chat statements as verified facts.
- Preserve chronology, links, contradictions, and topic evolution.
- In the agent-tuning stage, backup first before any change.
```

## Recommended Operating Mode

- Best mode:
  - staged pipeline
  - strict JSON outputs
  - human-readable recap after each stage
- Fallback mode:
  - unified prompt
  - final schema

## Links

- Related:
  - `master_prompt.md`
  - `system_instruction.md`
  - `production_prompt_unified.md`
- Source:
  - Telegram export to be attached in the next chat

## Next Actions

- [ ] В новом чате прикрепить экспорт Telegram-базы
- [ ] Запустить Stage 1 на `JSON`-экспорте
- [ ] После Stage 1 перейти к Stage 2 и Stage 3
- [ ] Собрать итоговый аналитический документ

## Sync Signal

- KB write-back выполнен в этот пакет.
- Отдельный sync/export pipeline в репозитории для этого материала не обнаружен; пакет готов как source-of-truth для следующей сессии.

## Tags

#note #prompt-pack #telegram #analysis #llm
