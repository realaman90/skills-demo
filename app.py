from __future__ import annotations

import logging
import os
import re
import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
SKILLS_DIR = BASE_DIR / "skills"
SKILL_ID_RE = re.compile(r"^[a-z0-9-]+$")
TEXT_FILE_EXTENSIONS = {".md", ".txt"}

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("agent_skills_actions")

app = FastAPI(title="Agent Skills Actions API", version="1.0.0")


class GetSkillRequest(BaseModel):
    skill_id: str = Field(..., min_length=1)


class GetSkillFileRequest(BaseModel):
    skill_id: str = Field(..., min_length=1)
    path: str = Field(..., min_length=1)


class SearchDocsRequest(BaseModel):
    skill_id: str = Field(..., min_length=1)
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


class RunToolCompatRequest(BaseModel):
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


def parse_skill_metadata(skill_markdown: str) -> dict[str, Any]:
    skill_id = ""
    name = ""
    description = ""
    required_tools: list[str] = []
    in_required_tools = False

    for raw_line in skill_markdown.splitlines():
        line = raw_line.strip()

        if line.startswith("skill_id:"):
            skill_id = line.split(":", 1)[1].strip().strip('"').strip("'")
            in_required_tools = False
            continue
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip().strip('"').strip("'")
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
            if line == "":
                continue
            in_required_tools = False

    return {
        "skill_id": skill_id,
        "name": name,
        "description": description,
        "required_tools": required_tools,
    }


def normalize_and_validate_path(raw_path: str) -> str | None:
    path = raw_path.replace("\\", "/").strip()
    if not path:
        return None
    if path.startswith("/"):
        return None

    as_path = Path(path)
    if as_path.is_absolute():
        return None
    if ".." in as_path.parts:
        return None

    normalized = as_path.as_posix()
    if not (
        normalized.startswith("references/")
        or normalized.startswith("assets/")
    ):
        return None
    return normalized


def read_file_text(path: Path) -> str:
    if path.suffix.lower() in TEXT_FILE_EXTENSIONS:
        return path.read_text(encoding="utf-8", errors="replace")
    return path.read_bytes().decode("latin-1", errors="replace")


def resolve_skill_dir(skill_id: str) -> Path:
    return SKILLS_DIR / skill_id


def _json_response_to_dict(response: JSONResponse) -> dict[str, Any]:
    try:
        return json.loads(response.body.decode("utf-8"))
    except Exception:
        return {"error": "request_failed"}


@app.get("/health", operation_id="health")
async def health() -> dict[str, bool]:
    return {"ok": True}


@app.get("/skills", operation_id="list_skills")
async def list_skills() -> dict[str, list[dict[str, Any]]]:
    skills: list[dict[str, Any]] = []
    if not SKILLS_DIR.exists():
        return {"skills": skills}

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue

        metadata = parse_skill_metadata(skill_md.read_text(encoding="utf-8", errors="replace"))
        if not metadata["skill_id"]:
            metadata["skill_id"] = skill_dir.name

        skills.append(
            {
                "skill_id": metadata["skill_id"],
                "name": metadata["name"],
                "description": metadata["description"],
                "required_tools": metadata["required_tools"],
            }
        )

    return {"skills": skills}


@app.post("/get_skill", operation_id="get_skill")
async def get_skill(payload: GetSkillRequest):
    if not validate_skill_id(payload.skill_id):
        return bad_request("invalid_skill_id")

    skill_md = resolve_skill_dir(payload.skill_id) / "SKILL.md"
    if not skill_md.exists():
        return JSONResponse(status_code=404, content={"error": "skill_not_found"})

    return {
        "skill_id": payload.skill_id,
        "content": skill_md.read_text(encoding="utf-8", errors="replace"),
    }


@app.post("/get_skill_file", operation_id="get_skill_file")
async def get_skill_file(payload: GetSkillFileRequest):
    if not validate_skill_id(payload.skill_id):
        return bad_request("invalid_skill_id")

    normalized_path = normalize_and_validate_path(payload.path)
    if not normalized_path:
        return bad_request("invalid_path")

    skill_dir = resolve_skill_dir(payload.skill_id)
    if not skill_dir.exists():
        return JSONResponse(status_code=404, content={"error": "skill_not_found"})

    target = (skill_dir / normalized_path).resolve()
    if not str(target).startswith(str(skill_dir.resolve())):
        return bad_request("invalid_path")

    if not target.exists() or not target.is_file():
        return JSONResponse(status_code=404, content={"error": "file_not_found"})

    return {
        "skill_id": payload.skill_id,
        "path": normalized_path,
        "content": read_file_text(target),
    }


