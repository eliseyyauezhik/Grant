---
name: skill-conductor
description: Full lifecycle management for agent skills. Use when creating, evaluating, editing, reviewing, or packaging skills. Do NOT use for general coding tasks or non-skill files.
---

# Skill Conductor

Full lifecycle management for agent skills: design → build → test → evaluate → package.

Synthesized from Anthropic official guide, obra/superpowers, mgechev/best-practices, and OpenClaw skill-creator. Adapted for Antigravity.

## Modes

Detect mode from context. If ambiguous, ask.

1. **CREATE** — new skill from scratch
2. **EDIT** — improve existing skill
3. **EVAL** — TDD-style evaluation of a skill
4. **REVIEW** — assess third-party skill quality
5. **PACKAGE** — validate and package for distribution

---

## Mode 1: CREATE

### Phase 1: Use Cases (do not skip)

Extract 2-3 concrete scenarios before writing anything.

Ask:

- "What specific task should this skill handle?"
- "What would a user say to trigger it?"
- "What should NOT trigger it?"

Conclude when: clear picture of what the skill does, for whom, and when.

### Phase 2: Baseline (TDD RED)

Before writing the skill, verify the agent fails without it:

1. Take one use case from Phase 1
2. Run it in a clean session without the skill
3. Document: what went wrong, what the agent guessed, what it missed
4. This is the baseline. If the agent already handles it perfectly, the skill is unnecessary

Do not skip baseline. If you didn't watch the agent fail, you don't know what to teach.

### Phase 3: Architecture

Choose primary pattern (can combine). See `references/patterns.md` for details.

| Pattern | Use when |
|---|---|
| Sequential workflow | clear step-by-step process |
| Iterative refinement | output improves with cycles |
| Context-aware selection | same goal, different tools by context |
| Domain intelligence | specialized knowledge beyond tool access |
| Multi-service coordination | workflow spans multiple services |

Choose degrees of freedom:

| Freedom | When | Example |
|---|---|---|
| Low (scripts) | fragile, error-prone, must be exact | API calls, file ops |
| Medium (pseudocode) | preferred pattern exists, some variation ok | data processing |
| High (text) | multiple approaches valid, judgment needed | design decisions |

### Phase 4: Scaffold

Initialize skill structure:

```bash
python .agents/skills/skill-conductor/scripts/init_skill.py <skill-name> --path .agents/skills [--resources scripts,references,assets]
```

Or create manually:

```
skill-name/
├── SKILL.md          # required
├── scripts/          # deterministic operations
├── references/       # detailed docs, loaded on demand
└── assets/           # templates, images for output
```

### Phase 5: Write SKILL.md

#### Frontmatter

```yaml
---
name: kebab-case-name
description: [purpose in one sentence]. Use when [triggers]. Do NOT use for [negative triggers].
---
```

Rules (non-negotiable):

- `name`: lowercase, digits, hyphens only. no consecutive hyphens. matches folder name. max 64 chars
- `description`: max 1024 chars. no angle brackets.
- description = purpose + triggers. **NEVER workflow/process steps**
- start triggers with "Use when..."
- include negative triggers ("Do NOT use for...")
- third person, imperative voice

#### Body structure

```markdown
# Skill Name

## Overview
What this enables. 1-2 sentences. Core principle.

## [Main sections]
Step-by-step with numbered sequences.
Concrete templates over prose.
Imperative voice: "Extract the text..." not "You should extract..."

## Common Mistakes
What goes wrong + how to fix.
```

#### Writing rules

- **Imperative, third person.** "Extract the data" not "I will extract"
- **One term per concept.** Pick "template" and stick with it
- **Step-by-step numbering.** Decision trees mapped explicitly
- **Concrete templates > prose.** Pattern-matching beats paragraphs
- **Progressive disclosure.** SKILL.md = brain (<500 lines). References = details
- **No junk files.** No README, CHANGELOG inside the skill
- **Token budget.** Frequently loaded: <200 words. Standard: <500 words. Heavy reference: move to references/

### Phase 6: Verify (TDD GREEN)

Run the same use case from Phase 2, now with the skill active.

1. Does the skill trigger automatically?
2. Does the agent follow instructions from body (not just description)?
3. Does the output meet the use case requirements?
4. Does it NOT trigger on unrelated queries?

If any fail → back to Phase 5.

### Phase 7: Refactor

1. Find new ways the agent rationalizes around the skill
2. Plug loopholes in SKILL.md
3. Re-verify
4. Repeat until stable

---

## Mode 2: EDIT

1. Read the existing SKILL.md completely
2. Identify the problem: undertriggering? overtriggering? wrong execution? missing edge case?
3. Apply fix using Phase 5 writing rules
4. Run Phase 6 verify on the changed behavior
5. Check: did the fix break anything else? (regression)

Common edit patterns:

| Problem | Signal | Fix |
|---|---|---|
| Undertriggering | skill doesn't load | add keywords to description |
| Overtriggering | loads for unrelated queries | add negative triggers |
| Skips body | follows description instead | remove process from description |
| Inconsistent output | varies across sessions | add explicit templates, reduce freedom |
| Too slow | large context | move detail to references/ |

---

## Mode 3: EVAL

TDD-style evaluation. Three stages, run in order.

### Stage 1: Discovery

Generate 6 test prompts: 3 that SHOULD trigger + 3 that should NOT.
Run each in clean session. Target: 6/6.

### Stage 2: Logic

Simulate execution step by step. For each step:

1. What exactly is the agent doing?
2. Which file/script is it reading or running?
3. Flag any execution blockers (ambiguous instructions)

### Stage 3: Edge Cases

Attack the skill:

1. What if a script fails?
2. What if input is malformed?
3. What if multiple skills could trigger simultaneously?

### Scoring

Rate on 5 axes (1-10 each):

| Axis | What it measures |
|---|---|
| Discovery | triggers correctly, doesn't false-trigger |
| Clarity | instructions unambiguous |
| Efficiency | token budget respected |
| Robustness | handles edge cases |
| Completeness | covers stated use cases |

Score: 45-50 production ready, 35-44 solid, 25-34 needs work, <25 rewrite.

Run eval script: `python .agents/skills/skill-conductor/scripts/eval_skill.py <skill-folder>`

---

## Mode 4: REVIEW

Checklist (pass/fail):

```
[ ] SKILL.md exists, exact case
[ ] Valid YAML frontmatter (name + description)
[ ] name: kebab-case, matches folder, ≤64 chars
[ ] description: ≤1024 chars, no angle brackets
[ ] description has triggers ("Use when...")
[ ] description has NO workflow/process steps
[ ] No README.md inside skill folder
[ ] SKILL.md < 500 lines
[ ] References max 1 level deep
[ ] Scripts tested and executable
[ ] No hardcoded paths/tokens/secrets
```

---

## Mode 5: PACKAGE

1. Run REVIEW checklist
2. Run validation: `python .agents/skills/skill-conductor/scripts/quick_validate.py <skill-folder>`
3. Final check: verify structure intact

---

## Quick Reference

### Description formula

```
[One sentence: what it does] + Use when [triggers]. + Do NOT use for [negative triggers].
```

### Success metrics

| Metric | Target |
|---|---|
| Triggering accuracy | ≥90% (5/6 in discovery test) |
| Workflow completion without user correction | ≥80% |
| Failed API/script calls | 0 |
