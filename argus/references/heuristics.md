# Argus heuristics and scoring rubric

Deterministic rules applied over inventory metadata. Flags mean "worth a human look" — never confirmed malware. The same evidence always yields the same flag, which makes every verdict explainable and auditable.

## Suspicious-file rules

| ID | Rule (evidence over metadata) | Severity |
|---|---|---|
| R1 | Name matches a double extension whose final extension is executable (`*.pdf.exe`, `*.jpg.scr`, `*.docx.bat`, `*.xlsx.com`) | high |
| R2 | Executable extension (`exe`, `bat`, `cmd`, `com`, `scr`, `msi`, `ps1`, `vbs`, `js`, `wsf`, `dll`) inside a folder whose majority type is documents or media | high |
| R3 | Declared extension disagrees with the file header bytes (e.g., `*.jpg` whose first bytes are a program or archive signature) | high |
| R4 | Zero-byte payload (`size = 0`) outside configuration conventions | medium |
| R5 | Size grossly anomalous for declared type (a `*.txt` over 100 MB, a `*.pdf` over 500 MB) | medium |
| R6 | Extension on a platform watchlist (`.lnk`, `.url`, `.hta`, `.iso` inside user folders) | medium |
| R7 | Hidden-looking or confusable names (leading dot on a regular document, double spaces, look-alike characters) | low |
| R8 | Recently created executable whose neighbors are all older data files | medium |

Handling: R1–R3 and R8 propose quarantine (move to the scope quarantine directory, never delete). R4–R7 propose review lines in the plan. Every flag carries rule id, path, and the evidence that fired it.

## Duplicate handling

- Exact duplicates (same content hash): keep the recommended best version, propose archive for the rest.
- Best version for media: highest resolution, then original capture timestamp, then richest metadata.
- The native deduplication plan (`file-workflow`, `kind=deduplication`, `keep-by latest|oldest`) is offered when the user prefers the platform engine.

## Document classes (Phase 6)

`invoice`, `contract`, `receipt`, `letter`, `statement`, `other`. Extraction fields: `date`, `issuer`, `total`. Proposed rename convention: `YYYY-MM_class_issuer.ext` (sanitized). Documents that fail text parsing are routed to the photo expert for OCR, then reclassified once.

## Health score rubric (0–100)

Start at 100, then subtract, floor at 0:

| Finding | Points off |
|---|---|
| Per high-severity flag (R1–R3, R8) | −15, capped at −45 |
| Per medium-severity flag (R4–R6) | −5, capped at −20 |
| Duplicate groups present | −2 each, capped at −15 |
| Loose/unclassified files over 20% of inventory | −10 |
| Storage reclaimable over 20% of scope size | −10 |
| Documents without a taxonomy home over 30% of documents | −10 |
| Prior journal entry older than the retention threshold | −5 |

Bonus back: +5 if the previous run exists and findings decreased. The rubric is deterministic: identical findings always produce the same score, and the journal stores score history for the `what-changed` trend line.

## Confidence rule

When a phase cannot reach high confidence (unparsable document, unreadable metadata, ambiguous class), the item is placed in the plan's "review" group instead of any action group. Low confidence never becomes an automatic mutation.
