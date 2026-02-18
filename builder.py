from __future__ import annotations

import re
import shutil
import zlib
from dataclasses import dataclass, field
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DOCS_DIR = ROOT_DIR / "docs"
SKILLS_DIR = ROOT_DIR / "skills"

ALLOWED_DOC_EXTENSIONS = {".md", ".txt", ".pdf"}

CAT_VOICE = "voice/tone"
CAT_MESSAGING = "messaging/value props"
CAT_POSITIONING = "positioning"
CAT_VISUAL = "visual identity"
CAT_EXAMPLES = "examples"
CAT_GLOSSARY = "glossary/terminology"
CAT_LEGAL = "legal/compliance"

ALL_CATEGORIES = [
    CAT_VOICE,
    CAT_MESSAGING,
    CAT_POSITIONING,
    CAT_VISUAL,
    CAT_EXAMPLES,
    CAT_GLOSSARY,
    CAT_LEGAL,
]

CATEGORY_KEYWORDS = {
    CAT_VOICE: [
        "voice",
        "tone",
        "style",
        "writing style",
        "brand voice",
        "tone of voice",
        "dos and don'ts",
    ],
    CAT_MESSAGING: [
        "messaging",
        "value prop",
        "value proposition",
        "benefit",
        "brand equity",
        "equity",
        "claim",
        "proof point",
        "audience",
    ],
    CAT_POSITIONING: [
        "positioning",
        "position",
        "category",
        "competitive",
        "differentiator",
        "differentiation",
        "salience",
        "blue ocean",
        "market",
    ],
    CAT_VISUAL: [
        "visual",
        "brand identity",
        "logo",
        "color",
        "typography",
        "design system",
    ],
    CAT_EXAMPLES: [
        "example",
        "sample",
        "template",
        "headline",
        "tagline",
        "cta",
        "subject line",
    ],
    CAT_GLOSSARY: [
        "glossary",
        "terminology",
        "term",
        "naming",
        "capitalize",
        "capitalization",
        "word list",
    ],
    CAT_LEGAL: [
        "legal",
        "compliance",
        "regulatory",
        "disclaimer",
        "privacy",
        "gdpr",
        "hipaa",
        "copyright",
        "trademark",
        "forbidden",
        "prohibited",
    ],
}

SKILL_CATEGORY_TARGETS = {
    "branding": set(ALL_CATEGORIES),
    "brand-copy": {
        CAT_VOICE,
        CAT_MESSAGING,
        CAT_POSITIONING,
        CAT_VISUAL,
        CAT_EXAMPLES,
    },
    "brand-review": set(ALL_CATEGORIES),
    "messaging": {CAT_MESSAGING, CAT_POSITIONING},
    "glossary-enforcer": {CAT_GLOSSARY},
}

SKILL_META = {
    "branding": {
        "name": "Branding",
        "group": "branding",
        "subcategory": "umbrella",
        "description": "Umbrella brand skill for writing, reviewing, and terminology checks using available docs.",
        "triggers": [
            "write brand copy",
            "review this copy for brand fit",
            "align this message to our voice",
            "check if this claim is allowed",
            "create a headline and CTA",
            "improve tone consistency",
            "enforce approved terms",
        ],
    },
    "brand-copy": {
        "name": "Brand Copy",
        "group": "branding",
        "subcategory": "copy",
        "description": "Create new copy aligned with documented voice, messaging, and examples.",
        "triggers": [
            "write landing page copy",
            "draft email copy",
            "generate ad copy",
            "rewrite in brand voice",
            "create homepage headline",
            "write product value prop",
            "craft CTA variants",
        ],
    },
    "brand-review": {
        "name": "Brand Review",
        "group": "branding",
        "subcategory": "review",
        "description": "Review draft copy against tone, messaging, terminology, and compliance constraints.",
        "triggers": [
            "review this copy",
            "QA this message",
            "find policy issues",
            "check terminology compliance",
            "audit tone consistency",
            "validate claims",
            "flag risky phrasing",
        ],
    },
    "messaging": {
        "name": "Messaging",
        "group": "branding",
        "subcategory": "messaging",
        "description": "Shape positioning and value proposition messaging from source documentation.",
        "triggers": [
            "create positioning statement",
            "summarize value props",
            "build message hierarchy",
            "compare messaging options",
            "write audience-specific messaging",
            "draft proof-point bullets",
        ],
    },
    "glossary-enforcer": {
        "name": "Glossary Enforcer",
        "group": "branding",
        "subcategory": "glossary",
        "description": "Enforce preferred terminology and flag forbidden terms in outputs.",
        "triggers": [
            "enforce terminology",
            "find forbidden words",
            "normalize naming",
            "apply glossary rules",
            "fix capitalization rules",
            "check term consistency",
        ],
    },
}


