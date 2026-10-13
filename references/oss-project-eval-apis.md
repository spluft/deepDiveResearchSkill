# OSS project evaluation via primary APIs (HackerNews-proof evidence set)

For "is X good / what are the alternatives" research on GitHub projects. Every number
below is from the project's own registries — no blog/README trust needed.

## Endpoint kit (all plain `curl -sL -A 'Mozilla/5.0'`)
| Question | Endpoint | Watch for |
|---|---|---|
| Maturity / activity | `api.github.com/repos/{o}/{r}` → stars, forks, open_issues, created_at, pushed_at, license, **default_branch** | fetch README via `raw.githubusercontent.com/{o}/{r}/<default_branch>/README.md` (wrong branch = 404) |
| Security record | `api.github.com/repos/{o}/{r}/security-advisories?per_page=100` | count + severity + "incomplete fix" in titles; absent/empty ≠ secure — check for closed security issues too |
| Bus factor | `api.github.com/repos/{o}/{r}/contributors?per_page=10` | #1-vs-#2 contribution gap; check #2's last activity date |
| Release cadence | `api.github.com/repos/{o}/{r}/releases?per_page=5` | gaps between tags vs commit push date |
| Real adoption | `api.npmjs.org/downloads/point/last-month/{pkg}`; Docker Hub `hub.docker.com/v2/repositories/{ns}/{img}/` (pull_count) | compare download volume against star count |
| Organic buzz | `hn.algolia.com/api/v1/search?query={name}&tags=story` and `search_by_date?...&tags=comment` | big-stars + ~zero HN stories/comments = manufactured hype flag |
| Existence check | `api.github.com/search/repositories?q={name}&sort=stars` | the competitor named in a brief may not exist at all — confirm before dispatching more children after it |

## Credibility tells (green/red)
- **Fork-to-star ratio**: healthy 2–4%; ≥10% suggests promo/coordinated installs (both extremes worth reporting).
- **Stars vs organic-discussion ratio**: 30k+ stars with no HN story and only tutorial-farm content = synthetic growth; report it as a finding, not just context.
- **Astroturf shape**: same-URL spam from vendor-adjacent accounts, multilingual tutorial-video wall in the README, promo baseline on social — collapse to ONE promotional source per the dedupe rule.
- **Vaporware shape**: polished README + repo 404 on the API / only a zero-star personal mirror → immediately do-not-recommend, say so in the report.
- **AI-written code**: co-author trailers like `Claude Code <noreply@anthropic.com>` on most commits — note under maturity, changes maintenance risk assessment.

## Order that worked
repo API (facts + default_branch) → README raw → security-advisories → contributors/releases → npm/Docker volume → HN Algolia → then alternatives landscape sweep (one child per niche tier: same-problem competitors vs adjacent-category tooling), each child verifying stars/last-push on api.github.com itself.
