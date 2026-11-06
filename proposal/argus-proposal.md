# Argus — Project Proposal (Round 1 draft)

Track: Open Innovation · Entrant: individual

> Word budget check: the ten answers below must total ≤500 English words. The Annex is outside the limit.

## 1. What does your Skill do? (one sentence)

Argus, the hundred-eyed steward, audits authorized NAS folders for duplicates, suspicious files, storage waste and disorganization; it proposes a numbered, approval-gated action plan, executes only what the user confirms, and keeps a journal it can diff — and undo.

## 2. Target user and problem

Home and prosumer NAS owners whose folders silently decay over time: duplicates accumulate, scans stay unclassified, space is wasted, and suspicious files go unnoticed. They need order with evidence and a way back — not a black box.

## 3. Solution

Argus is a Markdown-only Uliya Skill that runs a nine-phase audit, presents one numbered plan, executes only the approved items, and records a dated journal entry with an undo manifest, a dashboard, and a health score.

## 4. Core user flow

The user says "Argus, audit Documents"; Argus reports its findings and presents the numbered plan; the user replies "all" or selects items; Argus executes and reports the score and journal path. Later runs answer "what changed?" or "undo the last run".

## 5. Differentiation

Published skills are single-purpose and stateless: they run once and forget. Argus adds steward memory — a journal with run-over-run diffs — reversibility through its undo manifest, a deterministic suspicious-file rule set, and a health score, forming one coherent steward rather than five separate tools.

## 6. NAS capabilities used, and where

file-agent inventories, deduplicates, moves and tags (`ug-filesystem`, `ug-filemgr`, `file-workflow`) in phases 1–5 and 8; document-agent classifies and extracts fields (`ug-document`) in phase 6; knowledge-agent stores the run digest (`ug-knowledge`) in phase 9; photo-agent supplies OCR and media metadata (`ug-photo`); security-monitor-agent summarizes camera events (`ug-surveillance`). The local AI model backs classification; data never leaves the NAS.

## 7. Technical approach

The parent SKILL.md delegates self-contained instructions to six registered experts over published CLI families (catalog v2.0.0). Deterministic rules turn expert evidence into verdicts; low-confidence items route to review; every mutation requires explicit user approval. Inputs: scope paths and mode. Outputs: the plan, executed changes, journal, undo manifest, dashboard, and score.

## 8. Current status

Complete and statically validated: SKILL.md plus eleven linked reference documents pass the official checker with zero errors and zero warnings. Remaining: on-device validation of delegation depth, quarantine semantics, and journal read-back.

## 9. Validation plan

Core 1 — full-audit on a synthetic messy folder: verify plan accuracy, approved execution, journal and undo manifest, and one reverted item. Core 2 — file-this on a scanned invoice: correct classification, rename, filing, and journal entry. Edge — empty folder or first run without a journal: clean empty result, no invented diff.

## 10. Limitations and risks

Argus flags suspicious files for review; it is not an antivirus. Large scopes run sampled and paginated. Journal fidelity depends on the metadata exposed by supported capabilities, and the single assigned testing day limits on-device tuning.

---

## Annex (outside the 500-word limit)

### A. Entrant identification

**Full name**: Helmut Chaparro Sandoval — individual entry, no team members.

**Residence**: Bogotá D.C., Colombia — eligible country per Section 3 of the Official Rules.

**Contact**: helmut.chs@gmail.com · Repository: github.com/HCHAPS404/ARGUS

### B. Consent declaration

I, Helmut Chaparro Sandoval, declare that: (a) this submission is my original work; (b) the Skill and its core workflow were newly developed during the Hackathon period — development began on November 6, 2026; (c) no previously developed Skills or submission materials were reused; (d) I have read and agree to be bound by the Official Rules and the Devpost Terms of Service; and (e) I meet the eligibility requirements stated in the Official Rules.

### C. Third-party components and licenses

The Argus package ships Markdown documentation only; it invokes published UGREEN NAS capabilities at runtime and distributes no code, libraries, datasets, or external services.

- **UGREEN Uliya Skill Kit v0.7.3** — sponsor-provided development tooling; used for capability consultation and static validation; not distributed inside the package.
- **No other third-party components** — no external dependencies, fonts, images, or data flows are included.

### D. AI tools used

- **Devin** (Cognition) — AI coding assistant; supported drafting and validation of the Markdown skill files and proposal text. All output was reviewed, edited, and approved by the entrant; the concept, architecture, and decisions are the entrant's own.
- **UGREEN UGOS Skill Creation Tool v0.7.3** — sponsor-provided; capability consultation and static checks.

### E. Author's license

The entrant's original work — the Argus skill package and its accompanying documentation — is intended for publication under the MIT License; the license text ships in the public repository.

### F. Electronic signature

/s/ Helmut Chaparro Sandoval — Bogotá D.C., Colombia — November 6, 2026