@dataclass
class DocRecord:
    src_path: Path
    rel_path: Path
    extension: str
    text: str
    categories: set[str] = field(default_factory=set)


def ensure_input_output_dirs() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)


def reset_skills_output() -> None:
    if not SKILLS_DIR.exists():
        SKILLS_DIR.mkdir(parents=True, exist_ok=True)
        return
    for child in SKILLS_DIR.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def read_text_file(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="ignore")


def decode_pdf_escaped_string(value: str) -> str:
    result: list[str] = []
    i = 0
    while i < len(value):
        ch = value[i]
        if ch != "\\":
            result.append(ch)
            i += 1
            continue
        i += 1
        if i >= len(value):
            break
        esc = value[i]
        if esc in ("\\", "(", ")"):
            result.append(esc)
            i += 1
            continue
        if esc == "n":
            result.append("\n")
            i += 1
            continue
        if esc == "r":
            result.append("\r")
            i += 1
            continue
        if esc == "t":
            result.append("\t")
            i += 1
            continue
        if esc == "b":
            result.append("\b")
            i += 1
            continue
        if esc == "f":
            result.append("\f")
            i += 1
            continue
        if esc.isdigit():
            octal = esc
            i += 1
            for _ in range(2):
                if i < len(value) and value[i].isdigit():
                    octal += value[i]
                    i += 1
                else:
                    break
            try:
                result.append(chr(int(octal, 8)))
            except Exception:
                pass
            continue
        result.append(esc)
        i += 1
    return "".join(result)


def sanitize_line(raw: str) -> str:
    line = "".join(ch for ch in raw if ch.isprintable())
    line = re.sub(r"\s+", " ", line).strip()
    return line


def is_likely_pdf_metadata(line: str) -> bool:
    return bool(
        re.search(
            r"(author\(|creator\(|flatedecode|pdfdocencoding|xobject|procset|structparents|viewerpreferences|linearized|type\s*/|metadata|fontname|basefont|baseencoding|registry\(|supplement|ordering\(|xmp core|rdf:description|rdf:|xmlns:|adobe:ns:meta|x:xmptk|ascent|capheight|fontbbox|descent|charset|cidsysteminfo|acrobat distiller|mailto:)",
            line,
            flags=re.IGNORECASE,
        )
    )


def is_meaningful_line(raw: str) -> bool:
    line = sanitize_line(raw)
    if len(line) < 18:
        return False
    if re.fullmatch(r"[0-9A-Fa-f]{12,}", line):
        return False
    if "/" in line and "http" not in line.lower():
        return False
    if line.count("/") >= 3:
        return False
    if is_likely_pdf_metadata(line):
        return False
    if re.search(
        r"(flatedecode|pdfdocencoding|xobject|procset|structparents|viewerpreferences|linearized|type/catalog|metadata\s+\d)",
        line,
        flags=re.IGNORECASE,
    ):
        return False
    visible = re.sub(r"\s+", "", line)
    if not visible:
        return False
    letters = sum(1 for ch in visible if ch.isalpha())
    digits = sum(1 for ch in visible if ch.isdigit())
    if letters < 6:
        return False
    if digits > letters * 1.5:
        return False
    ascii_chars = sum(1 for ch in line if ord(ch) < 128)
    if ascii_chars / max(1, len(line)) < 0.9:
        return False
    allowed_chars = sum(
        1
        for ch in line
        if ch.isalnum() or ch.isspace() or ch in ".,;:'\"!?()-/&%+"
    )
    if allowed_chars / max(1, len(line)) < 0.85:
        return False
    if len(re.findall(r"[A-Za-z]{3,}", line)) < 3:
        return False
    return True


