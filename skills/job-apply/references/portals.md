# Portal details

## Workday

Wait for field values and dropdown options to load, not only the step heading. A heading can appear before saved answers, required fields, or repeated rows are available. Navigation during that interval can overwrite values or trigger spurious errors.

After adding a repeating row, wait for the new row's own input, read its current identifier, then type and blur. Do not assume the row exists immediately after Add, and do not reuse identifiers across navigation.

After saving edits to websites or employment, reopen or reload the saved draft. In one observed application, local Review showed four work stints and one website while the server retained eight work rows and five websites. New rows then produced duplicate-URL errors even with distinct visible values. A fresh load exposed the stale records. Delete the duplicate persisted rows through the form, save completely, reload, and verify the final count. Do not work around stale duplicates by creating alternate URL spellings.

The current section's heading does not prove that saving has completed. Wait for a definite next step or validation result; slower saves can take more than ten seconds. On timeout, inspect before clicking again.

The required terms checkbox can reset after reloading the draft. Inspect the actual value before continuing.

Keep a co-op and a later part-time return as separate stints if the form needs distinct dates. Do not turn the co-op into uninterrupted employment.

A stored browser tab title can say Sign In even after authentication. Inspect the page itself.

A final Submit click is not the result. Capture the success message and matching requisition in Candidate Home. If submission seems to hang, check the existing application status before retrying.
