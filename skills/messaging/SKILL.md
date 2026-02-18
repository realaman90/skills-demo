name: Messaging
skill_id: messaging
description: Shape positioning and value proposition messaging from source documentation.
triggers:
- "create positioning statement"
- "summarize value props"
- "build message hierarchy"
- "compare messaging options"
- "write audience-specific messaging"
- "draft proof-point bullets"
inputs_schema:
{
  "task_type": "write | review | messaging | terminology",
  "request": "string",
  "target_audience": "string (optional)",
  "output_format": "string (optional)"
}
outputs_schema:
{
  "verification": "string",
  "answer": "string",
  "compliance_checklist": ["string"],
  "sources_used": [
    {
      "quote": "string",
      "citation": "docs/<original-file> (preferred) or source/<copied-file>",
      "lines": "start-end (optional)"
    }
  ]
}
required_tools:
- get_skill_file
- search_docs
- run_tool
steps:
1. Determine request mode: writing, review, messaging, or terminology.
2. Always call `get_skill_file` for `references/INDEX.md` first.
3. If `get_skill_file` or `search_docs` are unavailable in the session, use `run_tool` fallback:
   - `run_tool` with `tool_name="get_skill_file"` and `args={"skill_id":"messaging","path":"references/INDEX.md"}`
   - `run_tool` with `tool_name="search_docs"` and `args={"skill_id":"messaging","query":"<keywords>","top_k":5}`
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

VERIFICATION STRING: VERIFIED_SKILL:messaging:v1
Final answer must start with: VERIFIED_SKILL:messaging:v1
