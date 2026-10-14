# Legacy fleet reference

The legacy module preserves older deployment helpers and configuration shapes. It is optional. Start with the current [README](../README.md), [fleet recipe](modules/fleet-tools.md) and [maintenance guide](maintenance.md).

`examples/legacy-fleet.json` illustrates separate personal, work and secondary identities, two gateways, and three machine roles. Its users, addresses, emails and service labels are examples. Use only accounts and workers you own or are authorized to configure. Keep work and personal histories, memory and credentials separate.

Configure each machine's OS, user, SSH alias, checkout and role. A single worker is enough. Extra machines can receive inference client keys through authenticated private transfer; gateway management keys and OAuth files remain on their refresh owner. Native accounts keep their authentication and settings.

Use `fleet release`, preview `fleet diff --profile NAME`, then apply only to a new managed profile. Profiles with session history require the documented idle migration. The historical installers under `imports/windows` may create scheduled tasks or start services; inspect them before adapting anything and preserve active installations.

Gateway configuration binds to your configured private address and requires separate client and management keys. Sign in freshly for each identity; do not copy native refresh credentials. Model choices are examples and need verification against your own provider.

Third-party skills are vendored and pinned; built-in, plugin-owned and organization-managed skills stay with their providers. Keep private auto-memory, deployment backups, session records and usage receipts outside this repository. Source provenance is described in [imports](../imports/README.md).
