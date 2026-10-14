# Validate your setup

Run the deployment tests before changing profiles. They use temporary homes, not a live account:

```sh
python3 -m unittest discover -s tests -v
```

After an authorized installation, run `scripts/fleet doctor` on each configured worker. Check profile protection, pinned skill contents, provider identity, and reachability. A passing offline test does not verify your live setup.

Use a fresh conversation to verify file access and a follow-up turn for each selected provider. Keep transcripts, account details, quota receipts and session identifiers in private state outside Git. Verify cache accounting separately with [the cache guide](cache-verification.md).

Check specialized tools only when selected: image generation, geometry validation, real browser verification and native Windows display tests each have different prerequisites. Display tests require the worker's interactive login. Record which checks passed and which remain unverified; do not copy an earlier installation's results.
