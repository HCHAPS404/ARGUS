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

NAS folders decay silently: duplicates pile up, scans stay unclassified, space is wasted, and odd files go unnoticed. Existing tools fix one slice and forget. We wanted a steward — something that audits, proposes, waits for a yes, and remembers. Named after Argus Panoptes, the hundred-eyed guardian of Greek myth.

## What it does

Argus audits authorized folders across five checks — duplicates, suspicious patterns, storage waste, disorganization, and document hygiene — then presents one numbered action plan. It executes only the approved items, writes a dated journal entry with an undo manifest and a health score, and can later report what changed or revert the last run. Modes: full-audit, quick-sweep, file-this, what-changed, report, revert, prefs, watch.

## How we built it

A Markdown-only Uliya Skill. SKILL.md delegates self-contained instructions to six registered expert agents over nine published CLI families (capability catalog v2.0.0). Deterministic rules turn evidence into verdicts; low-confidence items route to review; every mutation requires approval. The journal persists as plain files written and re-read via the filesystem CLI. Validated with the official check-skill.mjs: static-pass, zero errors, zero warnings.

## Challenges we ran into

Fitting a broad steward into one coherent workflow instead of five tools; writing an honest suspicious-file rule set (flags for review, never antivirus claims); engineering memory — journal, undo manifest, preferences, dashboard — from plain Markdown state files.

## Accomplishments that we're proud of

A complete skill package that passes the official checker with zero errors and zero warnings; a nine-phase pipeline with eight modes; and a stateful design — journal diffs, undo, watchlist preferences, health score — that stateless skills do not have.

## What we learned

The Uliya delegation model and its approval boundary; how much the capability catalog already provides (native deduplication and organize plans); and how to design explainable automation where rules, not the model, set verdicts.

## What's next for Argus

Finalist validation on the iDX6011 Pro with our synthetic dataset; tuning sample caps, delegation granularity, and heuristics against real metadata; then the demo video.

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
