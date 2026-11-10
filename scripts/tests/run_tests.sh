#!/usr/bin/env bash
# Offline test suite for ledger_lint.py — asserts exit codes + FAIL/ADVISORY tags per fixture.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LINT="$HERE/../ledger_lint.py"
FIX="$HERE/fixtures"
PASS=0; FAIL=0

run_case() { # name expected_exit [grep-pattern...]
  local name="$1" want="$2"; shift 2
  local out rc
  out="$(python3 "$LINT" "$FIX/$name" 2>&1)"; rc=$?
  local ok=1
  if [ "$rc" -ne "$want" ]; then
    echo "FAIL [$name]: expected exit=$want got exit=$rc"; ok=0
  fi
  local pat
  for pat in "$@"; do
    if ! printf '%s\n' "$out" | grep -qF -- "$pat"; then
      echo "FAIL [$name]: stdout missing: $pat"; ok=0
    fi
  done
  if [ "$ok" -eq 1 ]; then echo "PASS [$name] exit=$rc"; PASS=$((PASS+1));
  else echo "$out" | sed 's/^/    | /'; FAIL=$((FAIL+1)); fi
}

run_case good                0 "0 structural FAIL, 0 advisory" "exit=0" \
                             "STATS: scratchpad.md: 5 https urls"
run_case advisory            1 "ADVISORY: A1" "ADVISORY: A3" "github.com" \
                             "STATS: scratchpad.md: 5 https urls" "exit=1"
run_case broken-schema       2 "FAIL: S1" "FAIL: S2" "exit=2"
run_case bad-status          2 "FAIL: S3" "FAIL: S5" "exit=2"
run_case coverage-mismatch   2 "FAIL: S3" "exit=2"
run_case unbacked-conclusion 2 "FAIL: S4" "FAIL: S7" "exit=2"
run_case budget-exhaustive   2 "FAIL: S6" "exit=2"

# extract_urls sanity: bare github.com/foo/bar in a scratchpad claim must trigger A3
# while the https URLs of the same file are still counted in STATS (see advisory case).
if grep -q 'github.com/foo/bar' "$FIX/advisory/scratchpad.md"; then
  echo "PASS [extract-urls-bare-domain] bare domain present in advisory fixture"; PASS=$((PASS+1))
else
  echo "FAIL [extract-urls-bare-domain] bare domain missing from advisory fixture"; FAIL=$((FAIL+1))
fi

echo "----"
echo "suite: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