def extract_pdf_text_fragments_from_blob(blob: bytes) -> list[str]:
    decoded = blob.decode("latin-1", errors="ignore")
    fragments: list[str] = []

    for match in re.finditer(r"\(((?:\\.|[^\\)])*)\)\s*Tj", decoded):
        text = decode_pdf_escaped_string(match.group(1))
        text = sanitize_line(text)
        if is_meaningful_line(text):
            fragments.append(text)

    for match in re.finditer(r"\[(.*?)\]\s*TJ", decoded, flags=re.DOTALL):
        array_blob = match.group(1)
        for text_match in re.finditer(r"\(((?:\\.|[^\\)])*)\)", array_blob):
            text = decode_pdf_escaped_string(text_match.group(1))
            text = sanitize_line(text)
            if is_meaningful_line(text):
                fragments.append(text)

    for match in re.finditer(r"\(((?:\\.|[^\\)])*)\)\s*['\"]", decoded):
        text = decode_pdf_escaped_string(match.group(1))
        text = sanitize_line(text)
        if is_meaningful_line(text):
            fragments.append(text)

    # Fallback for PDFs where text operators are hard to parse.
    if not fragments:
        for match in re.finditer(r"[A-Za-z][A-Za-z0-9 ,.;:()'\"/&+\-]{20,}", decoded):
            text = sanitize_line(match.group(0))
            if is_meaningful_line(text):
                fragments.append(text)

    return fragments


def extract_pdf_text_best_effort(path: Path) -> str:
    data = path.read_bytes()
    blobs: list[bytes] = [data]

    stream_re = re.compile(rb"stream\r?\n(.*?)\r?\nendstream", flags=re.DOTALL)
    for match in stream_re.finditer(data):
        raw_stream = match.group(1)
        blobs.append(raw_stream)
        for wbits in (zlib.MAX_WBITS, -zlib.MAX_WBITS):
            try:
                decompressed = zlib.decompress(raw_stream, wbits=wbits)
                blobs.append(decompressed)
                break
            except Exception:
                continue

    fragments: list[str] = []
    for blob in blobs:
        fragments.extend(extract_pdf_text_fragments_from_blob(blob))
        if len(fragments) >= 250:
            break

    cleaned = unique_keep_order([frag for frag in fragments if is_meaningful_line(frag)])
    return "\n".join(cleaned[:120])[:12000]


def classify_doc(rel_path: Path, text: str) -> set[str]:
    haystack = f"{rel_path.as_posix()}\n{text[:5000]}".lower()
    categories: set[str] = set()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in haystack for keyword in keywords):
            categories.add(category)
    return categories


def discover_docs() -> list[DocRecord]:
    records: list[DocRecord] = []
    for path in sorted(DOCS_DIR.rglob("*")):
        if not path.is_file():
            continue
        extension = path.suffix.lower()
        if extension not in ALLOWED_DOC_EXTENSIONS:
            continue

        if extension in {".md", ".txt"}:
            text = read_text_file(path)
        else:
            text = extract_pdf_text_best_effort(path)

        rel_path = path.relative_to(DOCS_DIR)
        categories = classify_doc(rel_path, text)
        records.append(
            DocRecord(
                src_path=path,
                rel_path=rel_path,
                extension=extension,
                text=text,
                categories=categories,
            )
        )

    return records


def decide_skill_ids(docs: list[DocRecord]) -> list[str]:
    distinct_categories = {cat for doc in docs for cat in doc.categories}
    if len(docs) < 5 or len(distinct_categories) < 3:
        return ["branding"]

    has_messaging = any(CAT_MESSAGING in doc.categories for doc in docs)
    has_positioning = any(CAT_POSITIONING in doc.categories for doc in docs)
    has_glossary = any(CAT_GLOSSARY in doc.categories for doc in docs)
    has_legal = any(CAT_LEGAL in doc.categories for doc in docs)

    skill_ids = ["brand-copy"]
    if has_positioning or sum(1 for doc in docs if CAT_MESSAGING in doc.categories) >= 2:
        skill_ids.append("messaging")
    if has_glossary:
        skill_ids.append("glossary-enforcer")
    if has_legal or has_glossary:
        skill_ids.append("brand-review")

    # Keep deterministic order and max 4.
    ordered = ["brand-copy", "brand-review", "messaging", "glossary-enforcer"]
    return [sid for sid in ordered if sid in skill_ids][:4]


