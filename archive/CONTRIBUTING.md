# How we work in this repository

These are the rules of this repo. They are also 25 of the 100 marks
(Parts C and D), so read them once properly.

---

## 1. Never commit to `main`

`main` is the version that works. It changes only when a reviewed branch is
merged into it.

```bash
git checkout main
git pull
git checkout -b feature/validate-year
```

Branch names: `feature/what-it-adds` or `fix/what-it-repairs`.
Use hyphens, be specific. `feature/stuff` is not a branch name.

## 2. Commit messages say WHY, not WHAT

Git already records what changed — you do not need to repeat it. What it
cannot record is the reason.

| No | Yes |
|---|---|
| `update` | `Reject whitespace-only titles so blank entries stop loading` |
| `fixed stuff` | `Make city comparison case-insensitive — volunteers type lower case` |
| `validation.py` | `Use >= at both year bounds so 1100 and 1900 are accepted` |
| `asdf` | anything at all |

In six months you will read your own history as a stranger. Write for them.

## 3. Every change arrives by pull request

```bash
git push -u origin feature/validate-year
```

Then open a PR on GitHub. In the description say what it does and what you
are unsure about.

## 4. Your partner reviews before it merges

You may not merge your own PR unreviewed, and your partner may not approve a
PR they have not read. Use the frames from Week 1:

> **I notice** `validate_city` compares with `==`.
> **I wonder** what happens when a volunteer types `timbuktu`.
> **I suggest** lowering the case on both sides before comparing.

A review that says "looks good" scores zero for Part D. A review that finds
a real bug is worth more to your mark *and* your grade in Part A, because
the hidden tests will find that bug if you do not.

## 5. Respond to reviews with commits, not arguments

When your partner's review lands, push a follow-up commit to the same branch
that answers it. Part D explicitly awards 3 marks for a review that changed
something.

## 6. Conflicts are normal

If you both edit `validation.py`, git will stop and ask which version you
want. It is not an error and you have not broken anything — it is the tool
refusing to guess. Resolve it **together**, out loud, and let the better
argument win.

You need at least one genuine conflict in your history. You will almost
certainly get one without trying.

---

## The daily loop

```bash
git checkout main && git pull          # start from what works
git checkout -b feature/thing          # your own lane
# ... write code, run pytest ...
git add -A
git commit -m "Why this change exists"
git push -u origin feature/thing       # open the PR
# ... partner reviews, you respond with another commit ...
# ... merge on GitHub ...
git checkout main && git pull          # pick up the merged work
```

## Before you push, always

```bash
pytest -v
python tools/check_collaboration.py
```
