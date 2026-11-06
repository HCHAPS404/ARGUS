# Argus edge-case catalog

How Argus behaves when things are not normal. Every entry names the trigger and the required behavior; the principle behind all of them is the same — preserve evidence, report honestly, never improvise.

## Scope and input problems

| Case | Expected behavior |
|---|---|
| Scope does not exist | Report "path not found"; ask once for a corrected scope; stop without touching anything. |
| Scope is empty | Report an empty result with reason; journal the run as a clean first pass; score 100. |
| Scope is entirely watchlisted | Refuse politely: explain the watchlist excludes everything; ask whether to update `prefs`. |
| User supplies a file path instead of a folder | Accept it as a one-item scope or route to `file-this`; never climb into the parent folder silently. |
| Nested/overlapping scopes | Merge into the smallest set of disjoint roots before inventory; report the merge. |
| Symlinked or shortcut entries inside scope | Treat link targets outside the scope as out of bounds; report them, never follow them. |

## First-run and state problems

| Case | Expected behavior |
|---|---|
| First run (no journal) | Say "no baseline"; skip diff terms; write the initial entry normally. |
| Journal exists but is unreadable or truncated | Warn that the baseline is corrupt; run as first run **without** overwriting the corrupt file; note it in the new entry. |
| Preferences file malformed | Ignore malformed lines, honor the valid ones, list the ignored lines for the user. |
| Undo manifest missing for `revert` | Report that nothing is recorded as revertible; suggest `what-changed` instead. |

## Execution problems

| Case | Expected behavior |
|---|---|
| Name collision at destination | Append a numeric suffix (`-1`, `-2`), record both names in the journal and undo manifest. |
| Item moved/deleted between plan and approval | Mark the item `not executed — no longer at source`; continue with remaining approved items. |
| Destination occupied during `revert` | Mark that item non-revertible with the reason; complete the rest; never overwrite. |
| File locked or in use | Report `not executed — locked`; keep the item pending in the journal for a future run. |
| Permission denied mid-run | Report the failed items with the reason; preserve all completed partial results. |
| User cancels mid-execution | Stop immediately; journal what completed; the partial manifest stays valid for `revert`. |
| All plan items rejected | Journal a run with zero actions; the audit findings still stand as the report. |

## Scale problems

| Case | Expected behavior |
|---|---|
| Inventory exceeds listing limit | Paginate; report total and coverage ("4,210 of ~6,000 files inventoried"). |
| Document set exceeds sample cap | Classify up to the cap chosen deterministically (largest-first or newest-first); report coverage and offer a follow-up pass. |
| Duplicate groups very large | Group fully, but present the plan paginated by group; approval grammar accepts ranges and categories. |
| Hundreds of plan items | Batch the plan by category; ask the user to approve per category rather than per line. |

## Evidence problems

| Case | Expected behavior |
|---|---|
| Metadata field unavailable | Downgrade affected rules to "not evaluated" and say so; never substitute a guess. |
| Header bytes unreadable | R3 does not fire on that file; report "signature not evaluated". |
| Classifier confidence low | Item goes to the review bucket of the plan; it is never auto-moved. |
| Conflicting signals (benign name + suspicious header) | The higher-severity rule wins; both evidence lines are shown. |

## Interaction problems

| Case | Expected behavior |
|---|---|
| Approval reply is ambiguous | Ask once for clarification using the numbered ids; do not interpret loosely. |
| Expert returns `waiting_user` mid-phase | Relay the question verbatim; resume only after the user answers. |
| User asks for an out-of-scope action | Decline and restate the confirmed scope; offer to re-confirm scope explicitly. |
| User requests "delete the duplicates" | Propose the reversible archive alternative; deletion happens only if the user insists after the risk warning, and is still journaled. |
