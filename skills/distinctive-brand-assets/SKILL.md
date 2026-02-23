# SKILL: Distinctive Brand Assets

name: Distinctive Brand Assets
skill_id: distinctive-brand-assets
skill_group: brand-strategy
skill_subcategory: identity
version: 1.0
status: active

---

## Description

Teaches how to identify, measure, build, and protect distinctive brand assets (DBAs) — the sensory and verbal cues that trigger brand retrieval in memory. Covers Romaniuk's Distinctive Assets framework and Grid (fame × uniqueness), Keller's brand elements criteria (memorable, meaningful, likable, transferable, adaptable, protectable), asset types (visual, verbal, sonic, character), measurement approaches, and the consistency imperative.

---

## Triggers

- distinctive brand assets
- DBA
- brand elements
- brand codes
- brand identity
- logo
- brand colour
- brand character
- sonic logo
- jingle
- brand name distinctiveness
- brand symbol
- tagline memory
- distinctive assets grid
- brand asset fame
- brand asset uniqueness
- brand recognition
- brand recall
- asset consistency
- brand codes and cues
- Romaniuk brand assets
- Keller brand elements
- sensory brand cues
- verbal brand elements
- packaging distinctiveness

---

## Inputs Schema

```
task_type: educate | audit | build | measure | protect | learn
brand_name: string (optional)
asset_type: visual | verbal | sonic | character | all (optional)
context: string (optional)
```

---

## Outputs Schema

```
framework_explanation: markdown
asset_audit: markdown (if audit task)
build_recommendations: markdown (if build task)
measurement_approach: markdown (if measure task)
protection_guidance: markdown (if protect task)
citations: list of source references
verification: VERIFIED_SKILL:distinctive-brand-assets:v1
```

---

## Required Tools

- get_skill_file
- search_docs

---

## Optional Internal Tools

- run_tool

---

## Steps

1. **Verify skill loaded** — Output: `VERIFIED_SKILL:distinctive-brand-assets:v1`

2. **Load INDEX.md first** — Call `get_skill_file` with path `references/INDEX.md` for this skill.

3. **Classify task type** from input:
   - `educate` → explain DBA framework and brand elements criteria
   - `audit` → assess existing assets using Distinctive Assets Grid
   - `build` → recommend asset development priorities
   - `measure` → design fame × uniqueness measurement
   - `protect` → identify consistency risks and protection strategies
   - `learn` → Socratic mode: guide the student to apply the DBA framework themselves

4. **For learn tasks** — Do NOT deliver the answer directly. Use a Socratic approach:
   - Open with: "Before I explain the framework — pick one brand asset you think is most distinctive for your brand. Why do you think it's working? What makes you confident it's actually owned by your brand and not generic to the category?"
   - After the student responds: identify what is correct, what is missing, and what assumption needs testing
   - Present the Distinctive Assets Grid and Keller's 6 criteria as questions for the student to apply, not statements to read
   - After each student response, ask: "How would you measure that? What data would prove or disprove it?"
   - Challenge one assumption — e.g., "You say the colour is distinctive — but do customers actually link it to your brand, or just to the category?"
   - Close with: "What would you do first if your budget were cut in half — protect existing assets or build new ones? Defend that."

5. **For educate tasks** — Load `references/normalized/PRINCIPLES.md` and `references/normalized/ROMANIUK_FRAMEWORK.md`

5. **For audit tasks** — Load `references/normalized/ROMANIUK_FRAMEWORK.md` and `references/normalized/ASSET_TYPES.md`

6. **For build tasks** — Load `references/normalized/KELLER_ELEMENTS.md` and `references/normalized/ASSET_TYPES.md`

7. **For measure tasks** — Load `references/normalized/MEASUREMENT.md` and `references/normalized/ROMANIUK_FRAMEWORK.md`

8. **For protect tasks** — Load `references/normalized/CONSISTENCY.md` and `references/normalized/ROMANIUK_FRAMEWORK.md`

9. **Fallback** — If `get_skill_file` fails, use `run_tool` with `search_docs` and query matching the task type.

10. **Load supporting files as needed**:
    - `references/normalized/GLOSSARY.md` — for definitions
    - `references/normalized/PDF_SUMMARIES.md` — for source overviews
    - `references/normalized/SOURCE_QUOTES.md` — for direct citation evidence

11. **Apply Distinctive Assets Grid** for audit and measure tasks:
    - Plot assets on Fame (x-axis) × Uniqueness (y-axis)
    - Defend: high fame + high uniqueness
    - Invest: low fame + high uniqueness
    - Avoid/Watch: high fame + low uniqueness
    - Ignore/Test: low fame + low uniqueness

12. **Apply Keller's 6 criteria** for build and evaluate tasks:
    Memorable | Meaningful | Likable | Transferable | Adaptable | Protectable

13. **Cite evidence** using format: `"<quote or principle>" (from: docs/newskills/08_Distinctive_Brand_Assets/<filename>)`

14. **Structure output**:
    - Lead with verification string
    - Framework or audit section
    - Actionable recommendations with priorities
    - Key citations
    - Checklist of next steps

---

## Checklist

- [ ] VERIFIED_SKILL:distinctive-brand-assets:v1 output at start
- [ ] Task type correctly classified
- [ ] Distinctiveness vs. differentiation distinction made clear
- [ ] Distinctive Assets Grid applied for audit/measure tasks
- [ ] Keller's 6 criteria applied for build/evaluate tasks
- [ ] Asset types (visual, verbal, sonic, character) considered
- [ ] Fame and uniqueness as the two key DBA dimensions used
- [ ] Consistency imperative communicated for protect tasks
- [ ] Citations include source file references
- [ ] For learn tasks: Socratic mode active — student hypothesis elicited before framework is delivered

---

VERIFICATION STRING: VERIFIED_SKILL:distinctive-brand-assets:v1