def map_docs_to_skills(skill_ids: list[str], docs: list[DocRecord]) -> dict[str, list[DocRecord]]:
    mapping: dict[str, list[DocRecord]] = {skill_id: [] for skill_id in skill_ids}
    if not skill_ids:
        return mapping
    if skill_ids == ["branding"]:
        mapping["branding"] = list(docs)
        return mapping

    assigned: dict[str, set[str]] = {}

    for skill_id in skill_ids:
        target_categories = SKILL_CATEGORY_TARGETS[skill_id]
        for doc in docs:
            doc_key = doc.rel_path.as_posix()
            if doc.categories & target_categories:
                mapping[skill_id].append(doc)
                assigned.setdefault(doc_key, set()).add(skill_id)

    # Ensure every doc is mapped to at least one skill.
    default_skill = "brand-copy" if "brand-copy" in mapping else skill_ids[0]
    for doc in docs:
        doc_key = doc.rel_path.as_posix()
        if doc_key not in assigned:
            mapping[default_skill].append(doc)

    # Deduplicate while preserving order.
    for skill_id in skill_ids:
        deduped: list[DocRecord] = []
        seen: set[str] = set()
        for doc in mapping[skill_id]:
            key = doc.rel_path.as_posix()
            if key in seen:
                continue
            seen.add(key)
            deduped.append(doc)
        mapping[skill_id] = deduped

    # Remove empty non-primary skills for a cleaner grouping.
    primary = skill_ids[0]
    cleaned = {primary: mapping[primary]}
    for skill_id in skill_ids[1:]:
        if mapping[skill_id]:
            cleaned[skill_id] = mapping[skill_id]
    return cleaned


def safe_source_name(rel_path: Path) -> str:
    source_name = rel_path.as_posix().replace("/", "__")
    source_name = re.sub(r"[^A-Za-z0-9._-]", "_", source_name)
    return source_name


def copy_source_docs(skill_dir: Path, docs: list[DocRecord]) -> dict[str, str]:
    source_dir = skill_dir / "references" / "source"
    source_dir.mkdir(parents=True, exist_ok=True)

    source_map: dict[str, str] = {}
    used_names: set[str] = set()
    for doc in docs:
        rel_key = doc.rel_path.as_posix()
        base_name = safe_source_name(doc.rel_path)
        name = base_name
        stem = Path(base_name).stem
        suffix = Path(base_name).suffix
        counter = 2
        while name in used_names:
            name = f"{stem}_{counter}{suffix}"
            counter += 1
        used_names.add(name)
        source_map[rel_key] = name
        shutil.copy2(doc.src_path, source_dir / name)
        if doc.extension == ".pdf":
            extract_path = source_dir / f"{name}.extract.txt"
            lines = candidate_lines(doc.text)
            if lines:
                extract_body = "\n".join(lines[:120])
            else:
                extract_body = "No extractable quote."
            extract_path.write_text(
                (
                    f"# Extracted Text: {name}\n\n"
                    f"Original doc: docs/{rel_key}\n\n"
                    f"{extract_body}\n"
                ),
                encoding="utf-8",
            )
    return source_map


def candidate_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("```"):
            continue
        line = line.lstrip("#").strip()
        line = sanitize_line(line)
        if len(line) < 18:
            continue
        if not is_meaningful_line(line):
            continue
        if len(line) > 220:
            line = f"{line[:220].rstrip()}..."
        lines.append(line)
    return lines


def unique_keep_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        deduped.append(value)
    return deduped


