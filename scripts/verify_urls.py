#!/usr/bin/env python3
"""Verify URLs in a research report / findings file (pipeline step 10, zero-LLM).

Usage:
    verify_urls.py REPORT.md [MORE_FILES...]   # or: echo "https://..." | verify_urls.py

Extracts all http(s) URLs, checks each once via `curl -sI` (HEAD, browser UA,
15s timeout; falls back to GET for 405/501). Prints one line per URL:
    OK <status>      2xx/3xx after redirects
    RESTRICTED <st>  401/403 — anti-bot, NOT dead, keep the link
    DEAD <st>        404/410, or unresolvable host
    TRANSIENT <st>   429/5xx — retry later, no hammering
    TIMEOUT          no response within 15s
    ERR <reason>     curl-level failure

Exit code: 0 if every URL is OK/RESTRICTED/TRANSIENT; 1 if any DEAD/TIMEOUT/ERR
(unverifiable links are as dangerous as dead ones before delivery).
"""
import re
import subprocess
import sys

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
URL_RE = re.compile(r"https?://[^\s\)>\]\"'`]+")
DEAD_STATUS = {404, 410}
RESTRICTED_STATUS = {401, 403}


def extract_urls(text):
    urls, seen = [], set()
    for raw in URL_RE.findall(text):
        u = raw.rstrip(".,;:!?")
        if u not in seen:
            seen.add(u)
            urls.append(u)
    return urls


def _curl(url, head):
    args = ["curl", "-s", "--max-time", "15", "-A", UA]
    args += ["-I", "-L"] if head else ["-o", "/dev/null", "-L"]
    args.append(url)
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=25)
    except subprocess.TimeoutExpired:
        return None, "timeout", 28
    status = None
    for line in (p.stdout or "").splitlines():
        m = re.match(r"HTTP/[\d.]+\s+(\d{3})", line.strip())
        if m:
            status = int(m.group(1))  # last line = final after redirects
    err_text = (p.stderr or "") + "\n" + (p.stdout or "")
    err = err_text.strip().splitlines()[-1] if err_text.strip() else None
    return status, err, p.returncode


def check(url):
    status, err, rc = _curl(url, head=True)
    if status in (405, 501):  # some hosts reject HEAD
        status, err, rc = _curl(url, head=False)
    if status is None:
        if rc in (6, 7):  # could not resolve / could not connect
            return "DEAD", "unresolvable host"
        if err == "timeout":
            return "TIMEOUT", "no response in 15s"
        return "ERR", err or "no HTTP status"
    if 200 <= status < 400:
        return "OK", status
    if status in DEAD_STATUS:
        return "DEAD", status
    if status in RESTRICTED_STATUS:
        return "RESTRICTED", status
    if status >= 429:
        return "TRANSIENT", status
    return "HTTP", status


def main():
    text = ""
    for path in sys.argv[1:]:
        with open(path, encoding="utf-8", errors="replace") as f:
            text += f.read() + "\n"
    if not sys.argv[1:]:
        text = sys.stdin.read()

    urls = extract_urls(text)
    if not urls:
        print("no URLs found")
        return 0

    bad = 0
    for u in urls:
        verdict, detail = check(u)
        if verdict in ("DEAD", "TIMEOUT", "ERR"):
            bad += 1
        print(f"{verdict} {detail}\t{u}")
    print(f"\n{len(urls)} URLs checked, {bad} dead/unverifiable")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())