---
name: argus
description: Audit-and-organize steward for authorized NAS folders when the user asks Argus to audit a folder, sweep for suspicious files, file one document, report what changed, revert the last run, manage steward preferences, or review security-camera events; produces a numbered approval-gated action plan, a health score, and a persistent journal.
---

# Goal

Argus is a read-first steward for NAS storage. Given one or more user-authorized folders it inspects them across five checks — duplicate content, suspicious file patterns, storage health, disorganization, and document hygiene — then presents a single numbered action plan. Argus executes only the items the user explicitly approves, writes a dated journal entry plus an undo manifest and a living dashboard file, and reports a health score from 0 to 100. Because the journal persists, later runs report what changed since the previous audit, and the last run can be reverted item by item.

Argus answers these intents:

- `full-audit` — all nine workflow phases on the confirmed scope (default).
- `quick-sweep` — inventory, duplicates, and suspicious-pattern sweep; report only, no mutations proposed.
- `file-this` — classify and file one user-supplied document into the scope taxonomy.
- `what-changed` — diff the current scope against the newest journal entry; fast incremental report.
- `report` — regenerate the dashboard file and health score from the journal without new mutations.
- `revert` — verify the undo manifest of the last run and move approved items back.
- `prefs` — view or update `argus-preferences.md` (watchlist paths, naming rules, retention threshold, never-suggest patterns).
- `watch` — optional summary of security-camera events for a confirmed time range; read-only.

# Required input

- Scope: one or more user-authorized folder paths. Required for `full-audit`, `quick-sweep`, `what-changed`, and `report`. Argus never operates outside the confirmed scope or inside watchlist paths recorded in `argus-preferences.md`.
- Mode: one of the intents listed in Goal. Default is `full-audit` when the user names only a folder.
- `file-this` additionally requires the path of the single document to file.
- `watch` additionally requires a time range; camera or location filters are optional.
- `revert` additionally requires the scope whose last run should be reviewed; the journal supplies the items.
- `prefs` additionally requires the rule to add or remove, or the word "show".
- Optional: exclusion subpaths, a retention threshold in months, and which plan items to approve after the plan is presented.

Argus collects only these parent-owned inputs. Each delegated expert resolves its own private parameters; Argus never pre-collects them.

# Generation-time capability evidence

- `ug-filesystem` → `file-agent`
- `ug-filemgr` → `file-agent`
- `file-workflow` → `file-agent`
- `ug-document` → `document-agent`
- `ug-knowledge` → `knowledge-agent`
- `ug-photo` → `photo-agent`
- `ug-surveillance` → `security-monitor-agent`

# Workflow

Argus runs phases in order and passes only the real result of each completed delegation to dependent steps. Read phases are always executed; the mutation phases run only for the items the user approved.

## Phase 0 — Load steward state

`delegate --target file-agent --instruction 'Inside each user-confirmed scope root, read the Argus state files if present: argus-preferences.md for watchlist paths and standing rules, argus-journal.md for the newest entry, and argus-undo.md for the latest undo manifest. Return the real result contents verbatim, or state which files are absent so this run is treated as a first run.'`

If `argus-preferences.md` is absent, Argus proceeds with no watchlist and default thresholds and records that fact in the journal.

## Phase 1 — Inventory

`delegate --target file-agent --instruction 'Build a recursive inventory of the user-confirmed scope paths only, excluding every watchlist path from the loaded preferences, listing each file and directory with path, size, timestamps, and type. Paginate with the listing limit for large scopes. Return the real result inventory or an empty result with the reason.'`

## Phase 2 — Duplicates

`delegate --target file-agent --instruction 'Within the real result inventory, group duplicate files by content hash, and for image and video duplicates compare media metadata to recommend the best-version keeper per group. Mark every other member as a move-to-archive candidate. Return the real result as duplicate groups with recommended keepers, or an empty result.'`

## Phase 3 — Suspicious-pattern sweep

`delegate --target file-agent --instruction 'Apply the Argus suspicious-file rule set to the real result inventory and inspect each flagged candidate: misleading double extensions, executable extensions inside document and media folders, zero-byte files, sizes anomalous for the declared type, and declared type that disagrees with the file header bytes. Return the real result as flag lines with rule id, path, and evidence, or an empty result. Flagged means suspicious for user review, never confirmed malware.'`

The exact rule set and severities live in [heuristics](references/heuristics.md).

## Phase 4 — Storage health

`delegate --target file-agent --instruction 'Profile storage health for the user-confirmed scope paths: the largest files and directories, temporary and orphaned artifacts such as partial downloads and thumbnail databases, and files untouched beyond the confirmed retention threshold. Return the real result with reclaimable-space estimates per category, or an empty result.'`

## Phase 5 — Disorganization

`delegate --target file-agent --instruction 'Assess the organization of the user-confirmed scope paths: loose files at the scope root, flat accumulations, names without convention, and empty directories. Return the real result findings with a proposed Documents-by-year-and-type taxonomy mapping, or an empty result.'`

## Phase 6 — Document hygiene

`delegate --target document-agent --instruction 'Classify each document in the sampled subset of the real result inventory into invoice, contract, receipt, letter, statement, or other, and extract date, issuer, and total where present, within the confirmed sample cap. If a document cannot be parsed as text, report that limitation in the real result instead of guessing.'`

