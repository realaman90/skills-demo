# skills-demo

Minimal standalone demo for testing ChatGPT Custom GPT Actions tool-calling with local `SKILL.md` files.

## Project structure

```text
skills-demo/
  app.py
  requirements.txt
  openapi.yaml
  README.md
  skills/
    hello-skill/SKILL.md
    calc/SKILL.md
    fetch-and-summarize/SKILL.md
    notes/SKILL.md
    router-test/SKILL.md
```

## Setup and run

```bash
cd skills-demo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Base URL (local): `http://localhost:8000`

## curl examples

`GET /health`

```bash
curl -s http://localhost:8000/health
```

`GET /skills`

```bash
curl -s http://localhost:8000/skills
```

`POST /get_skill`

```bash
curl -s -X POST http://localhost:8000/get_skill \
  -H "Content-Type: application/json" \
  -d '{"skill_id":"calc"}'
```

`POST /run_tool` (calculator)

```bash
curl -s -X POST http://localhost:8000/run_tool \
  -H "Content-Type: application/json" \
  -d '{"tool_name":"calculator","args":{"expression":"((3+5)*2)/7"}}'
```

`POST /run_tool` (now)

```bash
curl -s -X POST http://localhost:8000/run_tool \
  -H "Content-Type: application/json" \
  -d '{"tool_name":"now","args":{"tz":"Europe/Stockholm"}}'
```

`POST /run_tool` (fetch_url, allowlist-only)

```bash
curl -s -X POST http://localhost:8000/run_tool \
  -H "Content-Type: application/json" \
  -d '{"tool_name":"fetch_url","args":{"url":"https://example.com"}}'
```

`POST /run_tool` (save_note and list_notes)

```bash
curl -s -X POST http://localhost:8000/run_tool \
  -H "Content-Type: application/json" \
  -d '{"tool_name":"save_note","args":{"title":"todo","body":"ship demo"}}'

curl -s -X POST http://localhost:8000/run_tool \
  -H "Content-Type: application/json" \
  -d '{"tool_name":"list_notes","args":{}}'
```

## Import into Custom GPT Actions

1. Run this API and expose it publicly (see next section).
2. In GPT Builder, open **Actions** and import `openapi.yaml`.
3. Replace `https://YOUR_DOMAIN` in `openapi.yaml` with your public URL.
4. Save, test an action call, then test full skill execution.

## Expose local server

Use either tunnel option:

```bash
# ngrok
ngrok http 8000

# cloudflared
cloudflared tunnel --url http://localhost:8000
```

Copy the generated HTTPS URL and update `openapi.yaml` server URL.

## Cloud deploy start command

If your platform expects `main:app`, use:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Local development can still use:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## Suggested Custom GPT Instructions (router logic)

Use this as a starting instruction block for your Custom GPT:

```text
You are a strict skill router.

Rules:
1) If the user asks "what can you do" (or equivalent), always call list_skills first and summarize the returned skills.
2) Before executing any skill behavior, always call get_skill with the chosen skill_id and read the full SKILL.md.
3) Parse required_tools from SKILL.md and call run_tool for each required tool step.
4) Follow the steps section from SKILL.md deterministically.
5) In the final user answer, put the skill's VERIFICATION STRING as the first line verbatim.
6) If a tool call fails, report the tool error and stop.
```

## Notes

- `/skills` and `/get_skill` read local files from `./skills` only.
- Demo has no auth by design.
- `fetch_url` is restricted to: `example.com`, `www.iana.org`.
