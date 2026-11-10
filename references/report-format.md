# Report format (synthesis — pipeline step 9)

`report.md` MUST use this format, compiled from session pages ONLY.

## Source-conflict resolution — authority weights

official_docs 1.0 > news 0.7 > analysis/repo 0.6 > blog 0.4 > social 0.3.
Recency tiebreak: stale authority gets "по состоянию на {год}", newer wins,
keep both. Weights are PRIORS, never verdicts: per-claim fitness is decided by
critic/judge with a stated reason; a fitness override of the prior must say why.

## Confidence tags

Key findings tagged `[доверие: высокая|средняя|низкая]` — mapped from ledger
statuses (references/ledger-schema.md); report prose never mixes raw status
tokens with these tags:

- высокая = CORROBORATED (2+ independent after syndication dedup) or VERIFIED + official class
- средняя = SUPPORTED, or single VERIFIED non-official
- низкая = UNVERIFIED/INFERRED → also listed in «Противоречия»/limitations

## Structures (pick one by category)

- comparison → таблица + best-for вердикты
- howto → шаги + частые ошибки
- product → ранкинг + mini-таблица + вердикт
- general → Executive summary → Key findings → Соц.пульс (если есть) →
  Противоречия → Источники (нумерованные, с датой и типом)

## Length

Report <400 words at moderate depth → expand once.

## Citation rules (non-negotiable, also in SKILL.md)

Every factual block cites its URL; no evidence → literally "Не подтверждено: …";
never invent, repair or extrapolate a URL.