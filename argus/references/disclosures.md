# Disclosures

## Third-party components and licenses

Argus is a Markdown-only orchestration Skill. It ships no code, libraries, binaries, or bundled assets. It uses only published UGREEN NAS capabilities through registered expert agents (`file-agent`, `document-agent`, `knowledge-agent`, `photo-agent`, `security-monitor-agent`), as listed in `SKILL.md` under "Generation-time capability evidence". No external services are called; no data leaves the NAS by design.

## Principal functionality developed for this Hackathon

- The nine-phase stewardship workflow (inventory, duplicates, suspicious-pattern sweep, storage health, disorganization, document hygiene, plan, confirmed execution, journal).
- The deterministic suspicious-file rule set and health-score rubric (`references/heuristics.md`).
- Persistent steward state: journal, undo manifest, preferences, and dashboard (`references/journal-format.md`).
- The conversational plan-and-approval protocol (`references/conversation-protocol.md`).

## AI tools used and their principal uses

- Devin (Cognition) — AI coding assistant used for drafting and iterating the Skill Markdown, cross-checking against the official catalog and static checker, and preparing documentation. All outputs were reviewed and edited by the entrant.
- The UGREEN UGOS Skill Creation Tool (uliya-skill-kit v0.7.3, provided by the Sponsor) — capability catalog consultation and static validation via `check-skill.mjs`.

## License of this work

The entrant's original work is intended for publication under the MIT License.

## Data handling

Runs read only user-authorized scope paths and write state files only inside those paths. Test and demo data are synthetic. No credentials, personal data, or API keys are included in this package.
