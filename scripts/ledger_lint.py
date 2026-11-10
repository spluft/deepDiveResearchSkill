#!/usr/bin/env python3
"""Deterministic ledger linter for the research pipeline (zero-LLM, zero-network).

Usage:
    python3 ledger_lint.py RUNDIR [--no-report] [--json]

RUNDIR must contain: 00-brief.md, scratchpad.md, 00-queries.md, report.md.
Missing files are structural FAILs (report.md exempt with --no-report).
Structural FAIL -> exit 2; otherwise advisories -> exit 1; otherwise exit 0.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_urls import extract_urls, URL_RE  # shared URL extraction; do not reimplement

STATUSES = "VERIFIED|SUPPORTED|CORROBORATED|CONTRADICTED|UNVERIFIED|INFERRED"
CLAIM_RE = re.compile(
    r"^- claim: (?P<claim>.+?) \| id: (?P<id>E\d+) \| url: (?P<url>https://[^|\s]+|none) \| "
    r"role: (?P<role>evidence|discovery) \| class: (?P<class>gov|academic|vendor|news|community|other) \| "
    r"retrieval: (?P<retrieval>full|partial|snippet|metadata) \| date: (?P<date>\d{4}-\d{2}-\d{2}|n/d) \| "
    r"status: (?P<status>" + STATUSES + r") \| conf: (?P<conf>high|med|low)$")
STATUS_BACKING = {"VERIFIED", "SUPPORTED", "CORROBORATED"}
RETR_BACKING = {"full", "partial"}
COV_STATUSES = ("SUFFICIENT", "PARTIAL", "BLOCKED", "UNRESOLVED", "N-A")
FORBIDDEN = ("исчерпывающ", "exhaustive", "полное исследование", "complete research")
BARE_DOMAIN_RE = re.compile(
    r"(?:^|[^:/\w])((?:[a-z0-9-]+\.)+(?:com|org|net|io|ru|dev|ai|gov|edu))\b", re.MULTILINE)
QLINE_RE = re.compile(r"^- Q(\d+):\s*(.*)$")
QUERY_RE = re.compile(r"^- q: (.+?) \| task: \S+ \| round: \d+ \| outcome: "
                      r"(new|extension|duplicate|failed|LACK_OF_DATA)", re.MULTILINE)
EREF_RE = re.compile(r"\[E(\d+)\]")
STOP_RE = re.compile(r"^stop: (saturation|budget|round-cap)$", re.MULTILINE)
SUBQ_RES = [re.compile(r"^## Subquestions\b")]
CONC_RES = [re.compile(r"^## Выводы\b"), re.compile(r"^## Conclusions\b")]
COV_RES = [re.compile(r"^## Покрытие\b"), re.compile(r"^## Coverage\b")]
FILES = ("00-brief.md", "scratchpad.md", "00-queries.md", "report.md")


def read(rundir, name):
    path = os.path.join(rundir, name)
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def section_lines(text, header_res):
    """Body '- ' lines of the first section whose header matches any regex (None: no section)."""
    if not text:
        return None
    out, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            if inside:
                break
            inside = any(rx.match(line) for rx in header_res)
        elif inside and line.startswith("- "):
            out.append(line)
    return out


def counts(findings, field):
    out = {}
    for d in findings.values():
        out[d[field]] = out.get(d[field], 0) + 1
    return out


def main():
    no_report, as_json = "--no-report" in sys.argv[1:], "--json" in sys.argv[1:]
    args = [a for a in sys.argv[1:] if a not in ("--no-report", "--json")]
    if not args:
        print("usage: ledger_lint.py RUNDIR [--no-report] [--json]")
        return 2
    fails, advs, stats = [], [], []
    text = {n: read(args[0], n) for n in FILES}
    for name, t in text.items():
        if t is None and not (name == "report.md" and no_report):
            fails.append(("missing-file", f"{name} not found in {args[0]}"))
    brief = text["00-brief.md"] or ""
    scratch = text["scratchpad.md"] or ""
    queries = text["00-queries.md"] or ""
    report = text["report.md"] or ""

    # S1: brief subquestions section with Q bullets
    brief_qids, qsec = set(), section_lines(brief, SUBQ_RES)
    if qsec is None:
        fails.append(("S1", "brief: no '## Subquestions' section"))
    else:
        brief_qids = {"Q" + m.group(1) for ln in qsec if (m := QLINE_RE.match(ln))}
        if not brief_qids:
            fails.append(("S1", "brief: '## Subquestions' has no '- Q<n>:' bullets"))

    # S2: scratchpad claim lines parse against the canonical schema
    findings, n_parsed, bad = {}, 0, []
    for i, ln in enumerate(scratch.splitlines(), 1):
        if not ln.startswith("- claim: "):
            continue
        m = CLAIM_RE.match(ln)
        if m:
            n_parsed += 1
            findings[m.group("id")] = m.groupdict()
        else:
            bad.append(i)
    if bad:
        fails.append(("S2", f"scratchpad: {len(bad)} malformed of {n_parsed + len(bad)} "
                            f"claim lines (lines {bad[:10]})"))

    # S3: coverage Q-set == brief Q-set; every coverage status in enum
    cov_qids = set()
    covsec = section_lines(report, COV_RES)
    if covsec is None and not no_report:
        fails.append(("S3", "report: no '## Покрытие'/'## Coverage' section"))
    for ln in covsec or []:
        m = QLINE_RE.match(ln)
        if not m:
            continue
        cov_qids.add(qid := f"Q{m.group(1)}")
        words = m.group(2).strip().split()
        if not words or words[0].rstrip(".—,(") not in COV_STATUSES:
            fails.append(("S3", f"{qid}: invalid coverage status {m.group(2)!r}"))
    if covsec is not None and cov_qids != brief_qids and (cov_qids or brief_qids):
        fails.append(("S3", f"coverage Q-set != brief Q-set (missing {sorted(brief_qids - cov_qids)}, "
                            f"unexpected {sorted(cov_qids - brief_qids)})"))

    # S4: every conclusion bullet cites >=1 solid, existing evidence id
    conc = section_lines(report, CONC_RES)
    if conc is None and not no_report:
        fails.append(("S4", "report: no '## Выводы'/'## Conclusions' section"))
    elif conc is not None:
        if not conc:
            fails.append(("S4", "conclusions section has no bullets"))
        for ln in conc:
            ids = [int(x) for x in EREF_RE.findall(ln)]
            if not ids:
                fails.append(("S4", f"conclusion bullet without [E..]: {ln[:70]!r}"))
            for n in ids:
                d = findings.get(f"E{n}")
                if d is None:
                    fails.append(("S4", f"[E{n}] referenced in conclusions does not exist"))
                elif not (d["status"] in STATUS_BACKING and d["role"] == "evidence"
                          and d["retrieval"] in RETR_BACKING):
                    fails.append(("S4", f"[E{n}] not solid backing (status={d['status']} "
                                        f"role={d['role']} retrieval={d['retrieval']})"))

    # S5/S6: footer stop line; no overclaim phrases unless stop=saturation
    if not no_report:
        if not (m := STOP_RE.search(report)):
            fails.append(("S5", "report: footer 'stop: saturation|budget|round-cap' missing"))
        elif m.group(1) != "saturation":
            low = report.lower()
            if (hits := [p for p in FORBIDDEN if p in low]):
                fails.append(("S6", f"stop={m.group(1)} but report contains {hits}"))

    # S7: every [E..] token anywhere in report exists in scratchpad
    for n in sorted({int(x) for x in EREF_RE.findall(report)} - {int(i[1:]) for i in findings}):
        fails.append(("S7", f"[E{n}] in report has no scratchpad entry"))

    # A1: exact-duplicate normalized q strings among outcome:new lines
    seen, dupes = set(), []
    for m in QUERY_RE.finditer(queries):
        if m.group(2) == "new":
            norm = " ".join(m.group(1).lower().split())
            dupes.append(norm) if norm in seen else seen.add(norm)
    if dupes:
        advs.append(("A1", f"duplicate outcome:new queries: {sorted(set(dupes))}"))

    # A2: duplicate-URL ratio (>20% repeated) + STATS block
    urls = [d["url"] for d in findings.values() if d["url"] != "none"]
    uniq = set(urls)
    if urls and (len(urls) - len(uniq)) / len(urls) > 0.20:
        advs.append(("A2", f"duplicate URL ratio {len(urls) - len(uniq)}/{len(urls)} > 20%"))
    stats.append(f"parsed={n_parsed} malformed={len(bad)} findings={len(findings)} "
                 f"unique_urls={len(uniq)}/{len(urls)}")
    for field in ("status", "role", "retrieval"):
        stats.append(f"{field}: " + ", ".join(f"{k}={v}" for k, v in sorted(counts(findings, field).items())))
    for name in FILES:
        if text[name] is not None:
            stats.append(f"{name}: {len(extract_urls(text[name]))} https urls")

    # A3: schemeless-looking domains (the bare-domain verify_urls-skips trap)
    bare = set()
    for src in (scratch, "" if no_report else report):
        bare.update(BARE_DOMAIN_RE.findall(URL_RE.sub(" ", src)))
    if bare:
        advs.append(("A3", f"schemeless-looking domains: {sorted(bare)}"))

    # A4: thin synthesis over many findings
    if not no_report and n_parsed >= 5 and (words := len(report.split())) < 400:
        advs.append(("A4", f"report {words} words with {n_parsed} findings (<400)"))

    for name, detail in fails:
        print(f"FAIL: {name}: {detail}")
    for name, detail in advs:
        print(f"ADVISORY: {name}: {detail}")
    for line in stats:
        print(f"STATS: {line}")
    code = 2 if fails else (1 if advs else 0)
    print(f"{len(fails)} structural FAIL, {len(advs)} advisory")
    print(f"exit={code}")
    if as_json:
        print(json.dumps({"structural_fails": [list(f) for f in fails],
                          "advisories": [list(a) for a in advs], "exit": code}, ensure_ascii=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
