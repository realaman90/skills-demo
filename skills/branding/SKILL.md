name: Branding
skill_id: branding
description: Umbrella brand skill for writing, reviewing, and terminology checks using available docs.
triggers:
- "write brand copy"
- "review this copy for brand fit"
- "align this message to our voice"
- "check if this claim is allowed"
- "create a headline and CTA"
- "improve tone consistency"
- "enforce approved terms"
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
  "sources_used": ["string"]
}
required_tools:
- get_skill_file
- search_docs
steps:
1. Determine request mode: writing, review, messaging, or terminology.
2. Always call `get_skill_file` for `references/INDEX.md` first.
3. Read the minimum needed normalized files:
   - writing: `references/normalized/VOICE.md`, `references/normalized/MESSAGING.md`, `references/normalized/GLOSSARY.md`, `references/normalized/EXAMPLES.md`
   - review: `references/normalized/VOICE.md`, `references/normalized/MESSAGING.md`, `references/normalized/GLOSSARY.md`, `references/normalized/CONSTRAINTS.md`
   - messaging: `references/normalized/MESSAGING.md`, `references/normalized/EXAMPLES.md`, `references/normalized/CONSTRAINTS.md`
   - terminology: `references/normalized/GLOSSARY.md`
4. If source PDFs are relevant, read `references/normalized/PDF_SUMMARIES.md` before drafting.
5. If a needed detail is missing, call `search_docs` with focused keywords and use only returned hits.
6. Produce the answer and include a section titled exactly `Compliance Checklist`.
7. Final answer MUST start with the verification string exactly.

Compliance Checklist:
- Voice and tone match `references/normalized/VOICE.md`.
- Messaging and claims match `references/normalized/MESSAGING.md`.
- Terminology follows `references/normalized/GLOSSARY.md`.
- Example style aligns with `references/normalized/EXAMPLES.md`.
- Legal and compliance constraints checked against `references/normalized/CONSTRAINTS.md`.
- Any missing rule is explicitly marked as "Not specified in docs."

VERIFICATION STRING: VERIFIED_SKILL:branding:v1
Final answer must start with: VERIFIED_SKILL:branding:v1