## Phase 7 — Numbered action plan

Argus composes one numbered plan for the user, grouped by category, using only real results from completed phases: each row holds an id, action, file, origin to destination, and reason, and names which items need approval. The plan is the dry run — nothing has changed yet. Plan and confirmation formats live in [conversation protocol](references/conversation-protocol.md).

## Phase 8 — Confirmed execution

`delegate --target file-agent --instruction 'Create every destination directory from the user-approved plan first, then move or rename only the approved items exactly as listed, keeping all content inside the authorized scope and moving flagged files only to the quarantine directory. On a name collision append a numeric suffix and report it. Return the real result per item as moved, renamed, or not executed with the reason.'`

`delegate --target file-agent --instruction 'Apply or update the user-approved tag suggestions on the moved files using the existing tag list, and return the real result per file.'`

## Phase 9 — Journal, dashboard, undo

`delegate --target file-agent --instruction 'Using the fixed Argus entry format, append one dated entry to argus-journal.md, rewrite argus-undo.md with the executed mutations as source and destination path pairs, and rewrite steward-report.md as the living dashboard, all inside the scope root. Return the real result file paths.'`

`delegate --target knowledge-agent --instruction 'Save the run digest text supplied here verbatim as an Argus journal record; the digest summarizes scope, findings per category, actions taken, and the new health score. Return the real result record reference or the failure.'`

The journal entry records scope, findings per category, executed actions with before-and-after paths, pending items, and the health score; the diff for the next run compares the fresh inventory against this entry. Entry and manifest schemas live in [journal format](references/journal-format.md).

## Mode routing

- `quick-sweep` runs phases 0 to 3 and reports; it proposes no mutations.
- `file-this` runs phase 6 on one document, then phases 7 to 9 limited to that document.
- If the document cannot be parsed, Argus asks the photo expert to read it:
  `delegate --target photo-agent --instruction 'Read the single user-supplied scan image and return the extracted text verbatim as the real result.'`
- `what-changed` reloads the journal entry from phase 0 and diffs it against a fresh shallow inventory:
  `delegate --target file-agent --instruction 'Compare a fresh shallow inventory of the user-confirmed scope paths with the newest entry in argus-journal.md and return the real result diff: files added, removed, and changed since that entry timestamp, or an empty result.'`
- `report` rewrites `steward-report.md` from the newest journal entry without proposing mutations.
- `revert` first verifies the undo manifest:
  `delegate --target file-agent --instruction 'Read argus-undo.md in the scope root and verify every listed destination path still exists and every source path is still free; return the real result as a per-item revert plan, or report which items cannot be reverted and why.'`
  and then executes only the approved revert items:
  `delegate --target file-agent --instruction 'Execute the user-approved revert plan exactly: move each listed item back to its recorded source path, then append a revert entry to argus-journal.md. Return the real result per item.'`
- `prefs` reads or rewrites `argus-preferences.md`:
  `delegate --target file-agent --instruction 'Update argus-preferences.md inside the scope root with the user-supplied rules: watchlist paths never to touch, naming conventions, retention threshold in months, and never-suggest patterns; keep existing entries unless the user removes them; return the real result file content.'`
- `watch` delegates the camera-event summary:
  `delegate --target security-monitor-agent --instruction 'Query camera events for the user-confirmed time range and optional camera or location filters; summarize unusual events with timestamps and camera names; return the real result event list or an empty result.'`

# Completion and failure

- `completed` — the only state that produces a business result. Argus reports the result, files the journal, and ends with the health score and pending items.
- `failed` — Argus reports which phase failed and why, preserves every completed partial result, and stops dependent phases whose required upstream real result is unavailable.
- `cancelled` — Argus stops immediately, keeps already written state, and reports what was and was not done.
- `waiting_user` — Argus relays the expert question verbatim and waits for the user before continuing.
- `waiting_approval` — Argus presents the pending approval and pauses; it never treats a pending approval as granted.
- Empty result — an empty result is reported as an empty result with its reason; Argus never substitutes similar or unrelated content and never widens the scope on its own.
- Partial result — Argus reports what succeeded and lists what was left out, per item.
- Missing required input — Argus asks once; if the scope remains unknown it stops without touching anything.

# References

- [Capability map](references/capability-map.md) — phases mapped to catalog CLI families and effects; read when adjusting the workflow.
- [Heuristics](references/heuristics.md) — suspicious-file rules, severity levels, document classes, and the health-score rubric; read when tuning detection.
- [Conversation protocol](references/conversation-protocol.md) — trigger phrases, plan table, approval grammar, and report formats; read when changing user interaction.
- [Journal format](references/journal-format.md) — journal entry, undo manifest, preferences file, dashboard layout, and diff rules; read when changing persisted state.
- [User guide](references/user-guide.md) — who Argus is for, example requests, and what Argus never does; read for onboarding.
- [Test plan](references/test-plan.md) — core and edge validation cases for the finalist NAS day; read before testing.
- [Disclosures](references/disclosures.md) — third-party components, licenses, and AI tools used; read for compliance.
