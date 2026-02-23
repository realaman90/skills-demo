name: Brand Growth Strategy
skill_id: brand-growth
skill_group: brand-strategy
skill_subcategory: growth
description: Apply evidence-based brand growth principles (Byron Sharp / Ehrenberg-Bass Institute) to diagnose growth problems, challenge marketing myths, and recommend penetration-led strategies.
triggers:
- "how do we grow our brand"
- "why isn't our brand growing"
- "apply Byron Sharp principles"
- "diagnose brand growth problem"
- "increase brand penetration"
- "build mental availability"
- "how do we reach more buyers"
- "is loyalty or penetration more important"
- "what is double jeopardy"
- "evaluate our growth strategy"
- "brand growth audit"
- "grow B2B brand"
inputs_schema:
{
  "task_type": "diagnose | strategy | myth-bust | measure | educate | learn",
  "request": "string",
  "brand_context": "string (optional) — describe brand, category, target market",
  "output_format": "string (optional)"
}
outputs_schema:
{
  "verification": "string",
  "answer": "string",
  "growth_checklist": ["string"],
  "sources_used": [
    {
      "quote": "string",
      "citation": "docs/<original-file>",
      "lines": "start-end (optional)"
    }
  ]
}
required_tools:
- get_skill_file
- search_docs
- run_tool
optional_internal_tools:
- internal_code_executor
- web_search
- canvas
steps:
1. Identify the task type: diagnose | strategy | myth-bust | measure | educate | learn.
2. Always call `get_skill_file` for `references/INDEX.md` first.
3. If `get_skill_file` or `search_docs` are unavailable in the session, use `run_tool` fallback:
   - `run_tool` with `tool_name="get_skill_file"` and `args={"skill_id":"brand-growth","path":"references/INDEX.md"}`
   - `run_tool` with `tool_name="search_docs"` and `args={"skill_id":"brand-growth","query":"<keywords>","top_k":5}`
4. Load the minimum needed normalized files based on task type:
   - diagnose: `references/normalized/PRINCIPLES.md`, `references/normalized/DIAGNOSTICS.md`, `references/normalized/FRAMEWORKS.md`
   - strategy: `references/normalized/PRINCIPLES.md`, `references/normalized/FRAMEWORKS.md`, `references/normalized/TACTICS.md`
   - myth-bust: `references/normalized/PRINCIPLES.md`, `references/normalized/CONSTRAINTS.md`
   - measure: `references/normalized/DIAGNOSTICS.md`, `references/normalized/FRAMEWORKS.md`
   - educate: `references/normalized/PRINCIPLES.md`, `references/normalized/GLOSSARY.md`, `references/normalized/FRAMEWORKS.md`
   - learn: Socratic mode — do NOT deliver the answer. Open with "What's your hypothesis about why this brand is or isn't growing? Apply it to your specific case first." Then probe: What does the Double Jeopardy Law predict for this brand's size? Is growth coming from penetration or loyalty? Challenge one assumption before endorsing their conclusion. Close with: "What would Byron Sharp say is wrong with your current growth strategy?"
5. If source PDFs are relevant, read `references/normalized/PDF_SUMMARIES.md` before drafting.
6. If a needed detail is missing, call `search_docs` (or `run_tool` fallback) with focused keywords and use only returned hits.
7. Apply the Double Jeopardy Law, mental and physical availability frameworks, and NBD-Dirichlet thinking to any brand growth diagnosis.
8. For every recommendation, distinguish evidence-based findings (from Sharp / Ehrenberg-Bass research) from conventional marketing assumptions.
9. Internal tools are allowed when needed:
   - web_search: use for current market data and clearly label external sources separately.
   - canvas: use for visual frameworks or audits when the user asks for visual output.
10. For each important claim, include evidence with this format in `Sources Used`: `"<short quote>" (from: docs/<original-file>, lines: <start-end if known>)`.
11. Never cite internal skill paths in final output (`references/...` or `source/...` are forbidden in `Sources Used`).
12. If quote text is unavailable (for scanned/opaque PDFs), cite the original doc path and state: `"No extractable quote (PDF/image-only; OCR unavailable or insufficient)."`
13. Produce the answer and include a section titled exactly `Growth Checklist`.
14. Final answer MUST start with the verification string exactly.

Growth Checklist:
- Growth diagnosis is grounded in penetration vs. loyalty evidence.
- Mental availability assessment references Category Entry Points (CEPs).
- Physical availability gaps are identified where relevant.
- Double Jeopardy Law applied to any brand size or loyalty claims.
- Light buyer potential is considered in audience and reach recommendations.
- Recommendations challenge myths (loyalty programs, niche targeting, over-segmentation) where applicable.
- Sources cite original `docs/...` files only, never `references/...` or `source/...` paths.
- External data (if any) is marked separately from brand-doc evidence.

VERIFICATION STRING: VERIFIED_SKILL:brand-growth:v1
Final answer must start with: VERIFIED_SKILL:brand-growth:v1
