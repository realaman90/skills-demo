from __future__ import annotations

import ast
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

BASE_DIR = Path(__file__).resolve().parent
SKILLS_DIR = BASE_DIR / "skills"
ALLOWED_FETCH_DOMAINS = {"example.com", "www.iana.org"}
SKILL_ID_RE = re.compile(r"^[a-z0-9-]+$")
CALC_EXPR_RE = re.compile(r"^[0-9+\-*/().\s]+$")
HTML_TAG_RE = re.compile(r"<[^>]+>")

NOTES: dict[int, dict[str, Any]] = {}
NEXT_NOTE_ID = 1

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("skills_demo")

app = FastAPI(title="Skills + Tools Demo API", version="1.0.0")


class GetSkillRequest(BaseModel):
    skill_id: str = Field(..., min_length=1)


class RunToolRequest(BaseModel):
    tool_name: str = Field(..., min_length=1)
    args: dict[str, Any] = Field(default_factory=dict)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("request method=%s path=%s", request.method, request.url.path)
    response = await call_next(request)
    logger.info(
        "response method=%s path=%s status=%s",
        request.method,
        request.url.path,
        response.status_code,
    )
    return response


def bad_request(error: str, message: str | None = None) -> JSONResponse:
    body: dict[str, Any] = {"error": error}
    if message:
        body["message"] = message
    return JSONResponse(status_code=400, content=body)


def validate_skill_id(skill_id: str) -> bool:
    return bool(SKILL_ID_RE.fullmatch(skill_id))


def extract_skill_metadata(skill_markdown: str) -> dict[str, Any]:
    skill_id = ""
    description = ""
    required_tools: list[str] = []
    in_required_tools = False

    for raw_line in skill_markdown.splitlines():
        line = raw_line.strip()

        if line.startswith("skill_id:"):
            skill_id = line.split(":", 1)[1].strip().strip('"').strip("'")
            in_required_tools = False
            continue

        if line.startswith("description:"):
            description = line.split(":", 1)[1].strip().strip('"').strip("'")
            in_required_tools = False
            continue

        if line.startswith("required_tools:"):
            in_required_tools = True
            inline = line.split(":", 1)[1].strip()
            if inline.startswith("[") and inline.endswith("]"):
                inner = inline[1:-1].strip()
                if inner:
                    required_tools.extend(
                        [
                            item.strip().strip('"').strip("'")
                            for item in inner.split(",")
                            if item.strip()
                        ]
                    )
                in_required_tools = False
            continue

        if in_required_tools:
            if line.startswith("-"):
                tool = line[1:].strip().strip('"').strip("'")
                if tool:
                    required_tools.append(tool)
                continue
            if not line:
                continue
            in_required_tools = False

    return {
        "skill_id": skill_id,
        "description": description,
        "required_tools": required_tools,
    }


def read_skill_file(skill_id: str) -> str:
    skill_path = SKILLS_DIR / skill_id / "SKILL.md"
    if not skill_path.exists():
        raise FileNotFoundError(skill_id)
    return skill_path.read_text(encoding="utf-8")


def safe_calculate(expression: str) -> float | int:
    if not CALC_EXPR_RE.fullmatch(expression):
        raise ValueError("invalid_expression")

    parsed = ast.parse(expression, mode="eval")
    allowed_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.USub,
        ast.UAdd,
        ast.Constant,
    )

    for node in ast.walk(parsed):
        if isinstance(node, ast.Constant):
            if not isinstance(node.value, (int, float)):
                raise ValueError("invalid_expression")
            continue
        if not isinstance(node, allowed_nodes):
            raise ValueError("invalid_expression")

    value = eval(compile(parsed, "<calculator>", "eval"), {"__builtins__": {}}, {})
    if not isinstance(value, (int, float)):
        raise ValueError("invalid_expression")
    return value


def strip_html_light(text: str) -> str:
    text = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", text)
    text = HTML_TAG_RE.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def run_calculator(args: dict[str, Any]) -> dict[str, Any] | JSONResponse:
    expression = str(args.get("expression", "")).strip()
    if not expression:
        return bad_request("invalid_args", "missing expression")

    try:
        value = safe_calculate(expression)
    except Exception:
        return bad_request("invalid_expression")

    return {
        "tool_name": "calculator",
        "output": str(value),
        "data": {"value": value},
    }


