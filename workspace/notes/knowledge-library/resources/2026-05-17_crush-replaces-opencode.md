---
type: knowledge-entry
category: resource
topic: tool
project: antigravity
integrity: verified
priority: critical
ttl: permanent
created: 2026-05-17
source_session: antigravity-migration-session
tags: [migration, opencode, crush, agent-skills, infrastructure]
---

# OpenCode архивирован → Crush — преемник

## Context
При планировании миграции из Antigravity в OpenCode обнаружено, что OpenCode (opencode-ai/opencode) был архивирован. Проект продолжается под именем Crush от Charm team.

## Knowledge

### Crush (charmbracelet/crush)
- **GitHub:** github.com/charmbracelet/crush — 24.4k⭐, 3369 коммитов
- **Статус:** активная разработка, MIT лицензия
- **Установка Windows:** `winget install charmbracelet.crush` или `scoop install crush`
- **Конфиг:** `crush.json` или `.crush.json` в корне проекта
- **Глобальный конфиг:** `$HOME/.config/crush/crush.json` (Unix), `%LOCALAPPDATA%\crush\crush.json` (Windows)

### Ключевые фичи
- **AGENTS.md** — читает нативно, совместимо на 100% с текущим форматом
- **Agent Skills** — `.agents/skills/*/SKILL.md` поддерживается нативно (стандарт agentskills.io)
- **MCP** — stdio, http, sse (три транспорта)
- **Hooks** — PreToolUse (блокировка, перезапись, логирование, auto-approve)
- **Custom Commands** — `.crush/commands/*.md` с поддержкой аргументов
- **LSP** — встроенная поддержка Language Server Protocol
- **Auto Compact** — автосжатие контекста при 95% окна
- **SQLite** — встроенная база для сессий
- **Multi-provider** — OpenAI, Anthropic, Gemini, GitHub Copilot, Groq, OpenRouter, Bedrock, Azure

### Где Crush ищет скиллы (Windows)
1. `%LOCALAPPDATA%\agents\skills\`
2. `%LOCALAPPDATA%\crush\skills\`
3. `.agents/skills/` (в проекте)
4. `.crush/skills/` (в проекте)
5. `.claude/skills/` (совместимость с Claude Code)
6. Дополнительные пути через `options.skills_paths`

### Совместимость Antigravity → Crush
| Компонент | Совместимость |
|---|---|
| AGENTS.md | 100% |
| .agents/skills/ | 100% |
| MCP-серверы | 95% (другой формат конфига) |
| Handovers | 100% (обычные .md файлы) |
| Knowledge Items | 0% (нет аналога, экспорт в vault) |
| Brain sessions | 0% (другой формат хранения) |

## Evidence
- Архивная пометка на opencode-ai/opencode (проверено 2026-05-17)
- README charmbracelet/crush (проверено 2026-05-17)
- agentskills.io спецификация (проверено 2026-05-17)

## Related
- [migration-plan.md](../../../.agents/handovers/) — полный план миграции
- [crush.json](../../../crush.json) — готовый конфиг для проекта
- [AGENTS.md](../../../AGENTS.md) — главные правила (совместимы)
