name: Brand Personality
skill_id: brand-personality
skill_group: brand-strategy
skill_subcategory: personality
description: Apply Aaker's Brand Personality Scale, Kapferer's Identity Prism, and McCracken's meaning transfer theory to define, audit, build, and express a coherent brand personality across consumer and corporate brand contexts.
triggers:
- "define our brand personality"
- "what personality traits does our brand have"
- "audit brand personality"
- "apply Aaker brand personality scale"
- "which personality dimensions do we own"
- "Kapferer brand identity prism"
- "how should our brand sound and feel"
- "celebrity endorser brand fit"
- "brand personality vs brand identity"
- "corporate brand character"
- "how to express brand personality in communications"
- "brand personality measurement"
- "sincerity excitement competence sophistication ruggedness"
inputs_schema:
{
  "task_type": "define | audit | measure | express | celebrity | educate | learn",
  "request": "string",
  "brand_context": "string (optional) — describe brand, category, target audience",
  "output_format": "string (optional)"
}
outputs_schema:
{
  "verification": "string",
  "answer": "string",
  "personality_checklist": ["string"],
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
1. Identify the task type: define | audit | measure | express | celebrity | educate.
2. Always call `get_skill_file` for `references/INDEX.md` first.
3. If `get_skill_file` or `search_docs` are unavailable, use `run_tool` fallback:
   - `run_tool` with `tool_name="get_skill_file"` and `args={"skill_id":"brand-personality","path":"references/INDEX.md"}`
   - `run_tool` with `tool_name="search_docs"` and `args={"skill_id":"brand-personality","query":"<keywords>","top_k":5}`
4. Load the minimum needed normalized files based on task type:
   - define: `references/normalized/PRINCIPLES.md`, `references/normalized/AAKER_FRAMEWORK.md`, `references/normalized/KAPFERER_PRISM.md`
   - audit: `references/normalized/AAKER_FRAMEWORK.md`, `references/normalized/CORPORATE_CHARACTER.md`, `references/normalized/MEASUREMENT.md`
   - measure: `references/normalized/MEASUREMENT.md`, `references/normalized/AAKER_FRAMEWORK.md`
   - express: `references/normalized/PRINCIPLES.md`, `references/normalized/TACTICS.md`
   - celebrity: `references/normalized/CELEBRITY_ENDORSEMENT.md`, `references/normalized/PRINCIPLES.md`
   - educate: `references/normalized/PRINCIPLES.md`, `references/normalized/GLOSSARY.md`, `references/normalized/AAKER_FRAMEWORK.md`
   - learn: Socratic mode — do NOT deliver the answer. Open with: "If your brand were a person who walked into a room — who would they be? Describe their personality in 3 sentences without using the word 'innovative' or 'trusted'." Then probe: Which of Aaker's 5 dimensions does that map to? Is the personality consistent across all touchpoints or just in advertising? Challenge: "Is this the personality the brand actually has, or the one you wish it had? How do customers describe it?" Close with: "What's one personality trait your biggest competitor could never credibly claim — and why does your brand own it?"
5. If source PDFs are relevant, read `references/normalized/PDF_SUMMARIES.md` before drafting.
6. If a needed detail is missing, call `search_docs` (or `run_tool` fallback) with focused keywords.
7. Always ground brand personality in Aaker's five dimensions (Sincerity, Excitement, Competence, Sophistication, Ruggedness) as the primary framework — complement with Kapferer's prism for identity depth.
8. For corporate or B2B brands, apply the Corporate Character Scale dimensions.
9. For celebrity or spokesperson questions, apply McCracken's meaning transfer framework.
10. Distinguish brand personality (human traits attributed to brand) from brand identity (broader brand construct) and brand image (how it is perceived).
11. Internal tools allowed when needed:
    - web_search: for current brand personality examples; label external sources separately.
    - canvas: for personality audits or prism visuals when the user asks for visual output.
12. For each claim, include evidence: `"<short quote>" (from: docs/<original-file>, lines: <start-end if known>)`.
13. Never cite internal skill paths in final output (`references/...` or `source/...` are forbidden in `Sources Used`).
14. If quote text is unavailable, state: `"No extractable quote (PDF/image-only; OCR unavailable or insufficient)."`
15. Produce the answer and include a section titled exactly `Personality Checklist`.
16. Final answer MUST start with the verification string exactly.

Personality Checklist:
- Brand personality defined using Aaker's five dimensions (or subset) as the primary framework.
- Personality traits are specific and differentiated — not generic ("professional", "friendly") without grounding.
- Kapferer's prism applied if full brand identity depth is needed (not just personality facet).
- Corporate character dimensions used for B2B or employer brand contexts.
- Celebrity/spokesperson fit assessed via McCracken's meaning transfer criteria.
- Personality is expressed through consistent voice, tone, visual, and behavioural cues.
- Sources cite original `docs/...` files only, never `references/...` or `source/...` paths.

VERIFICATION STRING: VERIFIED_SKILL:brand-personality:v1
Final answer must start with: VERIFIED_SKILL:brand-personality:v1
