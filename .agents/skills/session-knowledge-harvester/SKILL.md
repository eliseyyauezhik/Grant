---
name: session-knowledge-harvester
description: Extract, categorize, and persist valuable knowledge from AI coding sessions into a structured knowledge library. Use at the end of any substantial session to capture decisions, patterns, bug fixes, resources, and ideas. Do NOT use for trivial Q&A sessions or sessions that produced no reusable insights.
---

# Session Knowledge Harvester

## Purpose

Systematically extract valuable, reusable knowledge from the current session and persist it into the project's knowledge library (`workspace/notes/knowledge-library/`).

## When to Activate

- At the end of any substantial session (architecture work, debugging, research, integration)
- When the agent detects it has made a non-trivial discovery
- When explicitly asked by the user ("запомни", "сохрани знание", "harvest")
- **NOT** for trivial Q&A, simple file edits, or sessions with no reusable insights

## Extraction Process

### Step 1: Session Scan

Review the current session and identify items that match ANY of these criteria:

1. **Reusable** — will be useful in future sessions (not one-off)
2. **Non-trivial** — cannot be found in 30 seconds of googling
3. **Specific** — relates to a concrete project, stack, or workflow
4. **Verified** — was validated/tested in this session

### Step 2: Classify Each Item

For each extracted item, assign:

| Field | Values |
|---|---|
| **Category** | `decision` · `pattern` · `bug-fix` · `resource` · `idea` |
| **Topic** | `project` · `infrastructure` · `knowledge` · `workflow` · `tool` |
| **Project** | `kora` · `hermes` · `openclaw` · `antigravity` · `smartmeeting` · `general` |
| **Integrity** | `verified` · `unverified` · `needs-check` |
| **Priority** | `critical` · `high` · `medium` · `low` |
| **TTL** | `permanent` · `6-months` · `1-month` · `session-only` |

### Step 3: Write to Knowledge Library

Each item becomes a markdown file in the appropriate subdirectory:

```
workspace/notes/knowledge-library/
├── decisions/      # Architecture decisions, tool choices, strategy picks
├── patterns/       # Repeatable approaches, templates, workflows
├── bugs/           # Root cause + fix documentation
├── resources/      # External tools, links, documentation
└── index.md        # Auto-updated index of all entries
```

### File Naming Convention

```
{YYYY-MM-DD}_{short-slug}.md
```

Example: `2026-05-17_crush-replaces-opencode.md`

### Entry Template

```markdown
---
type: knowledge-entry
category: {decision|pattern|bug-fix|resource|idea}
topic: {project|infrastructure|knowledge|workflow|tool}
project: {project-name}
integrity: {verified|unverified|needs-check}
priority: {critical|high|medium|low}
ttl: {permanent|6-months|1-month|session-only}
created: {YYYY-MM-DD}
source_session: {session-id-or-date}
tags: []
---

# {Title}

## Context
{Why this knowledge exists — what problem or situation triggered it}

## Knowledge
{The actual reusable insight, pattern, fix, or decision}

## Evidence
{How was this verified — test results, links, screenshots}

## Related
{Links to related files, other entries, or external resources}
```

### Step 4: Update Index

After writing entries, update `workspace/notes/knowledge-library/index.md`:
- Add new entries to the appropriate category section
- Update the statistics block
- Update `last_updated` date

## Quality Filters

**DO record:**
- Architecture decisions with rationale (especially at "points of no return")
- Bug root causes + fixes (especially non-obvious ones)
- Working configurations (API keys format, server configs, etc.)
- Tool discoveries (new tools, migration paths, compatibility info)
- Workflow patterns that saved time

**DO NOT record:**
- Trivial code changes (rename variable, fix typo)
- Information that's in official docs and easy to find
- Temporary debugging steps that didn't lead anywhere
- Session-specific context that won't apply elsewhere

## Integration Notes

### With Crush (OpenCode successor)
This skill is compatible with the Agent Skills standard (agentskills.io).
Crush will discover it automatically from `.agents/skills/session-knowledge-harvester/SKILL.md`.

### With Claude Code
Place in `.claude/skills/session-knowledge-harvester/SKILL.md` or reference from `CLAUDE.md`.

### With Antigravity
Already loaded as a workspace skill.

### Future: Hook-based Automation
When Crush adds `PostSession` hooks, this skill can be triggered automatically:
```json
{
  "hooks": {
    "PostSession": [{
      "command": "echo 'Run session-knowledge-harvester skill'"
    }]
  }
}
```

## Example Harvest Output

From a session that migrated from Antigravity to Crush:

```markdown
# OpenCode has been archived → Crush is the successor

## Context
User planned migration from Antigravity to OpenCode. Research revealed OpenCode
(opencode-ai/opencode) was archived in 2026 and rebranded as Crush (charmbracelet/crush).

## Knowledge
- OpenCode → Crush (charmbracelet/crush), 24.4k⭐
- Crush natively reads `.agents/skills/SKILL.md` and `AGENTS.md`
- Install on Windows: `winget install charmbracelet.crush`
- Config file: `crush.json` or `.crush.json` in project root
- Crush supports hooks (PreToolUse), MCP (stdio/http/sse), LSP
- Agent Skills standard: agentskills.io

## Evidence
Verified via GitHub README (2026-05-17). Archive notice on opencode-ai/opencode confirmed.
```
