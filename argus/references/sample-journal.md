# Sample run — worked example

A complete Argus `full-audit` over the synthetic fixture `messy-scope/` (the same corpus in `test-data/`). Shows exactly what the user sees and what the state files contain. All filenames are synthetic.

## Input

User: "Argus, full audit of my Downloads test scope." First run — no journal, no preferences.

## Conversation excerpt

```text
Argus: Scanning messy-scope — 16 files inventoried (first run, no baseline).

Findings
- duplicates: 1 group — photo-2024-beach.jpg appears 3 times (incl. " copy" and backup/)
- suspicious: 3 flags — R1 report.pdf.exe (high), R2 Documents/runme.exe (high), R4 empty.bin (medium)
- storage: file.tmp + movie-download.part reclaimable (~1.2 GB)
- disorganization: 12 loose files at root (75% of scope)
- documents: 5 classified (invoice-001, contract-nda, receipt-store, statement-bank, letter-personal)

Action plan — 7 items
1. quarantine  report.pdf.exe → quarantine/           [R1, high]
2. quarantine  Documents/runme.exe → quarantine/      [R2, high]
3. review      empty.bin — zero-byte payload          [R4, needs you]
4. archive     photo-2024-beach copy.jpg, backup/…   keep highest-res original
5. archive     file.tmp, movie-download.part          [temp/orphaned]
6. file        5 documents → Documents/2026/class/    + rename YYYY-MM_class_issuer
7. tag         filed documents: finance, legal, personal

approve: all / ranges / categories / none

You: approve 1-2, 4-6 — skip 3 and 7

Argus: Executed 5/7. Skipped: item 3 (declined), item 7 (declined).
Journal entry written. Health score: 53.
```

## argus-journal.md — resulting entry

```text
## 2026-11-06 14:32 — mode: full-audit — run 001
scope: messy-scope
watchlist honored: none (no preferences file — defaults used)
findings: duplicates 1 group / suspicious 3 (2 high, 1 medium) / storage 2 items / loose 12 files / documents 5 classified
actions executed: quarantined 2, archived 3, moved 5
actions declined: 2 (items 3, 7)
pending review: item 3 — empty.bin (R4, medium)
health score: 53 (first run — no baseline)
undo manifest: argus-undo.md run 001
```

## argus-undo.md — resulting manifest

```text
run: 001 — 2026-11-06 14:32
moves:
- dst: quarantine/report.pdf.exe | src: messy-scope/report.pdf.exe
- dst: quarantine/runme.exe | src: messy-scope/Documents/runme.exe
- dst: archive/dupes/photo-2024-beach copy.jpg | src: messy-scope/photo-2024-beach copy.jpg
- dst: archive/dupes/photo-2024-beach.jpg | src: messy-scope/backup/photo-2024-beach.jpg
- dst: archive/tmp/file.tmp | src: messy-scope/file.tmp
- dst: archive/tmp/movie-download.part | src: messy-scope/movie-download.part
- dst: Documents/2026/Invoice/2026-04_invoice_acme.txt | src: messy-scope/invoice-001.txt
- dst: Documents/2026/Contract/2026-01_contract_nda.txt | src: messy-scope/contract-nda.txt
- dst: Documents/2026/Receipt/2026-02_receipt_store.txt | src: messy-scope/receipt-store.txt
- dst: Documents/2026/Statement/2026-03_statement_bank.txt | src: messy-scope/statement-bank.txt
- dst: Documents/2026/Letter/2026-05_letter_personal.txt | src: messy-scope/letter-personal.txt
renames: (folded into moves)
tags: none applied (item 7 declined)
notes: nothing was deleted; quarantine holds flags pending user decision
```

## steward-report.md — resulting dashboard

```text
# Steward report — messy-scope
last audit: 2026-11-06 · health score: 53 (first run)
pending review: 1 item (empty.bin) · quarantined: 2 · duplicates archived: 2
storage reclaimed: ~1.2 GB pending user confirmation of archives
recommended next audit: +30 days — run `what-changed` for a quick diff anytime
```

## Health score walkthrough (rubric from heuristics.md)

```text
start:                                100
R1 report.pdf.exe      (high)         −15
R2 Documents/runme.exe (high)         −15
R4 empty.bin           (medium)        −5
duplicate groups ×1                    −2
loose files 75% > 20% threshold       −10
storage reclaimable < 20% of scope     −0
documents unclassified < 30%           −0
prior journal: none (first run)        −0
bonus: n/a (no previous run)           −0
                                      ───
score                                   53
```

Deterministic: the same findings always produce 53. After execution, the *next* run rescans the cleaner scope — quarantined flags stop counting against the score, archived dupes drop the group count, and the loose-files term disappears — so the score trends upward and the trend line in the dashboard becomes real evidence of improvement.
