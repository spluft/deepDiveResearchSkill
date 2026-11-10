# Verification (claim-level; complements step 6/9a/10)

## Claim-atomic decomposition (mandatory before any verdict)

Split compound findings into independently verifiable claims; one evidence chain
per claim. "X supports Y, added in 3.2, on by default, +20% faster" = four
claims needing different evidence; one source may support two only. Verdicts are
never issued over compound sentences.

## Three-gate citation audit (mapping — arXiv:2605.06635)

1. **Link works** → step 10 `verify_urls.py` (the ONLY network checker).
2. **Relevant** + 3. **Supports the exact claim** → narrow claim-support judge
   ("does the cited URL actually support this line? yes/no/partially/
   contradicts"), stronger model than collectors, one URL at a time. The lint
   (ledger_lint.py) checks structure only — nobody expects it to judge semantics.
Misattribution is the dominant failure, not fabrication: ~4/5 of unsupported
agent claims are right numbers from the wrong source (arXiv:2610.38691) — keep
verbatim quotes; "a correct number can carry a wrong story" is the first
conflict axis the critic enumerates.

## Critic's bounded gap output

Critic appends `missing_evidence:` — ≤3 items, each `page → key claim lacking
primary source`. The critic NEVER emits query strings (rejected:
critic-generated queries = the banned separate-planner role); the director turns
missing_evidence into round-2 queries, logs them, and the round MUST retrieve
NEW sources — re-reading the same pages is the banned second pass over the same
context (arXiv:2310.01798, 2406.01297).

## S3-only domain checks (≤3 lines each; consulted by critic/judge, never tick-boxed)

- scientific: design vs question fit; sample/effect/CI; preprint vs peer-
  reviewed; replication; statsignificance ≠ practical benefit; correlation ≠ causation.
- technical: released vs announced vs experimental; version+date pinned;
  benchmark workload/method; reproducibility; known issues.
- product: spec ≠ measurement — separate manufacturer claims (mark
  `[vendor claim]`), independent lab numbers, user experience; never mix tiers.
- legal: jurisdiction named; original text + amendments + effective dates; no
  cross-jurisdiction transfer without justification.
- current events: event date vs publication date vs confirmation; early
  reporting is not established fact.

## Manual smoke checklist (run on demand after skill edits, outside tests)

S0/S1 spawn zero children; an S2 run logs every deviation `sources:` line; a
snippet-only finding cannot reach `## Выводы`; a CONTRADICTED claim survives to
the report both-sides; stop: budget ⇒ no «исчерпывающ/exhaustive» wording;
resume after context cut reads only `queries/deep-{session}/` and never re-runs
waves.
