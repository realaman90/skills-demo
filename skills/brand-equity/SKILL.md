# SKILL: Brand Equity

name: Brand Equity
skill_id: brand-equity
skill_group: brand-strategy
skill_subcategory: equity
version: 1.0
status: active

---

## Description

Teaches how brand equity is defined, measured, built, and protected. Covers Keller's Customer-Based Brand Equity (CBBE) pyramid, Feldwick's three-strand framework, brand knowledge structures (awareness + image), financial valuation approaches, sources of equity dilution, and strategies for equity building through CSR and associations.

---

## Triggers

- brand equity
- CBBE
- customer-based brand equity
- brand knowledge
- brand associations
- brand awareness
- brand image
- brand value
- brand strength
- brand asset value
- equity building
- equity dilution
- brand pyramid
- brand resonance
- brand salience
- brand performance
- brand feelings
- brand judgments
- intangible asset
- brand trust
- Keller brand equity
- Feldwick brand equity
- brand loyalty metric
- corporate societal marketing
- CSR and brand equity

---

## Inputs Schema

```
task_type: educate | diagnose | strategy | measure | protect | learn
brand_name: string (optional)
context: string (optional)
equity_concern: string (optional)
```

---

## Outputs Schema

```
framework_explanation: markdown
equity_assessment: markdown (if diagnose or measure)
strategy_recommendations: markdown (if strategy or protect)
citations: list of source references
verification: VERIFIED_SKILL:brand-equity:v1
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

1. **Verify skill loaded** — Output: `VERIFIED_SKILL:brand-equity:v1`

2. **Load INDEX.md first** — Call `get_skill_file` with path `references/INDEX.md` for this skill to understand all available reference files.

3. **Classify task type** from input:
   - `educate` → explain CBBE framework and brand knowledge structure
   - `diagnose` → assess current equity gaps
   - `strategy` → recommend equity-building actions
   - `measure` → recommend measurement approaches
   - `protect` → identify dilution risks and mitigation
   - `learn` → Socratic mode: guide the student to apply the framework themselves

4. **For learn tasks** — Do NOT deliver the answer directly. Use a Socratic approach:
   - Open with: "Before I walk you through the framework — what's your current read on brand equity for your brand or case? Give me your hypothesis first."
   - After the student responds: identify what is correct, what is missing, and what assumption needs testing
   - Present the CBBE pyramid and Feldwick's three strands as questions for the student to answer, not statements to absorb
   - After each student response, ask: "What trade-offs did you consider?" and "What evidence supports that?"
   - Challenge at least one assumption before endorsing their conclusion
   - Close with: "What would change your answer if a key variable — competitive intensity, budget, category maturity — shifted?"

5. **For educate tasks** — Load `references/normalized/PRINCIPLES.md` and `references/normalized/CBBE_FRAMEWORK.md`

5. **For diagnose tasks** — Load `references/normalized/BRAND_KNOWLEDGE.md` and `references/normalized/MEASUREMENT.md`

6. **For strategy tasks** — Load `references/normalized/EQUITY_BUILDING.md` and `references/normalized/CBBE_FRAMEWORK.md`

7. **For measure tasks** — Load `references/normalized/MEASUREMENT.md` and `references/normalized/FINANCIAL_EQUITY.md`

8. **For protect tasks** — Load `references/normalized/EQUITY_DILUTION.md` and `references/normalized/BRAND_KNOWLEDGE.md`

9. **Fallback** — If `get_skill_file` fails, use `run_tool` with `search_docs` and query matching the task type.

10. **Load supporting files as needed**:
    - `references/normalized/GLOSSARY.md` — for definitions
    - `references/normalized/PDF_SUMMARIES.md` — for source paper overviews
    - `references/normalized/SOURCE_QUOTES.md` — for direct citation evidence

11. **Apply CBBE pyramid** when diagnosing or educating:
    - Layer 1: Salience (brand identity — who are you?)
    - Layer 2: Performance + Imagery (brand meaning — what are you?)
    - Layer 3: Judgments + Feelings (brand response — what about you?)
    - Layer 4: Resonance (brand relationship — what about you and me?)

12. **Apply Feldwick's three strands** when discussing equity definitions:
    - Brand strength (behavioural loyalty)
    - Brand value (financial worth)
    - Brand description (associations, personality, image)

13. **Cite evidence** using format: `"<quote or principle>" (from: docs/newskills/07_Brand_Equity/<filename>)`

14. **Structure output**:
    - Lead with verification string
    - Framework or diagnosis section
    - Actionable recommendations (for strategy/protect tasks)
    - Key citations
    - Checklist of next steps

---

## Checklist

- [ ] VERIFIED_SKILL:brand-equity:v1 output at start
- [ ] Task type correctly classified
- [ ] CBBE pyramid applied where relevant
- [ ] Feldwick framework referenced for equity definition questions
- [ ] Brand knowledge (awareness + image) assessed
- [ ] Equity sources and dilution risks addressed
- [ ] Financial vs. customer-based equity distinguished if asked
- [ ] Measurement approach recommended for measure tasks
- [ ] Citations include source file references
- [ ] For learn tasks: Socratic mode active — student hypothesis elicited before framework is delivered

---

VERIFICATION STRING: VERIFIED_SKILL:brand-equity:v1
