# Devpost submission fields — copy-paste texts

Round 1 form for ugreenhackathon.devpost.com. Fill what the form asks; not every field may appear.

## Project name

Argus — AI Steward for UGREEN AI NAS

## Tagline / short description

The hundred-eyed steward that audits your NAS, proposes an action plan, executes only what you approve — and remembers everything.

## Track

Explore Your Imagination (= Open Innovation)

## Inspiration

NAS folders decay silently: duplicates pile up, scans stay unclassified, space is wasted, and odd files go unnoticed. Existing tools fix one slice and forget. We wanted a steward — something that audits, proposes, waits for a yes, and remembers.

## What it does

Argus audits authorized folders across five checks — duplicates, suspicious patterns, storage waste, disorganization, and document hygiene — then presents one numbered action plan. It executes only the approved items, writes a dated journal entry with an undo manifest and a health score, and can later report what changed or revert the last run. Modes: full-audit, quick-sweep, file-this, what-changed, report, revert, prefs, watch.

## How we built it

A Markdown-only Uliya Skill. SKILL.md delegates self-contained instructions to six registered expert agents (file-agent, document-agent, knowledge-agent, photo-agent, security-monitor-agent) over nine published CLI families (catalog v2.0.0). Deterministic rules turn evidence into verdicts; low-confidence items route to review; every mutation requires approval. The journal persists as plain files written and re-read via the filesystem CLI. Validated with the official check-skill.mjs: static-pass, zero errors, zero warnings.

## Challenges we ran into

Fitting a broad steward into one coherent workflow instead of five tools; writing an honest suspicious-file rule set (flags for review, never antivirus claims); engineering memory — journal, undo manifest, preferences, dashboard — from plain Markdown state files.

## Accomplishments

A complete skill package that passes the official checker with zero errors and zero warnings; a nine-phase pipeline with eight modes; and a stateful design — journal diffs, undo, watchlist preferences, health score — that stateless skills do not have.

## What we learned

The Uliya delegation model and its approval boundary; how much the capability catalog already provides (native deduplication and organize plans); and how to design explainable automation where rules, not the model, set verdicts.

## What's next for Argus

Finalist validation on the iDX6011 Pro with our synthetic dataset; tuning sample caps, delegation granularity, and heuristics against real metadata; then the demo video.

## Attachments to upload

- `Argus-Project-Proposal.pdf` (exported from Word, ≤1 MB)
- `submission-r1/argus-r1.zip` (13.8 KB, Markdown-only, checker-passed)

## Team

Individual — Helmut Chaparro Sandoval (Representative).

---

# Step 3 — Project details

## About the project (paste this whole Markdown block)

## Inspiration

Every NAS tells the same quiet story: folders that decay. Duplicates pile up across backup folders. Scans and downloads land in a pile nobody files. Temp artifacts and forgotten installers eat terabytes. And once in a while, a file shows up that just looks *wrong* — a `report.pdf.exe` sitting where documents live.

Existing tools each fix one slice — a dedupe pass here, a cleanup there — and then forget everything. They cannot tell you what changed since last month, they cannot undo what they did, and they never ask before acting.

We wanted something different: a **steward**, not a script. Something that audits like an inspector, proposes like an advisor, acts only on your word — and remembers everything it did. Named after **Argus Panoptes**, the hundred-eyed guardian of Greek myth who saw everything and forgot nothing.

## What it does

Argus audits user-authorized folders across **five checks** — duplicate content, suspicious file patterns, storage waste, disorganization, and document hygiene — then composes **one numbered action plan**. It executes only the items the user explicitly approves, writes a dated journal entry with an undo manifest and a living dashboard, and reports a deterministic **health score** from 0 to 100.

Because the journal persists as plain Markdown files inside the audited folder itself, later runs can answer *"what changed since last time?"* — and the last run can be reverted item by item.

| Mode | What it does |
|---|---|
| `full-audit` | The complete nine-phase pipeline: scan → analyze → plan → approve → execute → journal |
| `quick-sweep` | Fast hygiene pass — duplicates, temp files, suspicious patterns. Report only |
| `file-this` | Classify and file one document into the taxonomy, with a proposed name |
| `what-changed` | Diff the scope against the newest journal entry — incremental report |
| `report` | Regenerate the dashboard and health score — no mutations |
| `revert` | Verify the undo manifest and roll back the last run, item by item |
| `prefs` | Manage the persistent watchlist: never-touch paths, naming rules, thresholds |
| `watch` | Read-only summary of security-camera events for a time range |

