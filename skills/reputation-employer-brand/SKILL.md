# SKILL: Reputation & Employer Brand

name: Reputation & Employer Brand
skill_id: reputation-employer-brand
skill_group: brand-strategy
skill_subcategory: reputation
version: 1.0
status: active

---

## Description

Teaches how organisations build, measure, and protect corporate reputation and employer brand. Covers Ambler & Barrow's employer brand framework (EVP), Brown & Dacin's corporate associations (CA + CSR), RepTrak's reputation measurement model (7 dimensions), Porter & Kramer's Creating Shared Value, Aaker's purpose-driven brand strategy, Schein's organisational culture model, and reputation risk management. Bridges internal brand (talent/culture) with external brand (stakeholder reputation).

---

## Triggers

- employer brand
- employer value proposition
- EVP
- corporate reputation
- reputation management
- RepTrak
- corporate associations
- corporate ability
- CSR associations
- creating shared value
- CSV
- purpose-driven brand
- brand purpose
- organisational culture
- culture and reputation
- reputation risk
- stakeholder trust
- corporate communication
- talent brand
- talent attraction
- employee experience brand
- Ambler Barrow employer brand
- Brown Dacin corporate associations
- Porter Kramer shared value
- Aaker purpose brand
- Schein culture

---

## Inputs Schema

```
task_type: educate | diagnose | strategy | measure | protect | learn
organisation_name: string (optional)
context: string (optional)
audience: employees | candidates | consumers | investors | all (optional)
```

---

## Outputs Schema

```
framework_explanation: markdown
reputation_assessment: markdown (if diagnose or measure)
strategy_recommendations: markdown (if strategy)
protection_plan: markdown (if protect)
citations: list of source references
verification: VERIFIED_SKILL:reputation-employer-brand:v1
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

1. **Verify skill loaded** — Output: `VERIFIED_SKILL:reputation-employer-brand:v1`

2. **Load INDEX.md first** — Call `get_skill_file` with path `references/INDEX.md` for this skill.

3. **Classify task type** from input:
   - `educate` → explain employer brand and/or reputation frameworks
   - `diagnose` → assess current reputation or employer brand gaps
   - `strategy` → recommend CSV, purpose, or EVP strategy
   - `measure` → design RepTrak or employer brand measurement
   - `protect` → identify reputation risks and mitigation
   - `learn` → Socratic mode: guide the student to apply the frameworks themselves

4. **For learn tasks** — Do NOT deliver the answer directly. Use a Socratic approach:
   - Open with: "Before I walk you through the frameworks — what do you think is the biggest gap between what this organisation says it stands for and what it actually delivers? Start there."
   - After the student responds: identify what is correct, what is missing, and what assumption needs testing
   - Present RepTrak, Brown & Dacin's CA/CSR model, and Schein's culture levels as diagnostic questions, not explanations
   - After each student response, ask: "What evidence would a sceptical board member demand before accepting that assessment?"
   - Challenge one assumption — e.g., "You say the employer brand is strong — but what do Glassdoor reviews and voluntary attrition data actually show?"
   - Close with: "If you could fix only one thing — reputation externally or culture internally — which would you tackle first and why?"

5. **For educate tasks** — Load `references/normalized/PRINCIPLES.md` and `references/normalized/EMPLOYER_BRAND.md`

5. **For diagnose tasks** — Load `references/normalized/CORPORATE_REPUTATION.md` and `references/normalized/CULTURE.md`

6. **For strategy tasks** — Load `references/normalized/CREATING_SHARED_VALUE.md` and `references/normalized/PURPOSE_DRIVEN_BRAND.md`

7. **For measure tasks** — Load `references/normalized/REPUTATION_MEASUREMENT.md` and `references/normalized/EMPLOYER_BRAND.md`

8. **For protect tasks** — Load `references/normalized/REPUTATION_RISK.md` and `references/normalized/CORPORATE_REPUTATION.md`

9. **Fallback** — If `get_skill_file` fails, use `run_tool` with `search_docs` and query matching the task type.

10. **Load supporting files as needed**:
    - `references/normalized/GLOSSARY.md` — for definitions
    - `references/normalized/PDF_SUMMARIES.md` — for source overviews
    - `references/normalized/SOURCE_QUOTES.md` — for direct citation evidence

11. **Apply relevant framework based on audience:**
    - Internal (employees/candidates) → Employer Brand / EVP / Culture (Schein)
    - External (consumers/investors) → Corporate Reputation / Corporate Associations (Brown & Dacin)
    - Strategic (all stakeholders) → CSV (Porter & Kramer) / Purpose (Aaker)

12. **Apply Brown & Dacin's two-association model** for corporate reputation:
    - Corporate Ability (CA): expertise in production/delivery
    - Corporate Social Responsibility (CSR): social character and values

13. **Apply RepTrak 7 dimensions** for measurement tasks:
    Products & Services | Innovation | Workplace | Governance | Citizenship | Leadership | Performance

14. **Cite evidence** using format: `"<quote or principle>" (from: docs/newskills/09_Reputation_Employer_Brand/<filename>)`

15. **Structure output**:
    - Lead with verification string
    - Framework or diagnosis section
    - Audience-specific recommendations
    - Key citations
    - Checklist of next steps

---

## Checklist

- [ ] VERIFIED_SKILL:reputation-employer-brand:v1 output at start
- [ ] Task type and audience correctly classified
- [ ] Employer brand (internal) vs. corporate reputation (external) distinguished
- [ ] Brown & Dacin CA + CSR associations applied for reputation tasks
- [ ] RepTrak 7 dimensions referenced for measurement tasks
- [ ] EVP components addressed for employer brand tasks
- [ ] Culture (Schein's 3 levels) considered as foundation
- [ ] CSV or purpose strategy applied for strategic tasks
- [ ] Reputation risk sources and mitigations addressed for protect tasks
- [ ] Citations include source file references
- [ ] For learn tasks: Socratic mode active — student hypothesis elicited before framework is delivered

---

VERIFICATION STRING: VERIFIED_SKILL:reputation-employer-brand:v1
