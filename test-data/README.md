# Synthetic test data

For the finalist NAS day only — never contains real personal data. `messy-scope/` is the dirty folder for Core test 1 (see `argus/references/test-plan.md`).

Seeded findings:

| File | Expected flag |
|---|---|
| `report.pdf.exe` | R1 — double extension, executable tail (high) |
| `Documents/runme.exe` | R2 — executable inside a documents folder (high) |
| `holiday.jpg` (MZ bytes inside) | R3 — extension disagrees with header bytes (high) |
| `empty.bin` | R4 — zero-byte (medium) |
| `.DS_Store`, `Thumbs.db`, `file.tmp`, `movie-download.part` | temp/orphan artifacts |
| `photo-2024-beach.jpg` × 3 (incl. `backup/` copy) | exact duplicate group |
| 5 unclassified docs (`invoice-001`, `contract-nda`, `receipt-store`, `letter-personal`, `statement-bank`) | Phase 6 classification + rename proposals |
| `inbox/scan-iberdrola-april.txt` | Core test 2 (`file-this`) |

On the NAS day: copy `messy-scope/` into an authorized folder, snapshot a before-listing, run `full-audit`, approve a subset, verify journal/undo/dashboard, revert one item. For a real OCR check, swap the `.txt` stand-ins for actual scanned images of the same synthetic documents.