def collect_evidence(
    docs: list[DocRecord],
    source_map: dict[str, str],
    categories: set[str] | None,
    keywords: list[str] | None,
    limit: int = 6,
) -> list[str]:
    evidence: list[str] = []
    normalized_keywords = [k.lower() for k in (keywords or [])]

    for doc in docs:
        rel_key = doc.rel_path.as_posix()
        if categories is not None and not (doc.categories & categories):
            continue

        lines = candidate_lines(doc.text)
        selected: list[str] = []
        if lines and normalized_keywords:
            for line in lines:
                lower_line = line.lower()
                if any(keyword in lower_line for keyword in normalized_keywords):
                    selected.append(line)
                if len(selected) >= 2:
                    break
        if not selected and lines:
            selected = lines[:1]

        if not selected and doc.extension == ".pdf":
            selected = ["Document present; extractable text was limited."]

        for line in selected:
            source_name = source_map.get(rel_key, safe_source_name(doc.rel_path))
            evidence.append(
                f'- "{line}" (from: docs/{rel_key}; source: source/{source_name})'
            )
            if len(evidence) >= limit:
                return unique_keep_order(evidence)

    return unique_keep_order(evidence)


def render_section(title: str, bullets: list[str]) -> str:
    if not bullets:
        return f"## {title}\nNot specified in docs.\n"
    return f"## {title}\n" + "\n".join(bullets) + "\n"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def render_voice_md(docs: list[DocRecord], source_map: dict[str, str]) -> str:
    tone = collect_evidence(
        docs,
        source_map,
        {CAT_VOICE, CAT_MESSAGING, CAT_EXAMPLES},
        ["tone", "voice", "style", "clear", "friendly", "professional", "confident"],
    )
    dos = collect_evidence(
        docs,
        source_map,
        {CAT_VOICE, CAT_MESSAGING, CAT_GLOSSARY, CAT_LEGAL},
        ["must", "should", "prefer", "use", "always"],
    )
    donts = collect_evidence(
        docs,
        source_map,
        {CAT_VOICE, CAT_MESSAGING, CAT_GLOSSARY, CAT_LEGAL},
        ["avoid", "never", "don't", "do not", "forbidden", "prohibited"],
    )
    patterns = collect_evidence(
        docs,
        source_map,
        {CAT_EXAMPLES, CAT_VOICE, CAT_MESSAGING},
        ["example", "template", "pattern", "headline", "cta", "subject"],
    )
    return (
        "# VOICE\n\n"
        + render_section("Tone", tone)
        + "\n"
        + render_section("Do", dos)
        + "\n"
        + render_section("Don't", donts)
        + "\n"
        + render_section("Patterns", patterns)
    )


def render_messaging_md(docs: list[DocRecord], source_map: dict[str, str]) -> str:
    audience = collect_evidence(
        docs,
        source_map,
        {CAT_MESSAGING, CAT_POSITIONING},
        ["audience", "customer", "user", "buyer", "segment", "persona"],
    )
    value_props = collect_evidence(
        docs,
        source_map,
        {CAT_MESSAGING, CAT_POSITIONING},
        ["value", "benefit", "outcome", "save", "faster", "roi", "advantage"],
    )
    claims = collect_evidence(
        docs,
        source_map,
        {CAT_MESSAGING, CAT_POSITIONING, CAT_LEGAL},
        ["claim", "proof", "metric", "result", "evidence", "promise"],
    )
    return (
        "# MESSAGING\n\n"
        + render_section("Audience", audience)
        + "\n"
        + render_section("Value Propositions", value_props)
        + "\n"
        + render_section("Claims", claims)
    )


def render_glossary_md(docs: list[DocRecord], source_map: dict[str, str]) -> str:
    preferred_terms = collect_evidence(
        docs,
        source_map,
        {CAT_GLOSSARY, CAT_VOICE},
        ["prefer", "use", "term", "naming", "capitalize", "capitalization"],
    )
    forbidden_terms = collect_evidence(
        docs,
        source_map,
        {CAT_GLOSSARY, CAT_LEGAL},
        ["avoid", "forbidden", "never", "do not", "don't", "prohibited"],
    )
    definitions = collect_evidence(
        docs,
        source_map,
        {CAT_GLOSSARY},
        ["means", "definition", "defined", "refers to", "is the"],
    )
    return (
        "# GLOSSARY\n\n"
        + render_section("Preferred Terms", preferred_terms)
        + "\n"
        + render_section("Forbidden Terms", forbidden_terms)
        + "\n"
        + render_section("Definitions", definitions)
    )


