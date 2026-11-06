# ARGUS — UGREEN Hackathon 2026 on AI NAS

Project workspace for the `argus` skill ("the hundred-eyed steward"), built to the Uliya Skill Development Standard for the UGREEN Hackathon 2026 (Devpost: ugreenhackathon.devpost.com).

## Governance (rigid, user-set)

- **VCS**: only the repository owner runs git commit/push/PR. The assistant works on local files only — never execute git write operations.
- **No assistant attribution** anywhere: no "Generated with..." footers, co-author trailers, headers, comments, tags, or collaborator identification in any artifact.
- Hackathon rule: AI tools used must be disclosed in the submission's disclosures (references/disclosures.md). Wording is owner-decided.

## Workspace layout

| Path | Contents | Submitted? |
|---|---|---|
| `argus/` | The skill package (SKILL.md + references/) — the deliverable | Yes, zipped |
| `uliya-skill-kit/` | Official UGOS Skill Creation Tool v0.7.3 (catalog, checker, docs) | No |
| `proposal/` | Project Proposal PDF drafts (English, ≤500 words for the 10 answers) | Yes, PDF |
| `test-data/` | Synthetic test files for the R2 test plan | No |
| `submission-r1/` | Frozen copies of the exact submitted ZIP+PDF — never delete | No |
| `notes/` | Working notes, competitive intel | No |

## Checker (official validator)

```bash
node uliya-skill-kit/scripts/check-skill.mjs argus
```

Pass target: `status: "static-pass"`, `errors: 0`, `warnings: 0`. Node 20+ required.
Checker contract (v2.0.0): root allows only SKILL.md + references/ (plain .md only, all linked from SKILL.md); required H1s `# Goal`, `# Required input`, `# Workflow`, `# Completion and failure`, plus `# Generation-time capability evidence` with `` - `cli` → `agent` `` lines; delegates use `delegate --target <agent> --instruction '...'` single-quoted; body must cover completed/failed/cancelled/waiting_user/waiting_approval, empty results, and real-result passing; no code fences with language tags, no shell file ops, no absolute NAS paths, no cli.invoke, no credentials.

## Key facts

- 9 CLIs → 6 agents: ug-filesystem/ug-filemgr/file-workflow → file-agent; ug-document → document-agent; ug-knowledge → knowledge-agent; ug-photo → photo-agent; ug-video/ug-music → media-agent; ug-surveillance → security-monitor-agent.
- Catalog: `uliya-skill-kit/data/capability-catalog.json` (v2.0.0, source of truth).
- R1 deadline: Nov 15, 2026 11:45pm PT (= Nov 16 08:45 CET). Internal target: submit by Nov 14.
- All submission materials in English.
