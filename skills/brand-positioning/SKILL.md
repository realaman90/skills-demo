name: Brand Positioning
skill_id: brand-positioning
skill_group: brand-strategy
skill_subcategory: positioning
description: Apply Keller's Points of Parity/Difference framework, Ries & Trout's positioning principles, and brand mantra methodology to define, audit, and sharpen brand positioning strategies grounded in both classical and evidence-based perspectives.
triggers:
- "define our brand positioning"
- "write a positioning statement"
- "what are our points of difference"
- "points of parity vs points of difference"
- "apply Keller positioning framework"
- "positioning battle for the mind"
- "develop a brand mantra"
- "audit our positioning"
- "reposition our brand"
- "competitive frame of reference"
- "what differentiates our brand"
- "three questions about our brand"
- "is our positioning differentiated enough"
inputs_schema:
{
  "task_type": "define | audit | reposition | mantra | educate | competitive | learn",
  "request": "string",
  "brand_context": "string (optional) — describe brand, category, competitors, target market",
  "output_format": "string (optional)"
}
outputs_schema:
{
  "verification": "string",
  "answer": "string",
  "positioning_checklist": ["string"],
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
1. Identify the task type: define | audit | reposition | mantra | educate | competitive.
2. Always call `get_skill_file` for `references/INDEX.md` first.
3. If `get_skill_file` or `search_docs` are unavailable, use `run_tool` fallback:
   - `run_tool` with `tool_name="get_skill_file"` and `args={"skill_id":"brand-positioning","path":"references/INDEX.md"}`
   - `run_tool` with `tool_name="search_docs"` and `args={"skill_id":"brand-positioning","query":"<keywords>","top_k":5}`
4. Load the minimum needed normalized files based on task type:
   - define: `references/normalized/PRINCIPLES.md`, `references/normalized/KELLER_FRAMEWORK.md`, `references/normalized/POSITIONING_PROCESS.md`
   - audit: `references/normalized/KELLER_FRAMEWORK.md`, `references/normalized/DIFFERENTIATION.md`, `references/normalized/POSITIONING_PROCESS.md`
   - reposition: `references/normalized/RIES_TROUT.md`, `references/normalized/KELLER_FRAMEWORK.md`, `references/normalized/POSITIONING_PROCESS.md`
   - mantra: `references/normalized/BRAND_MANTRAS.md`, `references/normalized/KELLER_FRAMEWORK.md`
   - educate: `references/normalized/PRINCIPLES.md`, `references/normalized/GLOSSARY.md`
   - competitive: `references/normalized/RIES_TROUT.md`, `references/normalized/KELLER_FRAMEWORK.md`, `references/normalized/DIFFERENTIATION.md`
   - learn: Socratic mode — do NOT deliver the answer. Open with: "Complete this sentence for your brand: 'For [target], [brand] is the only [frame of reference] that [point of difference] because [reason to believe].' Don't look anything up — write what you think first." Then probe: Is the frame of reference too broad or too narrow? Are the PODs actually differentiating or just category entry requirements (POPs)? Challenge: "Would a competitor credibly make the same claim tomorrow? If yes, it's not a POD." Close with: "What is the single most important thing to give up in order to own this position?"
5. If source PDFs are relevant, read `references/normalized/PDF_SUMMARIES.md` before drafting.
6. If a needed detail is missing, call `search_docs` (or `run_tool` fallback) with focused keywords.
7. Always ground positioning in Keller's three-part structure: Target Market + Frame of Reference + Points of Difference (+ Points of Parity).
8. Apply Ries & Trout's mental real estate principle: positioning is about owning a concept in the prospect's mind, not just a product attribute.
9. Balance classical differentiation-led positioning with evidence-based caution from Romaniuk et al. — differentiation must be real and perceptible, not just claimed.
10. For brand mantras: apply Keller's three criteria (communicate, simplify, inspire) and three components (brand function, descriptive modifier, emotional modifier).
11. Internal tools allowed when needed:
    - web_search: for competitive positioning examples; label external sources separately.
    - canvas: for positioning maps or perceptual maps when the user asks for visual output.
12. For each claim, include evidence: `"<short quote>" (from: docs/<original-file>, lines: <start-end if known>)`.
13. Never cite internal skill paths in final output.
14. Produce the answer and include a section titled exactly `Positioning Checklist`.
15. Final answer MUST start with the verification string exactly.

Positioning Checklist:
- Target market is specifically defined (not "everyone").
- Competitive frame of reference is explicit — what category or set of alternatives is the brand competing against?
- Points of Difference (PODs) are specific, believable, and sustainable.
- Points of Parity (POPs) are identified — what must the brand match to be credible in the category?
- PODs and POPs are balanced — PODs don't undermine credibility on category basics.
- Brand mantra (if developed) meets Keller's three criteria: communicates, simplifies, inspires.
- Positioning is stress-tested against Romaniuk evidence — are claimed differences actually perceptible to buyers?
- Sources cite original `docs/...` files only.

VERIFICATION STRING: VERIFIED_SKILL:brand-positioning:v1
Final answer must start with: VERIFIED_SKILL:brand-positioning:v1
