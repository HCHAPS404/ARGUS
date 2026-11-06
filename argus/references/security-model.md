# Argus security and privacy model

What Argus promises, what it deliberately does not, and the boundaries it enforces. Read before modifying heuristics, quarantine behavior, or any copy that describes detection.

## What Argus is

A **heuristic screening layer** for user-authorized folders. It applies deterministic rules (R1–R8 in [heuristics](heuristics.md)) over file metadata and readable content to surface items worth a human look: misleading names, executables in document/media territory, zero-byte payloads, anomalous sizes, header/extension mismatches.

## What Argus is not

- **Not an antivirus.** No signature database, no behavioral sandbox, no real-time protection, no remediation. Argus says "flagged for review" — never "infected", "malware", "clean", or "safe".
- **Not a forensic tool.** It reports metadata-level anomalies; it does not attribute intent or prove compromise.
- **Not an enforcement agent.** It quarantines only on approval, deletes nothing silently, and never acts outside the confirmed scope.

## Evidence standard

Every flag carries three fields — **rule id, path, evidence** — and every flag is reproducible: the same file under the same rules always produces the same flag. There is no model judgment in a severity verdict. This is what makes a flag contestable: the user can see *why* it fired and override it.

| Tier | Rules | Plan disposition |
|---|---|---|
| High | R1–R3, R8 | Proposed quarantine (move only, approval required) |
| Medium | R4–R6 | Review lines in the plan |
| Low | R7 | Listed for awareness |
| Not evaluated | any rule lacking its input evidence | Reported as "not evaluated" — never guessed |

## Quarantine semantics

Quarantine is a **reversible relocation** inside the scope, not deletion and not a system primitive: a move to `quarantine/` recorded in the undo manifest. Items stay visible in the dashboard as quarantined; the user decides their fate. `revert` returns them to source after verification.

## Privacy boundary

- **Local-first**: all analysis runs inside UGOS capabilities on the NAS; no file content, metadata, or personal data leaves the device through Argus.
- **Minimal collection**: Argus reads only what the confirmed scope contains and only what each phase needs; watchlist paths are excluded before inventory, not after.
- **State files are user-readable**: journal, undo manifest, preferences, and dashboard are plain Markdown in the scope root — inspectable and user-editable.
- **No credential handling**: Argus never asks for or stores secrets, tokens, or passwords; if a flagged file looks like a credential store, it is reported as sensitive-looking — its contents are not copied or quoted.
- **Test data**: all development and demo corpora are synthetic; no real personal data is used in testing.

## Surveillance access (`watch` mode)

The `security-monitor-agent` capability is used **read-only** — event summaries for a user-confirmed time range. Argus never modifies camera settings, never stores footage, and correlates events with file activity only when the user explicitly asks.

## Trust boundaries Argus enforces on itself

| Boundary | Rule |
|---|---|
| Scope | Nothing outside the confirmed paths; nothing inside watchlist paths |
| Authority | No mutation without an explicit, specific approval |
| Knowledge | No result is ever fabricated; missing evidence is reported as missing |
| Persistence | State files record what happened; they never silently rewrite history (journal is append-only) |
| Language | Output says "flagged", "suspicious", "review" — never verdicts Argus cannot prove |
