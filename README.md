# Argus — AI Steward for UGREEN AI NAS

Entry for the **UGREEN Hackathon 2026 on AI NAS** (ugreenhackathon.devpost.com), track: **Open Innovation**.

**Argus, the hundred-eyed steward** audits authorized NAS folders across duplicates, anomalies, storage health and disorganization; proposes a numbered action plan; executes only what the user approves; and remembers every run in a persistent journal — so it can report what changed and even undo its last run.

## Contents

- `argus/` — the skill package itself (Markdown-only, Uliya standard). **This is what gets submitted.**
- `uliya-skill-kit/` — official UGOS Skill Creation Tool v0.7.3 (capability catalog + static checker).
- `proposal/` — Round 1 Project Proposal (PDF, ≤500 English words for the ten answers).
- `test-data/` — synthetic files for finalist validation.
- `submission-r1/` — frozen Round 1 submission artifacts.
- `AGENTS.md` — workspace rules and checker usage.

## Validate the skill

```bash
node uliya-skill-kit/scripts/check-skill.mjs argus
```

Target: `status: "static-pass"`, 0 errors, 0 warnings.