def render_examples_md(docs: list[DocRecord], source_map: dict[str, str]) -> str:
    snippets = collect_evidence(
        docs,
        source_map,
        {CAT_EXAMPLES, CAT_VOICE, CAT_MESSAGING},
        ["example", "sample", "headline", "cta", "subject", "copy"],
    )
    structures = collect_evidence(
        docs,
        source_map,
        {CAT_EXAMPLES, CAT_MESSAGING, CAT_POSITIONING},
        ["pattern", "template", "format", "structure", "framework"],
    )
    return (
        "# EXAMPLES\n\n"
        + render_section("Approved Snippets", snippets)
        + "\n"
        + render_section("Patterns", structures)
    )


def render_constraints_md(docs: list[DocRecord], source_map: dict[str, str]) -> str:
    legal_rules = collect_evidence(
        docs,
        source_map,
        {CAT_LEGAL, CAT_MESSAGING},
        ["legal", "compliance", "must", "cannot", "can't", "required", "prohibited"],
    )
    prohibited_claims = collect_evidence(
        docs,
        source_map,
        {CAT_LEGAL, CAT_MESSAGING},
        ["forbidden", "prohibited", "never", "avoid", "do not", "don't", "claim"],
    )
    disclaimers = collect_evidence(
        docs,
        source_map,
        {CAT_LEGAL},
        ["disclaimer", "privacy", "terms", "policy", "consent"],
    )
    return (
        "# CONSTRAINTS\n\n"
        + render_section("Legal and Compliance Constraints", legal_rules)
        + "\n"
        + render_section("Prohibited Claims", prohibited_claims)
        + "\n"
        + render_section("Required Disclaimers", disclaimers)
    )


def infer_topic_from_filename(rel_path: Path) -> str:
    stem = rel_path.stem
    words = re.findall(r"[A-Za-z0-9]+", stem)
    if not words:
        return "Not specified in docs."
    return " ".join(words).strip()


def render_pdf_summaries_md(docs: list[DocRecord], source_map: dict[str, str]) -> str:
    pdf_docs = [doc for doc in docs if doc.extension == ".pdf"]
    lines = ["# PDF_SUMMARIES", ""]
    if not pdf_docs:
        lines.append("Not specified in docs.")
        return "\n".join(lines)

    lines.append(
        "Best-effort summaries from PDF filenames and extractable text only (no OCR)."
    )
    lines.append("")

    for doc in pdf_docs:
        rel_key = doc.rel_path.as_posix()
        source_name = source_map.get(rel_key, safe_source_name(doc.rel_path))
        inferred_topic = infer_topic_from_filename(doc.rel_path)
        extract_lines = candidate_lines(doc.text)
        excerpt = "No extractable quote."
        if extract_lines:
            excerpt = extract_lines[0]
        lines.extend(
            [
                f"## {source_name}",
                f"- Original doc: docs/{rel_key}",
                f"- Inferred topic: {inferred_topic} (from: docs/{rel_key}; source: source/{source_name})",
                f'- Extractable text excerpt: "{excerpt}" (from: docs/{rel_key}; source: source/{source_name})',
                "",
            ]
        )

    return "\n".join(lines).rstrip()


def render_source_quotes_md(docs: list[DocRecord], source_map: dict[str, str]) -> str:
    lines = [
        "# SOURCE_QUOTES",
        "",
        "Short quote bank from source docs for citations in final answers.",
        "",
    ]
    if not docs:
        lines.append("Not specified in docs.")
        return "\n".join(lines)

    for doc in docs:
        rel_key = doc.rel_path.as_posix()
        source_name = source_map.get(rel_key, safe_source_name(doc.rel_path))
        lines.append(f"## {source_name}")
        lines.append(f"- Original doc: docs/{rel_key}")
        extracted = candidate_lines(doc.text)
        if extracted:
            for quote in extracted[:3]:
                lines.append(
                    f'- "{quote}" (from: docs/{rel_key}; source: source/{source_name})'
                )
        else:
            lines.append(f"- No extractable quote. (from: docs/{rel_key})")
        lines.append("")

    return "\n".join(lines).rstrip()