**What makes it different from a cleanup script:** Argus is *stateful*. Most skills are one-shot — they run, act, and forget. Argus keeps memory (journal + diff), keeps receipts (undo manifest), keeps your rules (preferences), and keeps score (0–100 health metric). Everything is reversible, everything is auditable, and nothing moves without your yes.

## How we built it

Argus is a **Markdown-only Uliya Skill** — no runtime, no binaries, no external services. The parent `SKILL.md` orchestrates six registered expert agents (`file-agent`, `document-agent`, `knowledge-agent`, `photo-agent`, `security-monitor-agent`, `media-agent`) over nine published CLI families from capability catalog v2.0.0, using only `delegate` commands with self-contained instructions.

The design follows a strict decision model:

**evidence → deterministic rules → confidence buckets → human approval → reversible action → journal**

- **Evidence first**: every verdict traces to real metadata (hashes, sizes, headers, timestamps) — never model intuition
- **Rules, not vibes**: the suspicious-file rule set (R1–R8: double extensions, executables in document folders, header/extension mismatches, zero-byte payloads…) is deterministic — same evidence, same flag
- **Confidence gating**: low-confidence findings route to a *review bucket* in the plan instead of automatic action
- **Reversible by design**: moves over deletes; flagged items go to a quarantine folder; the undo manifest records source→destination pairs
- **Memory from primitives**: journal, preferences, and dashboard are plain Markdown state files written and re-read through the filesystem CLI — no database needed
- **Honest security**: Argus *flags for review*, it never claims antivirus detection

Validated with the official `check-skill.mjs`: **static-pass, zero errors, zero warnings** — 8 Markdown files, 13.8 KB zipped.

## Challenges we ran into

- **Breadth without chaos**: fitting a steward's ambitions into one coherent workflow instead of five disconnected tools — solved with a strict nine-phase pipeline where read phases always run and mutation phases only run post-approval.
- **Honest heuristics**: writing a suspicious-file rule set that flags genuinely risky patterns (header/extension mismatch via magic bytes, double extensions) while never overclaiming "malware detection".
- **Engineering memory in Markdown**: journal, undo manifest, preferences, and dashboard had to be built from plain state files — including the diff logic that compares a fresh inventory against the last journal entry.
- **Designing for the unknown**: the catalog marks permission and stability details as unknown for several actions, so we designed for the strictest case — every mutation behind approval, every phase reporting partial results.

## Accomplishments that we're proud of

- A complete, checker-clean skill package: **static-pass, 0 errors, 0 warnings** on the official `check-skill.mjs`
- A nine-phase orchestrated pipeline with **eight user-facing modes** — from one-shot audits to reverting the last run
- A **stateful design** most skills lack: journal diffs, undo manifests, watchlist preferences, and a deterministic health score
- A suspicious-file heuristic layer that gives users early warning **honestly** — flags with evidence, never antivirus theater
- A worked synthetic test corpus (`test-data/messy-scope`) with one trigger file per heuristic rule, ready for finalist validation

## What we learned

- The **Uliya delegation model** and its approval boundary: the parent skill plans, experts execute, and the boundary between them is where trust is enforced
- How much the capability catalog already provides natively — deduplication plans, organize workflows, OCR, document extraction — and how to orchestrate rather than reimplement
- That **explainable automation** beats clever automation: deterministic rules over evidence produce verdicts users can audit, contest, and trust

## What's next for ARGUS

If selected as a finalist: validation on the **iDX6011 Pro** with our synthetic dataset — tuning sample caps, delegation granularity, and heuristic thresholds against real NAS metadata — then the three-minute demo video. Beyond the hackathon: media-library deduplication via the photo/medium experts, scheduled `quick-sweep` runs, and community-tunable heuristic packs.

## Built with (tags — add up to 25)

markdown · python · nodejs · ugos · ugreen-ai-nas · uliya-skill-kit · ai-agents · agent-orchestration · file-management · llm · automation · audit · data-organization · privacy · local-first · devin

## "Try it out" links

GitHub repository URL if the project is public; otherwise leave blank (Round 1 artifact is the attached ZIP).

## Image gallery (JPG/PNG/GIF, ≤5 MB, 3:2 ratio, up to 15)

1. Argus logo (generated emblem) — main visual
2. Optional: workflow diagram of the 9-phase pipeline
3. Optional: mock conversation of a plan being approved

## Demo video URL

Optional in Round 1 (no asterisk). Leave blank — the video is a Round 2 requirement (≤3 min, public YouTube).
