# Keep public source clean

The bank contains recipes, generic configuration and selected skills. Store real account settings, Canvas/Notion configuration, credentials, session state, device information, logs, backups and personal data outside the checkout. Personal spreadsheets and health exports are excluded.

Before committing, review the full diff, including added binary assets. Stage only intended source, refresh the inventory, then run:

```sh
python3 scripts/index-bank.py
git add bank/files.json
python3 scripts/check-public.py --history --secrets
python3 -m unittest discover -s tests -v
```

Install [Gitleaks](https://github.com/gitleaks/gitleaks) first; on macOS use `brew install gitleaks`. The `--secrets` flag requires it and fails if it is unavailable. CI uses version 8.30.1 with the published release checksum. The custom check scans tracked bytes, validates inventory hashes, and flags personal home paths, private tailnet details, example session IDs and private state files. Findings print locations, not matched values. Secret scanning supplements that check using Gitleaks' default rules.

The only Gitleaks exception is a SHA256 value in `bank/files.json` under the generic key rule. The checker verifies every inventory value against actual source bytes; other rules and other files remain enabled. Ignored local files never enter the scan snapshot or an exported kit.

`--history` checks every reachable revision, including data deleted from the latest files. Removing a file in a new commit does not remove its old contents. History cleanup requires coordinated replacement of affected refs and fresh clones for collaborators. Copies, forks and hosting caches can outlive that replacement. If an actual credential was exposed, revoke or rotate it with its owner; rewriting Git is insufficient.

Automated checks do not prove that every document or media file is appropriate to publish. Review screenshots, metadata and third-party licensing manually. Keep upstream credits and license notices. Private repository provenance and deployment records are omitted; hashes in the historical source manifest describe imports before public adaptation.
