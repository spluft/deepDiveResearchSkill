# Source routing (per-microtask scope line — NOT a gate stage)

The director may add ONE `sources:` line per microtask:
`sources: primary={families}; secondary={families}; avoid={families}; expand_if={condition}`
**Omitted = defaults below apply** — write the line only when deviating
(including from operator whitelists in the brief). It is a prioritized research
scope, never a hard allowlist. Backing: curated-vs-open coverage/trust trade-off
(arXiv:2607.05217), per-source-type evidence retrieval (arXiv:2603.00267); the
standalone topic-classifier stage stays REJECTED — this is a scope line attached
to a decomposed task, chosen after planning, by subtopic.

## Defaults (≤5 rows; domain read off the inline topic line)

| domain | primary | secondary | discovery only |
|---|---|---|---|
| science/medicine | original papers, registries (arXiv/PubMed/ClinicalTrials.gov), official bodies | systematic reviews/meta-analyses | wikis, news |
| software/infra | official docs, source code (release tarball), changelogs, issue trackers | independent benchmarks | HN/Reddit/blogs |
| product/hardware | manufacturer specs, recall/warranty docs | independent measurements, pro reviews | owner forums, user reports |
| law | official statutes/judgments of the jurisdiction | professional commentary | legal blogs |
| current events | official records, original statements | established newsrooms | aggregators, feeds |

## Rules

- Discovery source ≠ evidence source: a forum post identifying a bug is a lead;
  the GitHub issue or code is the evidence. Record both roles via `role:` in the
  ledger line (references/ledger-schema.md).
- Wikipedia: orientation + terminology + reference mining only; follow its
  citations up to primary sources; never a citation in the report for a factual
  key claim when a primary source exists.
- Expand scope only when: evidence insufficient / selected sources lack the
  answer / contradiction found / independent confirmation needed — record the
  reason as a query-log line. Never pad source counts with low-quality sites.
- Prefer the known specialist source over a broad search when one exists.
- Domain-restricted search where the tool supports it (`site:`, database UIs,
  the endpoint kit in oss-project-eval-apis.md).
