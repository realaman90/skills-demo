name: Jobs to Be Done
skill_id: jobs-to-be-done
skill_group: brand-strategy
skill_subcategory: customer-insight
description: Apply Christensen's Jobs-to-be-Done (JTBD) theory and Ulwick's outcome-based segmentation to identify what customers are really hiring a product to do, reframe innovation, and design better brand positioning and segmentation strategies.
triggers:
- "what job is our product hired to do"
- "apply jobs to be done"
- "JTBD analysis"
- "why do customers really buy from us"
- "what is the job our brand does"
- "segment by customer outcome"
- "outcome-based segmentation"
- "what causes customers to switch"
- "identify the job to be done"
- "rethink our market definition"
- "JTBD interviews"
- "what progress is the customer trying to make"
- "marketing malpractice"
inputs_schema:
{
  "task_type": "educate | identify-job | segmentation | innovation | positioning | research | learn",
  "request": "string",
  "brand_context": "string (optional) — describe product, category, customer",
  "output_format": "string (optional)"
}
outputs_schema:
{
  "verification": "string",
  "answer": "string",
  "jtbd_checklist": ["string"],
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
1. Identify the task type: educate | identify-job | segmentation | innovation | positioning | research.
2. Always call `get_skill_file` for `references/INDEX.md` first.
3. If `get_skill_file` or `search_docs` are unavailable, use `run_tool` fallback:
   - `run_tool` with `tool_name="get_skill_file"` and `args={"skill_id":"jobs-to-be-done","path":"references/INDEX.md"}`
   - `run_tool` with `tool_name="search_docs"` and `args={"skill_id":"jobs-to-be-done","query":"<keywords>","top_k":5}`
4. Load the minimum needed normalized files based on task type:
   - educate: `references/normalized/PRINCIPLES.md`, `references/normalized/GLOSSARY.md`
   - identify-job: `references/normalized/PRINCIPLES.md`, `references/normalized/JOB_MAPPING.md`
   - segmentation: `references/normalized/SEGMENTATION.md`, `references/normalized/JOB_MAPPING.md`
   - innovation: `references/normalized/PRINCIPLES.md`, `references/normalized/INNOVATION.md`
   - positioning: `references/normalized/PRINCIPLES.md`, `references/normalized/POSITIONING.md`
   - research: `references/normalized/RESEARCH_METHODS.md`, `references/normalized/JOB_MAPPING.md`
   - learn: Socratic mode — do NOT deliver the answer. Open with: "Describe the last time a customer chose your product. What were they trying to get done — functionally, emotionally, socially? What were they struggling with before they found you?" Then probe: What job is the brand actually hired for vs. what it assumes it's hired for? What would customers fire this brand for? Challenge demographic segmentation assumptions. Close with: "If Christensen reviewed your current customer segmentation, what would he say you're getting wrong?"
5. If source PDFs are relevant, read `references/normalized/PDF_SUMMARIES.md` before drafting.
6. If a needed detail is missing, call `search_docs` (or `run_tool` fallback) with focused keywords and use only returned hits.
7. Always frame "the job" in terms of the progress the customer is trying to make — not the product feature or customer demographic.
8. Distinguish between functional, emotional, and social dimensions of a job.
9. Apply the "hire / fire" metaphor: products are hired to do a job and fired when a better alternative appears.
10. When relevant, apply Ulwick's outcome-based segmentation: segment by desired outcomes, not demographics.
11. Internal tools are allowed when needed:
    - web_search: for current JTBD case studies and examples; label external sources separately.
    - canvas: for job maps or segmentation visuals when the user asks for visual output.
12. For each important claim, include evidence: `"<short quote>" (from: docs/<original-file>, lines: <start-end if known>)`.
13. Never cite internal skill paths in final output (`references/...` or `source/...` are forbidden in `Sources Used`).
14. If quote text is unavailable, state: `"No extractable quote (PDF/image-only; OCR unavailable or insufficient)."`
15. Produce the answer and include a section titled exactly `JTBD Checklist`.
16. Final answer MUST start with the verification string exactly.

JTBD Checklist:
- Job is defined as the progress the customer is trying to make — not the product feature or customer type.
- Job has functional, emotional, and social dimensions identified.
- Circumstance of the job is specified (when, where, in what context).
- Competing solutions (not just competing brands) are identified.
- Switch triggers (what causes hire/fire) are considered.
- Segmentation (if requested) is based on desired outcomes, not demographics.
- Innovation recommendations target unmet or underserved job outcomes.
- Sources cite original `docs/...` files only, never `references/...` or `source/...` paths.

VERIFICATION STRING: VERIFIED_SKILL:jobs-to-be-done:v1
Final answer must start with: VERIFIED_SKILL:jobs-to-be-done:v1
