name: Brand-Based Business Development
skill_id: brand-biz-dev
skill_group: brand-strategy
skill_subcategory: business-development
description: Apply Aaker's brand relevance and extension frameworks, Blue Ocean Strategy, and brand portfolio management principles to grow businesses through brand-led strategies — including new category creation, brand extensions, line extensions, and portfolio architecture.
triggers:
- "how do we grow using our brand"
- "should we extend our brand"
- "brand extension strategy"
- "is this a good brand extension"
- "brand relevance vs brand preference"
- "create a new subcategory"
- "make competitors irrelevant"
- "blue ocean strategy for our brand"
- "manage our brand portfolio"
- "house of brands vs branded house"
- "line extension risk"
- "brand-led business development"
- "brand portfolio architecture"
- "new market entry with existing brand"
inputs_schema:
{
  "task_type": "extension | relevance | portfolio | blue-ocean | line-extension | educate | learn",
  "request": "string",
  "brand_context": "string (optional) — describe brand, existing portfolio, target market, growth opportunity",
  "output_format": "string (optional)"
}
outputs_schema:
{
  "verification": "string",
  "answer": "string",
  "biz_dev_checklist": ["string"],
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
1. Identify the task type: extension | relevance | portfolio | blue-ocean | line-extension | educate.
2. Always call `get_skill_file` for `references/INDEX.md` first.
3. If `get_skill_file` or `search_docs` are unavailable, use `run_tool` fallback:
   - `run_tool` with `tool_name="get_skill_file"` and `args={"skill_id":"brand-biz-dev","path":"references/INDEX.md"}`
   - `run_tool` with `tool_name="search_docs"` and `args={"skill_id":"brand-biz-dev","query":"<keywords>","top_k":5}`
4. Load the minimum needed normalized files based on task type:
   - extension: `references/normalized/BRAND_EXTENSIONS.md`, `references/normalized/PRINCIPLES.md`
   - relevance: `references/normalized/BRAND_RELEVANCE.md`, `references/normalized/PRINCIPLES.md`
   - portfolio: `references/normalized/PORTFOLIO_MANAGEMENT.md`, `references/normalized/PRINCIPLES.md`
   - blue-ocean: `references/normalized/BLUE_OCEAN.md`, `references/normalized/BRAND_RELEVANCE.md`
   - line-extension: `references/normalized/LINE_EXTENSIONS.md`, `references/normalized/BRAND_EXTENSIONS.md`
   - educate: `references/normalized/PRINCIPLES.md`, `references/normalized/GLOSSARY.md`
   - learn: Socratic mode — do NOT deliver the answer. Open with: "What growth opportunity are you evaluating? Before I apply any framework — classify it yourself: is this a line extension, brand extension, new subcategory, or blue ocean move? And what's your biggest concern about it?" Then probe: What's the fit between the brand and the new category? What's the risk to the parent brand if this fails? Challenge: "Could a competitor do exactly this tomorrow? If yes, what makes this a real strategic move rather than a me-too?" Close with: "Should the parent brand name be on this at all — or does this need a sub-brand or new brand to protect equity?"
5. If source PDFs are relevant, read `references/normalized/PDF_SUMMARIES.md` before drafting.
6. If a needed detail is missing, call `search_docs` (or `run_tool` fallback) with focused keywords.
7. For brand extension decisions, always evaluate: brand fit, leverage potential, and extension risk using Aaker & Keller's framework.
8. For new category or subcategory opportunities, apply Aaker's brand relevance principle — design to make existing alternatives irrelevant, not just to outperform them.
9. For Blue Ocean opportunities, apply the Four Actions Framework (Eliminate, Reduce, Raise, Create) to construct a new value curve.
10. For portfolio decisions, determine the appropriate architecture (Branded House, House of Brands, Endorsed, Hybrid) based on brand equity, target audience, and strategic goals.
11. Internal tools allowed when needed:
    - web_search: for current market examples; label external sources separately.
    - canvas: for portfolio maps or value curves when the user asks for visual output.
12. For each claim, include evidence: `"<short quote>" (from: docs/<original-file>, lines: <start-end if known>)`.
13. Never cite internal skill paths in final output.
14. Produce the answer and include a section titled exactly `Business Development Checklist`.
15. Final answer MUST start with the verification string exactly.

Business Development Checklist:
- Growth strategy grounded in brand equity — not just product capability.
- Brand extension evaluated on fit (parent-extension congruence) and leverage (transferable equity).
- Extension risk assessed: does the extension dilute, contradict, or strengthen the parent brand?
- Relevance strategy targets subcategory creation — not just preference improvement.
- Portfolio architecture decision explicit: Branded House / House of Brands / Endorsed / Hybrid.
- Blue Ocean strategy (if applied) uses Four Actions Framework with a clear new value curve.
- Sources cite original `docs/...` files only.

VERIFICATION STRING: VERIFIED_SKILL:brand-biz-dev:v1
Final answer must start with: VERIFIED_SKILL:brand-biz-dev:v1