def run_now(args: dict[str, Any]) -> dict[str, Any] | JSONResponse:
    tz = args.get("tz")
    if not isinstance(tz, str) or not tz.strip():
        return bad_request("invalid_args", "missing tz")

    try:
        zone = ZoneInfo(tz)
    except ZoneInfoNotFoundError:
        return bad_request("invalid_tz")

    iso_value = datetime.now(zone).isoformat()
    return {
        "tool_name": "now",
        "output": iso_value,
        "data": {"iso": iso_value, "tz": tz},
    }


def run_fetch_url(args: dict[str, Any]) -> dict[str, Any] | JSONResponse:
    url = args.get("url")
    if not isinstance(url, str) or not url.strip():
        return {
            "tool_name": "fetch_url",
            "output": "Error: missing 'url' argument",
            "data": {},
        }

    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or parsed.hostname not in ALLOWED_FETCH_DOMAINS:
        return bad_request("domain_not_allowed")

    try:
        with httpx.Client(timeout=10.0, follow_redirects=True) as client:
            response = client.get(url)
            response.raise_for_status()
    except httpx.HTTPError as exc:
        return bad_request("fetch_failed", str(exc))

    final_host = response.url.host
    if final_host not in ALLOWED_FETCH_DOMAINS:
        return bad_request("domain_not_allowed")

    text = strip_html_light(response.text)[:2000]
    return {
        "tool_name": "fetch_url",
        "output": text,
        "data": {"url": str(response.url), "length": len(text)},
    }


def run_save_note(args: dict[str, Any]) -> dict[str, Any] | JSONResponse:
    global NEXT_NOTE_ID

    title = args.get("title")
    body = args.get("body")
    if not isinstance(title, str) or not isinstance(body, str):
        return bad_request("invalid_args", "title and body must be strings")

    note_id = NEXT_NOTE_ID
    NEXT_NOTE_ID += 1

    note = {"id": note_id, "title": title, "body": body}
    NOTES[note_id] = note

    return {
        "tool_name": "save_note",
        "output": f"Saved note #{note_id}",
        "data": {"id": note_id},
    }


def run_list_notes(args: dict[str, Any]) -> dict[str, Any]:
    _ = args
    notes_list = [NOTES[nid] for nid in sorted(NOTES.keys())]
    if not notes_list:
        output = "No notes."
    else:
        output = "\n".join(
            f'{note["id"]}. {note["title"]}: {note["body"]}' for note in notes_list
        )

    return {
        "tool_name": "list_notes",
        "output": output,
        "data": {"notes": notes_list},
    }


@app.get("/health")
async def health() -> dict[str, bool]:
    return {"ok": True}


@app.get("/skills")
async def list_skills() -> dict[str, list[dict[str, Any]]]:
    skills: list[dict[str, Any]] = []
    if not SKILLS_DIR.exists():
        return {"skills": skills}

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        metadata = extract_skill_metadata(skill_file.read_text(encoding="utf-8"))
        if metadata["skill_id"] and metadata["description"]:
            skills.append(
                {
                    "skill_id": metadata["skill_id"],
                    "description": metadata["description"],
                    "required_tools": metadata["required_tools"],
                }
            )

    return {"skills": skills}


@app.post("/get_skill")
async def get_skill(payload: GetSkillRequest):
    if not validate_skill_id(payload.skill_id):
        return bad_request("invalid_skill_id")

    try:
        content = read_skill_file(payload.skill_id)
    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"error": "skill_not_found"})

    return {
        "skill_id": payload.skill_id,
        "content": content,
        "source": "local",
    }


@app.post("/run_tool")
async def run_tool(payload: RunToolRequest):
    tool_name = payload.tool_name.strip()

    if tool_name == "calculator":
        return run_calculator(payload.args)
    if tool_name == "now":
        return run_now(payload.args)
    if tool_name == "fetch_url":
        return run_fetch_url(payload.args)
    if tool_name == "save_note":
        return run_save_note(payload.args)
    if tool_name == "list_notes":
        return run_list_notes(payload.args)

    return bad_request("unknown_tool")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
