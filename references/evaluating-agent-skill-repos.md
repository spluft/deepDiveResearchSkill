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

ADOPTED into SKILL.md as of v2.1.0 (2026-11-09, user sign-off):
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

## Evidence-backed stage verdicts (designing/evaluating any research pipeline)

Cross-checked survey of live deep-research frameworks (gpt-researcher, langchain
open_deep_research, deer-flow v2, storm, dzhng/deep-research, deepdive,
hybrid-deep-research, dexter) + engineering blogs + self-correction literature;
full record in the wiki (`queries/deep-agent-pipelines-2026-11/`):

- Severity/effort triage tiers: SUPPORTED (Anthropic explicit scaling rule: 1 agent
  3–10 calls / 2–4 subagents 10–15 each / 10+ subagents with divided responsibilities).
- Topic/domain classifier as a standalone stage before planning: WEAK — no live
  framework has one; keep topic hints inline in the brief, never a gated stage.
- Per-document summarization before analysis: SUPPORTED — the unit is
  URL + verbatim quote; paraphrase-under-summarization-pressure destroys precision.
- Separate fact-check / critic roles: SUPPORTED (CoVe independent verification,
  CRITIC tool-grounded critique, dedicated citation pass); judge-role PROLIFERATION
  not proven better — one well-prompted judge was most consistent.
- A second fixed self-critique round on the same context: CONTRADICTED — LLMs do not
  self-correct without external feedback and can degrade (Huang ICLR 2024;
  Kamoi TACL 2024 survey). A repeat round is justified only when it consumes NEW
  external evidence (fresh retrieval, source re-read, tool check); no published
  A/B of "2× vs 1×" exists — do not sell a double loop as proven better.
- Stopping rule: saturation (last N sources add nothing new) + hard budget cap is
  the practice convergent among newest systems; fixed round counters are legacy
  framework behavior; superiority of either is unpublished — mark as practice,
  not evidence.
- Final report: ONE-SHOT generation from condensed findings — parallel section-by-
  section writing measured "disjointed and not very cohesive" (LangChain).
- anthropics/skills ships NO deep-research skill — never cite one as a reference.
- Socialpranker/deepdive (365★) + Ddibirov/hybrid-deep-research (16★) implement the
  richest pipelines (genre/depth gate, claims ledger, saturation stop, multi-axis
  verify) but are solo-authored self-promo: their internal numbers (e.g. "Search-o1
  33%→24%", "URL fabrication impossible") are unverified claims — borrow the
  anatomy, never quote the stats.
