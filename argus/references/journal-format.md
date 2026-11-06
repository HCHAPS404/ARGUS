# Journal and state-file formats

All Argus state lives inside the audited scope root as plain Markdown files the user can read. A run writes at most: `argus-journal.md` (append-only), `argus-undo.md` (rewritten), `steward-report.md` (rewritten), `argus-preferences.md` (user-editable), and the `quarantine/` directory when flags are executed.

## argus-journal.md — append-only entries

One entry per run:

```text
## YYYY-MM-DD HH:mm — mode: full-audit — run 003
scope: <scope paths>
watchlist honored: <paths excluded>
findings: duplicates 4 groups / suspicious 2 (1 high, 1 medium) / storage 3 categories / loose 12 files / documents 5 classified
actions executed: moved 9, renamed 5, quarantined 1, tagged 4
actions declined: 3
pending review: items 14, 15 (low confidence)
health score: 82 (previous 71)
undo manifest: argus-undo.md run 003
```

## argus-undo.md — latest run's mutation manifest

```text
run: 003 — YYYY-MM-DD HH:mm
moves:
- dst: Documents/2026/Invoice/acme-march.pdf | src: Downloads/scan0013.pdf
- dst: quarantine/setup-pdf.exe | src: Downloads/setup-pdf.exe
renames:
- old: Documents/2026/Invoice/acme-march.pdf | new: Documents/2026/Invoice/2026-03_invoice_acme_812eur.pdf
tags:
- file: Documents/2026/Invoice/2026-03_invoice_acme_812eur.pdf | tag: finance
notes: collisions suffixed -1 where listed; nothing was deleted
```

`revert` reads this manifest, verifies each destination exists and each source is free, presents the inverse plan for approval, executes approved inverse moves, then appends a `revert` entry to the journal.

## argus-preferences.md — standing rules

```text
watchlist (never touch):
- Family Photos
- Legal/Originals
naming: YYYY-MM_class_issuer
retention months: 24
never suggest:
- archiving contracts
- quarantining files under Dev/
sample cap for document classification: 40
```

## steward-report.md — living dashboard

```text
# Steward report — <scope>
last audit: YYYY-MM-DD · health score: 82 (trend: 71 → 78 → 82)
pending review: 2 items · quarantined: 1 · duplicates archived: 12
recommended next audit: +30 days
```

## Diff rules (`what-changed`)

Compare a fresh shallow inventory against the newest journal entry: report files added, removed, and modified since that entry timestamp, plus score trend. A missing or unreadable journal entry degrades to "first run — no baseline", never to an invented comparison.
