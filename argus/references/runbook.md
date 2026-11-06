# Argus operational runbook

Per-phase execution contract for the steward workflow. Read this when changing delegation logic, adding phases, or debugging a run. The user-facing workflow lives in `SKILL.md`; this file is the operational detail behind it.

## Global delegation rules

- **Result passing**: the parent passes only the real result of a completed delegation into dependent phases. A phase never receives fabricated, cached-from-memory, or best-guess data.
- **Status handling**: every delegated step is tracked as `completed`, `failed`, `cancelled`, `waiting_user`, or `waiting_approval`. Only `completed` produces a business result that may flow downstream.
- **Approval gate**: phases 0–6 are read-only and always run (after scope confirmation). Phases 7–9 mutate state and run only for plan items the user explicitly approved.
- **Bounded runs**: inventory and document sampling honor listing limits and the configured sample cap; large scopes are paginated rather than truncated silently.
- **Scope discipline**: no phase ever widens the confirmed scope, touches watchlist paths, or reads outside the authorized roots.
- **Dependency rule**: a phase whose required upstream result is missing or empty stops cleanly and reports which prerequisite was unavailable; it does not improvise.

## Phase cards

### Phase 0 — Load steward state

- **Target**: `file-agent`
- **Reads**: `argus-preferences.md`, `argus-journal.md` (newest entry), `argus-undo.md` (latest manifest) inside each confirmed scope root.
- **Expected**: verbatim contents, or an explicit list of which files are absent.
- **Absent preferences** → run with defaults and no watchlist; record "no preferences" in the journal. **Absent journal** → first run; `what-changed` degrades to "no baseline".
- **Failure**: if a state file exists but is unreadable, treat as present-but-corrupt, warn the user, and do not overwrite it during this run.

### Phase 1 — Inventory

- **Target**: `file-agent`
- **Input**: confirmed scope paths, watchlist exclusions.
- **Expected**: recursive listing with path, size, timestamps, type per entry; or an empty result with reason.
- **Downstream**: every later phase consumes this inventory — they do not re-scan.
- **Failure**: unreadable subtrees are reported as partial inventory with the unreadable paths listed; the run continues on the readable remainder and says so.

### Phase 2 — Duplicates

- **Target**: `file-agent`
- **Input**: the real inventory.
- **Expected**: duplicate groups keyed by content hash, each with a recommended keeper (media groups ranked by resolution, then capture timestamp, then metadata richness).
- **Optional**: if the user prefers the platform engine, offer the native deduplication plan (`file-workflow`, `kind=deduplication`) and surface its plan for approval instead of Argus's own moves.
- **Empty result**: "no duplicates found" is a valid result, reported as such.

### Phase 3 — Suspicious-pattern sweep

- **Target**: `file-agent`
- **Input**: the real inventory plus the rule set in [heuristics](heuristics.md) (R1–R8).
- **Expected**: flag lines carrying rule id, path, and the exact evidence that fired; or an empty result.
- **Language**: output always says "flagged for review", never "infected" or "malware".
- **Downstream**: high-severity flags become quarantine proposals; medium and low become review lines in the plan.

### Phase 4 — Storage health

- **Target**: `file-agent`
- **Expected**: three profiles — largest files/directories, temporary and orphaned artifacts (partial downloads, thumbnail databases, caches), untouched-beyond-threshold files — each with reclaimable-space estimates.
- **Threshold**: the retention window comes from preferences (default 24 months).

### Phase 5 — Disorganization

- **Target**: `file-agent`
- **Expected**: findings for loose root files, flat accumulations, non-conforming names, empty directories; plus a proposed `Documents/YYYY/class` taxonomy mapping.
- **Downstream**: feeds plan items and the unclassified-files term of the health score.

### Phase 6 — Document hygiene

- **Target**: `document-agent`; fallback `photo-agent` for scans that fail text parsing.
- **Expected**: class (invoice / contract / receipt / letter / statement / other) plus `date`, `issuer`, `total` where present; honors the sample cap from preferences.
- **Honesty rule**: unparsable documents are reported as "could not be parsed" and land in the review bucket — never guessed.

### Phase 7 — Numbered action plan

- **Owner**: parent (no delegation).
- **Expected**: one numbered plan grouped by category — id, action, file, origin → destination, reason, severity/confidence. Review-bucket items are listed separately.
- **Gate**: the run pauses here. Approval grammar (all / ranges / categories / review-only) is defined in [conversation protocol](conversation-protocol.md).

### Phase 8 — Confirmed execution

- **Target**: `file-agent` (moves, renames, then tags).
- **Expected**: per-item result — `moved`, `renamed`, `tagged`, or `not executed` with reason.
- **Ordering**: destination directories are created before any move; flagged items go only to `quarantine/`; name collisions get a numeric suffix and are reported.
- **Partial execution**: the journal records exactly which items ran and which did not; nothing is retried silently.

### Phase 9 — Journal, dashboard, undo

- **Targets**: `file-agent` (writes `argus-journal.md`, `argus-undo.md`, `steward-report.md`) and `knowledge-agent` (stores the run digest).
- **Expected**: the three state files updated per [journal format](journal-format.md), plus the knowledge record reference.
- **Ordering**: written after execution so every recorded action reflects reality.

## Revert contract

`revert` is two-phase: first a verification pass (every destination still exists, every source still free) producing a per-item revert plan, then execution of the approved inverse moves only. Items that fail verification are reported as non-revertible with the reason — never force-moved over existing content. A revert writes its own journal entry, keeping the audit trail append-only.
