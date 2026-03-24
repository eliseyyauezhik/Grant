<!-- PRIORITY: repo_root/AGENTS.md > workspace/agents.md > scratch-dashboard/AGENTS.md -->
# KB Workspace Agent Rules

You are working inside an Obsidian-compatible vault in the `workspace/` folder.

## Core Rules

- For KB sessions, write-back is mandatory: before ending, update the linked project/progress note, then run sync/export to data views.
- For KB tasks, treat this vault as the working root. If the harness can select cwd, prefer launching from `workspace/`; if launched from the repo root, explicitly read `workspace/agents.md` and restrict KB changes to the `workspace/` folder.
- Create all new working notes in Markdown format.
- Obsidian database views and representations may use the native `.base` format.
- Vault settings in `.obsidian/*.json` are allowed as part of Obsidian configuration.
- Obsidian files in `.obsidian/`, including community plugins in `.obsidian/plugins/`, are not knowledge-base content.
- Do not create `.docx`, `.pdf`, `.rtf`, images, or other binary files inside the vault, except in `_assets_bin/`.
- Respond in Russian by default, unless the user requests otherwise.

## Knowledge Navigation

- Before reading a note, first try to understand its relationships.
- If the `obsidian` CLI is available, use `obsidian links <note>`, `obsidian backlinks <note>`, `obsidian search`, and `obsidian files`.
- If the `obsidian` CLI is unavailable, rely on wikilinks, folder structure, and Markdown file search.
- Do not read notes blindly if you can first narrow context through links.

## Creating New Materials

- Before creating a task, read `[[assets/task-template]]`.
- Before creating a note, read `[[assets/note-template]]`.
- Before creating a service record, read `[[assets/service-template]]`.
- Before creating a source record, read `[[assets/source-template]]`.
- Before creating a runbook, read `[[assets/runbook-template]]`.
- For kanban tasks, first read `[[skills/kanban-skill]]`.
- For capturing unstructured text, first read `[[skills/capture-skill]]`.
- For reviewing and analyzing notes, first read `[[skills/review-skill]]`.

## Opening Files

- After creating a new note, open it via `obsidian open path=<path>` or create it via `obsidian create ... open` if the CLI is available.
- If the CLI is unavailable, report the exact path to the created note and continue without auto-opening.

## Storage Boundaries

- `notes/` stores permanent knowledge and instructions.
- `projects/` stores active working documents, task boards, daily logs, and `.base` views.
- `assets/` stores reference templates.
- `.obsidian/plugins/` stores community plugin service files.
- `_assets_bin/` stores binary attachments that cannot be kept in the main note graph.