@app.post("/search_docs", operation_id="search_docs")
async def search_docs(payload: SearchDocsRequest):
    if not validate_skill_id(payload.skill_id):
        return bad_request("invalid_skill_id")
    if not payload.query.strip():
        return bad_request("invalid_args", "query cannot be empty")

    skill_dir = resolve_skill_dir(payload.skill_id)
    if not skill_dir.exists():
        return JSONResponse(status_code=404, content={"error": "skill_not_found"})

    tokens = re.findall(r"[a-z0-9]+", payload.query.lower())
    if not tokens:
        return bad_request("invalid_args", "query must contain alphanumeric tokens")

    search_roots = [
        skill_dir / "references" / "normalized",
        skill_dir / "references" / "source",
    ]
    candidate_files: list[Path] = []
    for root in search_roots:
        if not root.exists():
            continue
        for file_path in root.rglob("*"):
            if not file_path.is_file():
                continue
            if file_path.suffix.lower() in TEXT_FILE_EXTENSIONS:
                candidate_files.append(file_path)

    hits: list[dict[str, Any]] = []
    for file_path in sorted(candidate_files):
        text = read_file_text(file_path)
        if not text.strip():
            continue

        lower_text = text.lower()
        score = sum(lower_text.count(token) for token in tokens)
        if score <= 0:
            continue

        lines = text.splitlines()
        if not lines:
            lines = [text]

        best_idx = 0
        best_line_score = -1
        for idx, line in enumerate(lines):
            line_lower = line.lower()
            line_score = sum(line_lower.count(token) for token in tokens)
            if line_score > best_line_score:
                best_line_score = line_score
                best_idx = idx

        start = max(0, best_idx - 10)
        end = min(len(lines), best_idx + 11)
        snippet = "\n".join(lines[start:end]).strip()
        if len(snippet) > 3000:
            snippet = snippet[:3000].rstrip() + "..."

        hits.append(
            {
                "path": file_path.relative_to(skill_dir).as_posix(),
                "score": score,
                "snippet": snippet,
                "start_line": start + 1,
                "end_line": end,
            }
        )

    hits.sort(key=lambda item: (-int(item["score"]), item["path"]))
    return {"hits": hits[: payload.top_k]}


@app.post("/run_tool", operation_id="run_tool_compat")
async def run_tool_compat(payload: RunToolCompatRequest):
    tool_name = payload.tool_name.strip()
    args = payload.args or {}

    if tool_name == "get_skill":
        skill_id = args.get("skill_id")
        if not isinstance(skill_id, str):
            return {
                "tool_name": tool_name,
                "output": "Error: missing required arg 'skill_id'",
                "data": {},
            }
        result = await get_skill(GetSkillRequest(skill_id=skill_id))
        if isinstance(result, JSONResponse):
            body = _json_response_to_dict(result)
            return {
                "tool_name": tool_name,
                "output": f"Error: {body.get('error', 'request_failed')}",
                "data": body,
            }
        return {
            "tool_name": tool_name,
            "output": "ok",
            "data": result,
        }

    if tool_name == "get_skill_file":
        skill_id = args.get("skill_id")
        path = args.get("path")
        if not isinstance(skill_id, str) or not isinstance(path, str):
            return {
                "tool_name": tool_name,
                "output": "Error: missing required args 'skill_id' and/or 'path'",
                "data": {},
            }
        result = await get_skill_file(GetSkillFileRequest(skill_id=skill_id, path=path))
        if isinstance(result, JSONResponse):
            body = _json_response_to_dict(result)
            return {
                "tool_name": tool_name,
                "output": f"Error: {body.get('error', 'request_failed')}",
                "data": body,
            }
        return {
            "tool_name": tool_name,
            "output": "ok",
            "data": result,
        }

    if tool_name == "search_docs":
        skill_id = args.get("skill_id")
        query = args.get("query")
        top_k = args.get("top_k", 5)
        if not isinstance(skill_id, str) or not isinstance(query, str):
            return {
                "tool_name": tool_name,
                "output": "Error: missing required args 'skill_id' and/or 'query'",
                "data": {},
            }
        if not isinstance(top_k, int):
            top_k = 5
        result = await search_docs(
            SearchDocsRequest(skill_id=skill_id, query=query, top_k=top_k)
        )
        if isinstance(result, JSONResponse):
            body = _json_response_to_dict(result)
            return {
                "tool_name": tool_name,
                "output": f"Error: {body.get('error', 'request_failed')}",
                "data": body,
            }
        return {
            "tool_name": tool_name,
            "output": "ok",
            "data": result,
        }

    if tool_name == "list_skills":
        result = await list_skills()
        return {
            "tool_name": tool_name,
            "output": "ok",
            "data": result,
        }

    return {
        "tool_name": tool_name,
        "output": (
            "Error: deprecated or unknown tool. Use direct Actions "
            "`list_skills`, `get_skill`, `get_skill_file`, `search_docs`."
        ),
        "data": {
            "supported_tools": [
                "list_skills",
                "get_skill",
                "get_skill_file",
                "search_docs",
            ]
        },
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
