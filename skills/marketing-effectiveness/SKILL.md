# SKILL: Marketing Effectiveness

name: Marketing Effectiveness
skill_id: marketing-effectiveness
skill_group: brand-strategy
skill_subcategory: effectiveness
version: 1.0
status: active

---

## Description

Teaches how to maximise marketing effectiveness using evidence-based frameworks. Covers Binet & Field's Long and Short of It (brand building vs. sales activation, the 60/40 split), the 95-5 Rule (in-market vs. out-of-market buyers), Ehrenberg-Bass Double Jeopardy Law, how advertising works (emotional vs. rational routes), ESOV and market share growth, and measurement approaches. Bridges brand strategy with marketing investment decisions and ROI.

---

## Triggers

- marketing effectiveness
- advertising effectiveness
- brand building
- sales activation
- long and short of it
- Binet and Field
- 60 40 split
- brand vs activation
- short termism marketing
- 95-5 rule
- in-market buyers
- out of market buyers
- double jeopardy
- Ehrenberg-Bass effectiveness
- ESOV
- excess share of voice
- share of voice
- share of market
- how advertising works
- emotional advertising
- rational advertising
- advertising ROI
- marketing ROI
- marketing mix modelling
- media effectiveness
- IPA effectiveness
- marketing investment
- penetration growth
- advertising mechanisms
- fame advertising

---

## Inputs Schema

```
task_type: educate | diagnose | strategy | measure | plan | learn
brand_name: string (optional)
context: string (optional)
budget_concern: string (optional)
```

---

## Outputs Schema

```
framework_explanation: markdown
effectiveness_diagnosis: markdown (if diagnose task)
strategy_recommendations: markdown (if strategy or plan task)
measurement_approach: markdown (if measure task)
citations: list of source references
verification: VERIFIED_SKILL:marketing-effectiveness:v1
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

1. **Verify skill loaded** — Output: `VERIFIED_SKILL:marketing-effectiveness:v1`

2. **Load INDEX.md first** — Call `get_skill_file` with path `references/INDEX.md` for this skill.

3. **Classify task type** from input:
   - `educate` → explain Long and Short framework and key principles
   - `diagnose` → identify why current marketing may be underperforming
   - `strategy` → recommend brand/activation balance and investment approach
   - `measure` → design effectiveness measurement framework
   - `plan` → build a media/investment plan using effectiveness principles
   - `learn` → Socratic mode: guide the student to apply effectiveness frameworks themselves

4. **For learn tasks** — Do NOT deliver the answer directly. Use a Socratic approach:
   - Open with: "Before I share the evidence — what's your instinct on how this brand's marketing budget should be split between brand building and activation? Give me a number and your reasoning."
   - After the student responds: identify what is correct, what is missing, and what assumption needs testing
   - Present the 60/40 principle, 95-5 rule, and Double Jeopardy as questions for the student to apply to their brand, not facts to absorb
   - After each student response, ask: "What would your ESOV look like vs. competitors? And what does that predict for market share?"
   - Challenge one assumption — e.g., "You're confident performance marketing is working — but are you measuring only the 5% in-market? What about the 95% you're not reaching?"
   - Close with: "If your CFO cut brand budget by 30% citing 'no short-term ROI' — how would you make the evidence-based case against that decision?"

5. **For educate tasks** — Load `references/normalized/PRINCIPLES.md` and `references/normalized/LONG_AND_SHORT.md`

5. **For diagnose tasks** — Load `references/normalized/BRAND_VS_ACTIVATION.md` and `references/normalized/DOUBLE_JEOPARDY.md`

6. **For strategy tasks** — Load `references/normalized/LONG_AND_SHORT.md` and `references/normalized/95_5_RULE.md`

7. **For measure tasks** — Load `references/normalized/MEASUREMENT.md` and `references/normalized/BRAND_VS_ACTIVATION.md`

8. **For plan tasks** — Load `references/normalized/LONG_AND_SHORT.md`, `references/normalized/95_5_RULE.md`, and `references/normalized/BRAND_VS_ACTIVATION.md`

9. **Fallback** — If `get_skill_file` fails, use `run_tool` with `search_docs` and query matching the task type.

10. **Load supporting files as needed**:
    - `references/normalized/HOW_ADVERTISING_WORKS.md` — for mechanism questions
    - `references/normalized/GLOSSARY.md` — for definitions
    - `references/normalized/PDF_SUMMARIES.md` — for source overviews
    - `references/normalized/SOURCE_QUOTES.md` — for direct citation evidence

11. **Apply the Long and Short balance test** for any investment question:
    - What % of budget is brand building vs. activation?
    - Is the brand investing enough for long-term growth?
    - Is activation over-indexed (short-termism risk)?

12. **Apply the 95-5 Rule** when the client is considering targeting "only in-market buyers":
    - Only 5% are in-market; 95% are future buyers
    - Brand advertising must reach the 95% to build future demand
    - Activation should target the 5% to convert current demand

13. **Apply Double Jeopardy** for penetration vs. loyalty questions:
    - Growth comes from more buyers (penetration), not from making existing buyers more loyal
    - Light buyers vastly outnumber heavy buyers; reaching them is key

14. **Cite evidence** using format: `"<quote or principle>" (from: docs/newskills/10_Marketing_Effectiveness/<filename>)`

15. **Structure output**:
    - Lead with verification string
    - Framework or diagnosis section
    - Specific recommendations with rationale
    - Key citations
    - Checklist of next steps

---

## Checklist

- [ ] VERIFIED_SKILL:marketing-effectiveness:v1 output at start
- [ ] Task type correctly classified
- [ ] Long and Short of It framework applied where relevant
- [ ] Brand building vs. activation balance assessed
- [ ] 95-5 rule applied for targeting and audience questions
- [ ] Double Jeopardy applied for penetration vs. loyalty questions
- [ ] ESOV principle applied for share of voice questions
- [ ] How advertising works (emotional vs. rational) addressed if relevant
- [ ] Measurement approach included for strategy recommendations
- [ ] Citations include source file references
- [ ] For learn tasks: Socratic mode active — student hypothesis elicited before framework is delivered

---

VERIFICATION STRING: VERIFIED_SKILL:marketing-effectiveness:v1
