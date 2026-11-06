# Argus — user guide

## Who it is for

Anyone whose NAS folders drift out of shape: downloads piling up unclassified, duplicates eating space, scanned paperwork with no home, and the quiet worry that something odd landed where it should not. Argus is for people who want order with a record — and an undo button.

## What it does, in one breath

Say "Argus, audit Documents". It inspects the folder (duplicates, suspicious patterns, storage waste, disorganization, document hygiene), shows one numbered plan of proposed actions, waits for your yes, executes only that, and files a dated journal entry with an undo manifest and a health score. Next time you ask, it tells you what changed.

## Example requests

- "Argus, audit Documents" — the full nine-phase run.
- "Sweep Downloads for anything weird" — quick-sweep, report only.
- "File this invoice" — classify one document and put it in the taxonomy.
- "What changed since Tuesday?" — diff against the journal.
- "Undo the last run" — verified inverse moves after your approval.
- "Never touch Family Photos" — adds a standing watchlist rule.
- "Anything unusual on the cameras this week?" — read-only event summary.

## What Argus never does

- Never deletes your files — flagged items go to a recoverable quarantine, and every move is journaled for `revert`.
- Never touches paths outside your confirmed scope, or anything on your watchlist.
- Never acts on a pending approval — `waiting_approval` pauses until you decide.
- Never guesses: a flag means "worth your review", not "confirmed threat"; low-confidence items go to review, not to action.
- Never sends your content outside the NAS — findings are computed from metadata and platform experts, and state files stay in your folders.
- Never invents results: an empty result is reported as an empty result.

## Reading the artifacts

`steward-report.md` is the living dashboard (score, trend, pending). `argus-journal.md` is the audit log. `argus-undo.md` is what `revert` uses. `argus-preferences.md` is yours to edit — Argus reads it every run.