def render_index_md(
    skill_id: str,
    docs: list[DocRecord],
    source_map: dict[str, str],
    gaps: list[str],
) -> str:
    lines = [
        "# INDEX",
        "",
        f"- skill_id: {skill_id}",
        "",
        "## Source Files",
    ]
    if docs:
        for doc in docs:
            rel = doc.rel_path.as_posix()
            source_name = source_map.get(rel, safe_source_name(doc.rel_path))
            category_str = ", ".join(sorted(doc.categories)) if doc.categories else "uncategorized"
            lines.append(f"- source/{source_name} (from: docs/{rel}; categories: {category_str})")
    else:
        lines.append("- Not specified in docs.")

    lines.extend(
        [
            "",
            "## Normalized Files",
            "- normalized/VOICE.md",
            "- normalized/MESSAGING.md",
            "- normalized/GLOSSARY.md",
            "- normalized/EXAMPLES.md",
            "- normalized/CONSTRAINTS.md",
            "- normalized/PDF_SUMMARIES.md",
            "- normalized/SOURCE_QUOTES.md",
            "",
            "## Gaps",
        ]
    )
    if gaps:
        lines.extend(f"- {gap}" for gap in gaps)
    else:
        lines.append("- None detected from available docs.")
    return "\n".join(lines)


def render_skill_md(skill_id: str) -> str:
    meta = SKILL_META[skill_id]
    verification = f"VERIFIED_SKILL:{skill_id}:v1"
    triggers = "\n".join(f"- \"{trigger}\"" for trigger in meta["triggers"])
    return f"""name: {meta["name"]}
skill_id: {skill_id}
skill_group: {meta["group"]}
skill_subcategory: {meta["subcategory"]}
description: {meta["description"]}
triggers:
{triggers}
inputs_schema:
{{
  "task_type": "write | review | messaging | terminology",
  "request": "string",
  "target_audience": "string (optional)",
  "output_format": "string (optional)"
}}
outputs_schema:
{{
  "verification": "string",
  "answer": "string",
  "compliance_checklist": ["string"],
  "sources_used": [
    {{
      "quote": "string",
      "citation": "docs/<original-file> (preferred) or source/<copied-file>",
      "lines": "start-end (optional)"
    }}
  ]
}}
required_tools:
- get_skill_file
- search_docs
- run_tool
steps:
1. Determine request mode: writing, review, messaging, or terminology.
2. Always call `get_skill_file` for `references/INDEX.md` first.
3. If `get_skill_file` or `search_docs` are unavailable in the session, use `run_tool` fallback:
   - `run_tool` with `tool_name="get_skill_file"` and `args={{"skill_id":"{skill_id}","path":"references/INDEX.md"}}`
   - `run_tool` with `tool_name="search_docs"` and `args={{"skill_id":"{skill_id}","query":"<keywords>","top_k":5}}`
4. Read the minimum needed normalized files:
   - writing: `references/normalized/VOICE.md`, `references/normalized/MESSAGING.md`, `references/normalized/GLOSSARY.md`, `references/normalized/EXAMPLES.md`
   - review: `references/normalized/VOICE.md`, `references/normalized/MESSAGING.md`, `references/normalized/GLOSSARY.md`, `references/normalized/CONSTRAINTS.md`
   - messaging: `references/normalized/MESSAGING.md`, `references/normalized/EXAMPLES.md`, `references/normalized/CONSTRAINTS.md`
   - terminology: `references/normalized/GLOSSARY.md`
5. If source PDFs are relevant, read `references/normalized/PDF_SUMMARIES.md` before drafting.
6. If a needed detail is missing, call `search_docs` (or `run_tool` fallback) with focused keywords and use only returned hits.
7. For each important claim, include evidence with this format in `Sources Used`: `"<short quote>" (from: docs/<original-file>, lines: <start-end if known>)`.
8. If quote text is unavailable (for scanned/opaque PDFs), cite file path and state "No extractable quote."
9. Produce the answer and include a section titled exactly `Compliance Checklist`.
10. Final answer MUST start with the verification string exactly.

Compliance Checklist:
- Voice and tone are validated against loaded voice references.
- Messaging and claims are validated against loaded messaging references.
- Terminology is validated against loaded glossary references.
- Example style is validated against loaded example references.
- Legal and compliance constraints are validated against loaded constraint references.
- Any missing rule is explicitly marked as "Not specified in docs."
- Sources include short evidence quotes with citations, not only bare file paths.
- Prefer citations using original document names from `docs/...` and quote bank in `references/normalized/SOURCE_QUOTES.md`.

VERIFICATION STRING: {verification}
Final answer must start with: {verification}
"""


