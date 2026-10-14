# Imported source records

These files preserve the source material reviewed during the fleet migration. They are not deployment entrypoints. The Windows scripts are historical copies; inspect them and the current target before running them. Some were designed to install or restart T3 and must not run against an active installation.

`source-manifest.json` records historical imported skill hashes and public upstream provenance. Private repository locations, commits and backup paths are omitted. Current adapted file hashes live in `bank/files.json`. Profile memory and credentials are excluded.

Example machine roles live in `../machines/`. Managed behavior lives in `../scripts/fleetlib.py`. The historical machine notes here use placeholders; they do not describe a reachable installation.
