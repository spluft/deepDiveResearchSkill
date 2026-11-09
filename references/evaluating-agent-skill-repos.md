# Evaluating an external agent-skill / framework repo

For "should we adopt / replace / partially take skill X from GitHub" requests.

## Procedure

1. `git clone --depth 1` into the scratch dir; never evaluate from the README alone —
   READMEs market, protocol files are the truth.
2. Size the corpus first: `wc -c` over the skill's `.md` files. Same-skill copies are
   often duplicated per host-agent dir (.opencode/.muse/.claude/plugins) — pick the
   canonical dir (usually `plugins/<name>/skills/<name>/`) and read only it, times N
   otherwise.
3. Read the entry SKILL.md + core protocol file(s) FIRST (largest files), then cherry-pick
   references/ by title. Budget: core ~20KB before deciding whether to dig further.
4. Judge GENRE before anything else: does the external skill's loop operate on external
   knowledge (our class) or on own-systems metrics/code (business-task-intake / kanban
   class)? Genre mismatch → answer is always "partial borrow or nothing", never
   "replace"; adopting a wrong-genre skill wholesale is dead weight in the profile.
5. Deliver the verdict as: genre call → what to borrow (each with the step of OUR
   pipeline it lands on) → what to reject WITH the mechanism of why it doesn't
   transfer → offer to implement as a version bump + three-way re-sync (see SKILL.md
   Canonical copies & sync).
6. Protocol-only (markdown) skill repos have nothing to smoke-test — read-only
   evaluation is valid there; the live-smoke-test pitfall applies to repos shipping
   runnable tools.

## Standing verdicts (reviewed repos)

### uditgoenka/autoresearch (autonomous iteration loop, v2.3)
Genre: modify→verify→keep/discard metric loops on code/own systems + orchestrator
routing shell-script. NOT web research. Do NOT adopt as a skill; NOT a replacement.

BORROWED as candidate upgrades (pending user sign-off per pattern):
- Saturation stop: wave ends when net-new findings < threshold for 3 consecutive
  rounds (marginal-return stop, not just budget).
- Claim-level dedup: canonicalize each finding ({problem, persona/aspect, mechanism})
  and classify new/extension/duplicate — dedupes two leaves returning the same
  finding in different words; complements our source-mirror dedup.
- Blind judges for comparative verdicts: candidates under randomized labels, judges
  MUST rank ("all good" invalid), agents cold-started (anti-sycophancy) — use in S3
  synthesis when choosing BETWEEN alternatives.
- Forced-adversarial critic quota: critic must report >=3 concrete weaknesses with
  evidence and never compliment.

REJECTED with reason:
- Fork-and-flush (K fresh-context branches from best commit) — needs a numeric verify
  signal to select branches; web research has none, and its flush half (stateless
  leaves, files-only state) is already our design.
- TSV ledgers/evals/regression gates and the deterministic-routing shell script —
  belong to dev-loop territory (kanban/business-task-intake), not the research skill.
  Reusable idea for that class: routing logic in a deterministic script, success
  predicate pinned verbatim at round 0 and re-screened on resume, never re-derived.
