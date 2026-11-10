# Ledger schema & vocabularies (single owner — C4/C5/C7/C8 texts reference this file)

Machine state for one research run lives in the run dir
(`queries/deep-{session}/`): `00-brief.md`, `scratchpad.md`, `00-queries.md`,
`report.md` (+ child session pages). Lint: `scripts/ledger_lint.py RUNDIR`.

## Scratchpad finding line (canonical; parent appends after each wave, assigning E-ids)

```
- claim: {atomic claim} | id: E{n} | url: {https://...|none} | role: evidence|discovery
  | class: gov|academic|vendor|news|community|other | retrieval: full|partial|snippet|metadata
  | date: {YYYY-MM-DD|n/d} | status: VERIFIED|SUPPORTED|CORROBORATED|CONTRADICTED|UNVERIFIED|INFERRED
  | conf: high|med|low
```

Child return blocks carry the same fields (child cannot self-certify status:
child writes `status: UNVERIFIED` + the verbatim quote; parent/lint keep it).

**role** — `evidence`: the inspected source substantively supports/contradicts the
claim. `discovery`: helped locate info/direction only (search snippet, forum hint,
Wikipedia pointer). **A `discovery` finding can never carry a conclusion** —
conclusion bullets cite only evidence-role E-ids with retrieval full|partial.

**class** — site-level label of the publisher (borrowed vocabulary from
Perplexity's source labels: Government/Academic/Trusted). It NEVER substitutes
for the weight table or the per-claim judgment; absence of a meaningful class is
`other`, not low quality.

**retrieval** — what was actually seen: `full` document inspected; `partial`
relevant section read; `snippet` only search result text; `metadata` title/DOI
only. A snippet never upgrades a claim past UNVERIFIED. `date` = publication
date from the fetched copy, else `n/d` — never invented, never the page-update
date masquerading as freshness.

## Statuses (≤6, definitions + who may assign; never silently upgrade)

| status | definition | assigned by |
|---|---|---|
| VERIFIED | the cited retrieved document directly states the claim (judge: supports=yes) | claim-support judge |
| SUPPORTED | credible support with stated limits (secondary source, partial read, judge: partially) | judge / synthesis |
| CORROBORATED | ≥2 INDEPENDENT evidence sources after syndication dedup | synthesis ONLY |
| CONTRADICTED | credible evidence conflicts; both sides surface | judge / critic |
| UNVERIFIED | lacks primary provenance / not inspected (includes "unknown") | default (children) |
| INFERRED | reasoned conclusion from evidence, never presented as fact | synthesis ONLY (+caveat) |

Partial support = SUPPORTED + caveat text, not a separate token. The report never
carries raw status tokens and `[доверие: …]` tags mixed: map via report-format.md
(высокая = CORROBORATED or VERIFIED+official class; средняя = SUPPORTED or single
VERIFIED non-official; низкая = UNVERIFIED/INFERRED → limitations/противоречия).

## Coverage matrix (report section `## Покрытие`, binds to the BRIEF's subquestion list)

`- Q{n}: SUFFICIENT|PARTIAL|BLOCKED|UNRESOLVED|N-A`. No "COMPLETE" — it is
forbidden research vocabulary. Brief owns the Q-list (director covers every Q or
records a scope-cut line in 00-queries.md). PARTIAL/BLOCKED/UNRESOLVED must
surface in report limitations.

## Stop line (report footer, machine-readable)

`stop: saturation|budget|round-cap`. `saturation` is legal only under the
existing net-new-claims definition (below threshold 2–3 consecutive rounds).
When stop≠saturation the report must not contain «исчерпывающ», «exhaustive»,
«полное исследование», «complete research» — lint scans; budget exhaustion is
disclosed as unfinished work, never as completeness.

## Query log `00-queries.md` (parent-only appends; children never write it)

`- q: {query} | task: {id} | round: {n} | outcome: new|extension|duplicate|failed|LACK_OF_DATA`
Round 2+ must not re-issue a logged query without a new-angle reason line. Only
the director emits round-2 query strings; critic suggestions are consumed by the
director, never dispatched verbatim.

## Brief fields (00-brief.md, parent-owned; ≤12 lines)

topic / goal / depth / time-box / source whitelist (if any) / success criteria
(includes expected evidence type — no separate field) / inline topic line
(query type → source priorities) / `## Subquestions` section: `- Q1: …` lines.
Parent may amend the brief between rounds: record change+reason in
00-queries.md; coverage matrix binds to the LATEST list. Mid-run discovery that
the entity was resolved wrong → one logged name-collision re-dispatch, never
silent.
