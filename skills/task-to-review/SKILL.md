---
name: task-to-review
description: Carry an authorized code task through an isolated worktree, relevant checks, preview, and reviewable change. Use when the user asks to take a task to completion or prepare it for review.
---

Identify the repository, machine, selected account, and the observable result the user wants. Preserve project-specific model choices and instructions. For a new task, use a separate branch and worktree without changing the original checkout. When fleet is configured, `fleet task /path/to/repo task-slug --profile NAME --done 'completion condition'` creates and records it. Otherwise use the repository's ordinary Git worktree workflow.

Work until the requested result is reviewable. Run the checks that can catch failures introduced by the change. For UI work, inspect the rendered result and provide a screenshot and reachable preview when useful. For remote review, bind to `0.0.0.0` on the configured trusted network and return the actual reachable preview URL.

When fleet is configured, use `fleet lease heavy-build -- COMMAND ...` for a heavy local build so fleet-launched builds do not overlap. This only coordinates commands using the lease; inspect existing workload before assuming a machine is idle.

When a PR is authorized, write it for a reviewer who has not seen the chat. Resolve applicable CI and review findings within scope. Do not infer permission to publish, merge, or contact someone. Report a real blocker with the evidence needed to decide the next step.

Finish with the result, artifact or PR link, checks, and any unresolved limitation. Release only processes or previews this task owns when they are no longer needed. Keep an ownership record if a preview should remain available.