def render_assets_template() -> str:
    return """# REVIEW_CHECKLIST_TEMPLATE

- Voice check: Pass | Fail
- Messaging check: Pass | Fail
- Terminology check: Pass | Fail
- Example style check: Pass | Fail
- Compliance constraints check: Pass | Fail
- Open issues:
  - Not specified in docs.
"""


def build_skill(skill_id: str, docs: list[DocRecord], global_gaps: list[str]) -> None:
    skill_dir = SKILLS_DIR / skill_id
    references_dir = skill_dir / "references"
    normalized_dir = references_dir / "normalized"
    assets_dir = skill_dir / "assets"

    normalized_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)

    source_map = copy_source_docs(skill_dir, docs)
    write_text(skill_dir / "SKILL.md", render_skill_md(skill_id))
    write_text(
        references_dir / "INDEX.md",
        render_index_md(skill_id, docs, source_map, global_gaps),
    )
    write_text(normalized_dir / "VOICE.md", render_voice_md(docs, source_map))
    write_text(normalized_dir / "MESSAGING.md", render_messaging_md(docs, source_map))
    write_text(normalized_dir / "GLOSSARY.md", render_glossary_md(docs, source_map))
    write_text(normalized_dir / "EXAMPLES.md", render_examples_md(docs, source_map))
    write_text(normalized_dir / "CONSTRAINTS.md", render_constraints_md(docs, source_map))
    write_text(normalized_dir / "PDF_SUMMARIES.md", render_pdf_summaries_md(docs, source_map))
    write_text(normalized_dir / "SOURCE_QUOTES.md", render_source_quotes_md(docs, source_map))
    write_text(assets_dir / "REVIEW_CHECKLIST_TEMPLATE.md", render_assets_template())


def compute_gaps(docs: list[DocRecord]) -> list[str]:
    gaps: list[str] = []
    if not docs:
        gaps.append("No docs found under ./docs. Generated scaffold files only.")
        return gaps

    covered = {cat for doc in docs for cat in doc.categories}
    for category in ALL_CATEGORIES:
        if category not in covered:
            gaps.append(f"No explicit documentation found for category: {category}.")

    for doc in docs:
        if not doc.categories:
            gaps.append(f"Could not confidently categorize: docs/{doc.rel_path.as_posix()}.")
        if doc.extension == ".pdf" and not doc.text.strip():
            gaps.append(
                f"Limited extractable text in PDF (no OCR used): docs/{doc.rel_path.as_posix()}."
            )
    return gaps


def print_build_summary(
    skills_to_docs: dict[str, list[DocRecord]],
    gaps: list[str],
) -> None:
    print("Build summary")
    print("=============")
    print("skills created:")
    for skill_id in skills_to_docs:
        print(f"- {skill_id}")

    print("")
    print("docs mapped to each skill:")
    for skill_id, docs in skills_to_docs.items():
        print(f"- {skill_id}:")
        if docs:
            for doc in docs:
                print(f"  - docs/{doc.rel_path.as_posix()}")
        else:
            print("  - (none)")

    print("")
    print("gaps/unknowns:")
    if gaps:
        for gap in gaps:
            print(f"- {gap}")
    else:
        print("- none")


def main() -> None:
    ensure_input_output_dirs()
    docs = discover_docs()
    skill_ids = decide_skill_ids(docs)
    skills_to_docs = map_docs_to_skills(skill_ids, docs)
    gaps = compute_gaps(docs)

    reset_skills_output()
    for skill_id, mapped_docs in skills_to_docs.items():
        build_skill(skill_id, mapped_docs, gaps)

    print_build_summary(skills_to_docs, gaps)


if __name__ == "__main__":
    main()
