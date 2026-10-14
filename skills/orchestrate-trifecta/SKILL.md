---
name: orchestrate-trifecta
description: Coordinate implementation and independent review through T3 delegated tasks. Use when the user asks for trifecta, orchestration, builders or reviewers. Skip quick edits and delegated child tasks.
---

Use three roles: coordinator, builder and independent reviewer. They can share the same authorized account; the workflow does not require a university seat or multiple subscriptions.

Read the project's instructions and define completion, relevant checks and artifact locations. Call `orchestrator_capabilities` to discover provider instances, models, options and cross-provider child support. Respect project model requirements. Use only providers authorized for this task's identity. Employer work remains entirely in employer-approved environments. If a needed provider is missing or exhausted, report it and continue only the independent work possible on the selected identity.

Maintain a progress file with the brief, worktree paths, task IDs, outcomes and unresolved findings. Delegate implementation with `delegate_task`, `role: implementation` and `mode: async`. Each brief includes the goal, absolute worktree, relevant files, completion criteria, checks and commit rules. At most two concurrent builders by default; each gets its own worktree. Keep a distinct stable `clientRequestId` for each task and retain its `taskId`. Use `task_status` or `task_cancel` for that task. Do not create top-level threads to implement child work.

Review each completed unit with an independent delegate using `role: review`. Preserve GPT-6.1 Sol with high reasoning as the preferred reviewer when available and authorized; discover its live provider ID. Ask for ranked defects with file locations, consequences and proposed corrections. Give reviewers the brief and artifacts rather than the builder's assurance. Fix findings, then request one confirming review. Every review round is a new `delegate_task` with the original brief, earlier findings, responses and unresolved objections. Never continue a review by messaging its backing child thread.

Run the final relevant checks yourself. Register any authorized PR with `link_pull_request` when available. Do not infer permission to merge, publish or contact others. Report the reviewable result, checks, review findings and remaining limitations. Never restart T3, alter its providers, change Tailscale Serve or move employer content into personal accounts.
