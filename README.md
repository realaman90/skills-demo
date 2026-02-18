# Agent Skills Builder + Actions API

Small production-style demo that converts `./docs` into AgentSkills-style folders and serves them through a ChatGPT Actions-compatible API.

## Project Layout

```text
/
  app.py
  builder.py
  requirements.txt
  openapi.yaml
  README.md
  docs/
  skills/
    <skill_id>/
      SKILL.md
      references/
        INDEX.md
        source/
        normalized/
      assets/
```

## Quickstart (Local)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python builder.py
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

Local health check:

```bash
curl -s http://localhost:8000/health
```

## Railway Deploy

Use this start command:

```bash
python -m uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}
```

Recommended deploy flow:
1. Push this repo to GitHub.
2. Create a Railway service from the repo.
3. Confirm build installs `requirements.txt`.
4. Set start command above.
5. Redeploy and verify `/health`.

## Connect to Custom GPT (Actions)

1. Open GPT Builder and go to **Actions**.
2. Import `openapi.yaml`.
3. Replace `https://YOUR_DOMAIN` in `openapi.yaml` with your Railway URL.
4. Save and run test calls for:
   - `list_skills`
   - `get_skill`
   - `get_skill_file`
   - `search_docs`

## Paste-Ready Custom GPT Instructions (Router)

```text
You are a strict skill router that must use Actions for all skill content.

Rules:
1) If the user asks "what skills do you have" or equivalent, call `list_skills` first.
2) Select the best skill_id, then call `get_skill` before doing any task.
3) Read only minimum files with `get_skill_file` first (start with references/INDEX.md).
4) Use `search_docs` for targeted lookups when specific details are missing.
5) Final output MUST begin with the skill's VERIFICATION STRING exactly.
6) Include a section titled exactly: Compliance Checklist.
7) In "Sources Used", include short evidence quotes with citations (and line ranges if available), not only bare file paths.
8) If any required tool call fails or returns empty critical info, do not answer from memory; report the failure and request retry/context.
```

## API Overview

- `GET /health` -> `{"ok": true}`
- `GET /skills` -> list parsed skill metadata from `skills/*/SKILL.md`
- `POST /get_skill` -> returns SKILL.md text
- `POST /get_skill_file` -> returns file text from `references/` or `assets/`
- `POST /search_docs` -> keyword search in `references/normalized` + `references/source` (`.md`/`.txt`)

## Troubleshooting

### `invalid_args` (missing required fields)
- Ensure request JSON includes all required fields:
  - `get_skill`: `skill_id`
  - `get_skill_file`: `skill_id`, `path`
  - `search_docs`: `skill_id`, `query` (and optional `top_k`)

### Path validation failures
- `path` must be relative.
- `path` must start with `references/` or `assets/`.
- `path` cannot contain `..` or absolute prefixes.

### Empty search results
- Rebuild skills after adding docs: `python builder.py`.
- Query with narrower keywords (`"tone"`, `"claim"`, `"terminology"`).
- Confirm content exists under `skills/<skill_id>/references/normalized` or `source`.

### `run_tool` 404 or "requires approval"
- Re-import the latest `openapi.yaml` in Custom GPT Actions so only current operations are used.
- Confirm your actions list includes: `list_skills`, `get_skill`, `get_skill_file`, `search_docs`.
- If a stale config still calls `run_tool`, the backend now returns a compatibility response instead of 404.
