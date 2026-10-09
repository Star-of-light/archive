#!/usr/bin/env python3
"""Collaboration report — Part C (12 marks).

GIVEN. Do not edit. This runs in CI on every push and prints the same report
your teacher reads. Run it yourself any time:

    python tools/check_collaboration.py

It reads your git history. It cannot be satisfied by anything except actually
working the way the assignment asks: both partners committing, work arriving
on branches through merges, and at least one real conflict resolved together.
"""

import re
import subprocess
import sys


def sh(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()


def rule(title):
    print()
    print(title)
    print("-" * len(title))


def verdict(ok, got, need):
    mark = "PASS" if ok else "FAIL"
    print(f"  [{mark}]  {got}   (need: {need})")
    return ok


def main():
    print("=" * 62)
    print("  THE ARCHIVE — COLLABORATION REPORT")
    print("=" * 62)

    # ---------------------------------------------------- authors
    rule("1. Both partners committing (3 marks)")
    shortlog = sh("git shortlog -sne --all")
    authors = [line.strip() for line in shortlog.splitlines() if line.strip()]
    counts = []
    for line in authors:
        m = re.match(r"(\d+)\s+(.*)", line)
        if m:
            counts.append((int(m.group(1)), m.group(2)))
            print(f"         {m.group(1):>3}  {m.group(2)}")
    both = len(counts) >= 2 and all(n >= 6 for n, _ in sorted(counts)[:2])
    ok_authors = verdict(
        both,
        f"{len(counts)} author(s), lowest has {min([n for n, _ in counts]) if counts else 0} commits",
        "2 authors, >= 6 commits each",
    )

    # ---------------------------------------------------- main is protected
    rule("2. Nothing committed straight to main (2 marks)")
    direct = [x for x in sh(
        "git log --first-parent main --no-merges --pretty=%h"
    ).splitlines() if x]
    ok_direct = verdict(
        len(direct) <= 1,
        f"{len(direct)} non-merge commit(s) on main's first-parent line",
        "<= 1 (the initial commit only)",
    )

    # ---------------------------------------------------- branches
    rule("3. Feature branches (2 marks)")
    all_subjects = sh("git log --all --pretty=%s")
    branches = sorted(set(re.findall(r"(?:feature|fix)/[\w.-]+", all_subjects)))
    for b in branches:
        print(f"         {b}")
    ok_branches = verdict(
        len(branches) >= 4,
        f"{len(branches)} feature/fix branch name(s) seen in history",
        ">= 4",
    )

    # ---------------------------------------------------- merges
    rule("4. Work arrives by merge (part of 2 marks above)")
    merges = [x for x in sh("git log --merges --pretty=%h").splitlines() if x]
    print(f"         {len(merges)} merge commit(s)")

    # ---------------------------------------------------- conflict resolved
    rule("5. A real merge conflict, resolved (2 marks)")
    conflicted = 0
    for h in merges:
        # A merge whose result differs from both parents on a shared file is
        # evidence the merge was not a fast-forward and needed a decision.
        diff_p1 = sh(f"git diff --name-only {h}^1 {h}")
        diff_p2 = sh(f"git diff --name-only {h}^2 {h}")
        shared = set(diff_p1.splitlines()) & set(diff_p2.splitlines())
        shared.discard("")
        if shared:
            conflicted += 1
            print(f"         {h}  touched both sides: {', '.join(sorted(shared))}")
    ok_conflict = verdict(
        conflicted >= 1,
        f"{conflicted} merge(s) show a genuine two-sided resolution",
        ">= 1",
    )

    # ---------------------------------------------------- messages
    rule("6. Commit messages (3 marks — teacher spot-check)")
    lazy = re.compile(
        r"^\s*(update|updates|changes?|stuff|fix|fixes|wip|asdf|test|final|.)\s*$",
        re.IGNORECASE,
    )
    subjects = [s for s in sh("git log --pretty=%s --no-merges").splitlines() if s]
    weak = [s for s in subjects if lazy.match(s)]
    print(f"         {len(subjects)} commit message(s), {len(weak)} look(s) lazy")
    for s in weak[:5]:
        print(f"         weak: {s!r}")
    if not weak:
        print("         no obviously lazy messages found")

    # ---------------------------------------------------- summary
    print()
    print("=" * 62)
    passed = sum([ok_authors, ok_direct, ok_branches, ok_conflict])
    print(f"  {passed}/4 automated checks passing")
    if passed < 4:
        print("  Not there yet — see the FAILs above. This is fixable by")
        print("  working the way the brief asks, and by nothing else.")
    else:
        print("  On track. Messages are still marked by a human.")
    print("=" * 62)

    # Never fail the build — this is a report, not a gate.
    return 0


if __name__ == "__main__":
    sys.exit(main())
