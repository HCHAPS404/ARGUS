# Capability map

How each Argus phase maps to published NAS capability families (catalog v2.0.0). The parent Skill only delegates; the registered expert chooses Actions and parameters internally. Every mutation family is approval-gated (`gateway`, `conditional`, or `workflow` approval in the catalog).

## file-agent — `ug-filesystem`, `ug-filemgr`, `file-workflow`

| Phase | Capability family | Actions the expert may use | Effect |
|---|---|---|---|
| 0, 9, revert, prefs | `ug-filesystem` | `cat` (read state files), `echo` (write state files), `touch` | read / state-change |
| 1 | `ug-filesystem` | `ls`, `find` (pattern, type, min-size, max-size, date-type, timestamps, max-depth, limit), `stat`, `getfattr`, `category` | read |
| 2 | `ug-filemgr`, `ug-filesystem`, `file-workflow` | `scan-dedupe`, `md5sum`, `sha256sum`, `mediainfo`; `start --kind deduplication --keep-by` for the native plan | read |
| 3 | `ug-filesystem` | `find` (patterns, type, size bounds), `stat`, `getfattr`, `cat` first bytes for header-vs-extension checks | read |
| 4 | `ug-filesystem` | `find` (min-size, date bounds), `ls` | read |
| 5 | `ug-filesystem` | `ls` (shallow), `find` (type dir, empty roots) | read |
| 8 | `file-workflow`, `ug-filesystem`, `ug-filemgr` | `run` (execute a planned workflow), `batch-move` (renameBy, dateField), `mkdir`, `cpmv`, `rename`, `tag-add-file`, `tag-list` | state-change |
| revert | `ug-filesystem` | `cpmv`, `restore`, `echo` | state-change |

## document-agent — `ug-document`

| Phase | Actions the expert may use | Effect |
|---|---|---|
| 6, file-this | `extract` (schema), `qa` (entities), `metadata`, `page-count`, `reconcile` | read |
| report | `writing` (generate the digest text) | mixed |

## knowledge-agent — `ug-knowledge`

| Phase | Actions the expert may use | Effect |
|---|---|---|
| 9 | `save-text` (run digest record), `collect-evidence` (query prior journal evidence) | state-change / read |

## photo-agent — `ug-photo`

| Phase | Actions the expert may use | Effect |
|---|---|---|
| 2 | `meta`, `mediainfo` via inventory, `vision-vlm` for best-version ties | read |
| file-this fallback | `vision-ocr` | read |

## security-monitor-agent — `ug-surveillance`

| Mode | Actions the expert may use | Effect |
|---|---|---|
| watch | `cameras`, `event-timeline`, `identity-resolve`, `event-evidence` | read |

## Notes

- `file-workflow start` returns a native plan (`status=planned`) that `run` executes after approval — Argus feeds its own confirmed plan into it when a batch organization fits.
- `ug-filesystem restore` can recover items from the recycle area as a second safety net behind quarantine.
- All approval-bearing Actions are only ever reached after explicit user confirmation in Phase 7/8.
