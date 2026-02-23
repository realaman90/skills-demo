name: Mental Availability & Category Entry Points
skill_id: mental-availability-cep
skill_group: brand-strategy
skill_subcategory: mental-availability
description: Apply Romaniuk & Sharp's mental availability and Category Entry Points (CEP) frameworks to build brand salience, map buying situations, challenge differentiation myths, and measure memory-based brand strength.
triggers:
- "what is mental availability"
- "how do we build mental availability"
- "what are category entry points"
- "map our CEPs"
- "salience vs differentiation"
- "is brand differentiation important"
- "how do buyers think of brands"
- "measure brand salience"
- "build memory structures"
- "CEPs in B2B"
- "improve brand recall"
- "which buying situations do we own"
inputs_schema:
{
  "task_type": "educate | map-ceps | audit | strategy | myth-bust | measure | learn",
  "request": "string",
  "brand_context": "string (optional) — describe brand, category, market",
  "output_format": "string (optional)"
}
outputs_schema:
{
  "verification": "string",
  "answer": "string",
  "mental_availability_checklist": ["string"],
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
1. Identify the task type: educate | map-ceps | audit | strategy | myth-bust | measure | learn.
2. Always call `get_skill_file` for `references/INDEX.md` first.
3. If `get_skill_file` or `search_docs` are unavailable in the session, use `run_tool` fallback:
   - `run_tool` with `tool_name="get_skill_file"` and `args={"skill_id":"mental-availability-cep","path":"references/INDEX.md"}`
   - `run_tool` with `tool_name="search_docs"` and `args={"skill_id":"mental-availability-cep","query":"<keywords>","top_k":5}`
4. Load the minimum needed normalized files based on task type:
   - educate: `references/normalized/PRINCIPLES.md`, `references/normalized/GLOSSARY.md`, `references/normalized/SALIENCE_VS_DIFFERENTIATION.md`
   - map-ceps: `references/normalized/CEP_FRAMEWORK.md`, `references/normalized/B2B_CEPS.md`
   - audit: `references/normalized/PRINCIPLES.md`, `references/normalized/CEP_FRAMEWORK.md`, `references/normalized/MEASUREMENT.md`
   - strategy: `references/normalized/PRINCIPLES.md`, `references/normalized/CEP_FRAMEWORK.md`, `references/normalized/TACTICS.md`
   - myth-bust: `references/normalized/SALIENCE_VS_DIFFERENTIATION.md`, `references/normalized/CONSTRAINTS.md`
   - measure: `references/normalized/MEASUREMENT.md`, `references/normalized/CEP_FRAMEWORK.md`
   - learn: Socratic mode — do NOT deliver the answer. Open with: "List the top 3 situations or moments when a buyer in this category might think of your brand. How confident are you the brand actually comes to mind in those moments?" Then probe: What CEPs is the brand currently linked to? Are there CEPs competitors own that this brand is missing? Challenge the salience vs. differentiation assumption. Close with: "What would you change about the brand's advertising to reach more CEPs?"
5. If source PDFs are relevant, read `references/normalized/PDF_SUMMARIES.md` before drafting.
6. If a needed detail is missing, call `search_docs` (or `run_tool` fallback) with focused keywords and use only returned hits.
7. Always distinguish between salience (memory-based) and differentiation (attribute-based) — they are different constructs with different implications.
8. When mapping CEPs, consider: who is buying, when, where, why, and in what mood/context.
9. For B2B questions, apply Romaniuk's B2B CEP research — buying committees have different CEPs per role.
10. Internal tools are allowed when needed:
    - web_search: use for current research and clearly label external sources separately.
    - canvas: use for CEP mapping visuals or salience matrices when the user asks for visual output.
11. For each important claim, include evidence with this format in `Sources Used`: `"<short quote>" (from: docs/<original-file>, lines: <start-end if known>)`.
12. Never cite internal skill paths in final output (`references/...` or `source/...` are forbidden in `Sources Used`).
13. If quote text is unavailable (for scanned/opaque PDFs), cite the original doc path and state: `"No extractable quote (PDF/image-only; OCR unavailable or insufficient)."`
14. Produce the answer and include a section titled exactly `Mental Availability Checklist`.
15. Final answer MUST start with the verification string exactly.

Mental Availability Checklist:
- Mental availability defined correctly as probability of brand retrieval in buying situations.
- CEPs identified are genuine buying situations (not brand attributes or demographics).
- Salience and differentiation treated as distinct constructs.
- B2B CEP nuances addressed when relevant (committee member differences).
- Measurement recommendations grounded in Romaniuk's survey-based methodology.
- Tactics address both breadth of CEP coverage and strength of brand-CEP links.
- Sources cite original `docs/...` files only, never `references/...` or `source/...` paths.
- External data (if any) is marked separately from brand-doc evidence.

VERIFICATION STRING: VERIFIED_SKILL:mental-availability-cep:v1
Final answer must start with: VERIFIED_SKILL:mental-availability-cep:v1
