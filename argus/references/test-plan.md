# Argus test plan

Validation cases for the finalist NAS day (UGREEN iDX6011 Pro). All test data is synthetic.

## Core case 1 — Full audit on a messy folder

Dataset: a scope root with seeded content — exact duplicate files, one double-extension decoy (`report.pdf.exe`), one executable dropped into a documents folder, temp artifacts, loose files, and five nameless documents (invoices, a contract).

Steps: run `full-audit` on the scope → verify the plan lists the duplicate group, the two suspicious flags (R1, R2), storage findings, and a taxonomy proposal → approve a subset → confirm execution (moves to taxonomy, one quarantine) → verify `argus-journal.md`, `argus-undo.md`, and `steward-report.md` were written → run `revert` on one item.

Pass criteria: every executed item lands where the plan said; journal records before/after paths; health score computed; revert restores the item.

## Core case 2 — File-this on one document

Dataset: a single scanned invoice in an inbox folder.

Steps: run `file-this` on it → verify classification (`invoice`), extracted fields (date, issuer, total), proposed rename `YYYY-MM_invoice_issuer.ext` and destination → approve → verify the file lands renamed in `Documents/YYYY/Invoice/` and the journal entry exists.

Pass criteria: classification correct, rename convention applied, journal entry written.

## Edge case — Empty or first-run scope

Dataset A: an empty authorized folder. Dataset B: a populated scope with no `argus-journal.md` yet.

Steps A: run `full-audit` → expect a clean "empty result" report, no invented findings, no mutations. Steps B: run `what-changed` → expect "first run — no baseline" instead of a fabricated diff.

Pass criteria: graceful stop/empty handling in both, journal still records the run for B after a real audit.

## Procedure notes for the assigned day

1. Create the synthetic dataset first, then snapshot listing for before/after evidence.
2. Run core cases, then the edge case; keep the assistant transcript and file listings for the demo video.
3. Exercise the states at least once: decline the whole plan once (`cancelled` path), and leave one approval pending to show `waiting_approval`.
4. Back up journal and artifacts before credentials expire.
