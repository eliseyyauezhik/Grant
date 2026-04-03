# Research Notes

## 2026-03-30

- Existing outputs already contain the substantive knowledge:
  - `verified_knowledge_roadmap.md` has the library and trajectory.
  - `analytical-node-architecture.md` has the wider system context.
- The user asked for the material in a more convenient form, so the best move is a compact hub note rather than another long analysis file.
- The hub should be the front page, while the current roadmap stays the detailed source.
- A small link-back from the architecture note will make the structure easier to discover later.

## 2026-03-30 - Web briefing and execution surface split

- The user now needs a phone-friendly web page, not another vault note.
- Existing repository context already has a working static publishing pattern via `netlify_publish/` and authenticated `netlify` CLI.
- To avoid touching the existing grant landing, the safest route is a separate static folder and a separate Netlify site for the OpenClaw page.
- The most useful added value beyond the source materials is an explicit split:
  - what can be delegated through Telegram once OpenClaw is already configured;
  - what still requires a stationary computer / Antigravity environment.
- Evidence from the source docs supports a strict boundary:
  - Telegram is a managed surface with explicit ACL/topics;
  - runtime diagnostics, version discipline, channel configuration, file-memory setup, and corpus verification remain desktop-side work.
