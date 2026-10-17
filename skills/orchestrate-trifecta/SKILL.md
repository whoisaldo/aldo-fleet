---
name: orchestrate-trifecta
description: Run a build as a three-account workflow on T3's orchestrator. The thread on the coordinator Claude account coordinates, Claude on the builder account builds, and GPT-6.1 Sol on the reviewer Codex account reviews, all through delegate_task. Use when the user says "/orchestrate-trifecta", "trifecta", "use my workflow", "orchestrate this", gives a long or multi-part build goal, or asks for builders and reviewers. This is the default for any work big enough to delegate. Do NOT use for a quick edit or a question you can answer yourself, for unrelated employer work, or from inside a delegated child task.
---

# Orchestrate trifecta

## Shared copy setup

This is a redacted copy of a T3-specific workflow, not a standalone
orchestrator. Replace every angle-bracket provider ID with the matching ID
from your own live `orchestrator_capabilities` catalog. Use models and
options that catalog actually offers. The model names and review split below
are examples from the original workflow, not a promise of availability.

The account names, personal identity, employer and school references,
network addresses, and private machine paths have been removed. Plan limits
vary. Verify your own windows and quotas before using the thresholds below.

The included `scripts/usage.py` requires compatible gateway management APIs
and your own configuration. See README.md. It has no embedded credentials
and does not include any original account configuration.

A standing workflow for work big enough to hand out. Three accounts, one
role each, so that no single limit stops a run:

| Role | Account | T3 provider instance | Model | Limit |
| --- | --- | --- | --- | --- |
| Coordinator | Coordinator Claude account | the thread you are in | as started | check the actual plan |
| Builders | Builder Claude account | `<BUILDER_PROVIDER_ID>` | `claude-opus-5-5`, effort `high` | check the actual plan |
| Reviewers, 70% | GPT-6.1 Sol on the reviewer Codex account | `<REVIEWER_PROVIDER_ID>` | `gpt-6.1-sol`, reasoningEffort `high` | check the actual plan |
| Reviewers, 30% | Builder Claude account | `<BUILDER_PROVIDER_ID>` | `claude-opus-5-5`, effort `high` | as above |

You are the coordinator. If this thread is not on the selected coordinator Claude
account, say so and ask before going on. If you are a delegated child, do the
task you were given and do not start this workflow.

## Before the first delegation

1. Call `orchestrator_capabilities` (its output is large: it lands in a file,
   query it with `jq`). Confirm the three instances above exist with
   `canRunCrossProviderChildTask: true`, and take model and option ids from
   it. If an id here no longer matches, trust the live catalog and tell the user.
2. Run `python3 ~/.claude/skills/orchestrate-trifecta/scripts/usage.py` and note the
   three readings.
3. Write down what done means for this run, as checks you can run, and where
   the run's state lives: one progress file a successor could resume from.

## Your job as coordinator

The coordinator account pays for every token you read. Its quota can
limit the run. Spend it on decisions, not on work:

- Plan, split, brief, merge, run checks in the shell, decide. Do not write
  the feature code yourself and do not start native Claude subagents or
  workflows; those bill the coordinator account. Everything goes out through `delegate_task`.
- Do not open images or read large files a child can summarize. Ask for the
  answer in words with file paths and line numbers.
- Keep the progress file current after every merge and every review, with
  each `taskId`, what it was for, and its outcome.

## Delegating

- A child gets no history. Each task prompt carries the goal, what done
  means, the absolute worktree path, the files that matter, the checks to
  run, the repository's commit rules, and what to report back.
- `mode: "async"` for real work. A finished child wakes this thread on its
  own, so end the turn instead of polling. `mode: "wait"` only for a result
  you need within the same turn. `task_status` reads one mid-turn;
  `task_cancel` stops one that has gone wrong.
- A new `clientRequestId` for every task and every review round, kept stable
  across retries of that same call.
- At most two builders at once unless the user sets another number. Builders that
  run in parallel each get their own git worktree, created by you
  (`git worktree add`), with its path in the prompt. Two builders never share
  a checkout.
- Set `role`: `implementation` for builders, `review` for reviewers.

## Builders and their usage window

This workflow prioritizes the builder account to preserve coordinator
capacity. Verify the actual limits on your plans before using this policy.
Routing builders through `<BUILDER_PROVIDER_ID>` is what
makes that window visible: the fleet gateway records the usage header of
every response, and `usage.py` reads it.

- Run `usage.py` before each wave of builders and whenever a builder fails.
- Under 85% of the 5-hour window: build on the builder account.
- At 85% or more: start nothing large there. Let running builders finish.
- Exhausted (a child fails with a rate or usage limit error, or the status
  reads rejected): do these three things at once, so no work waits.
  1. Record in the progress file the time it ran out and the reset time
     `usage.py` gives.
  2. Carry on building on the coordinator account (`<COORDINATOR_PROVIDER_ID>`, `claude-opus-5-5`, effort
     `high`) at the same pace and the same number of builders. Re-send any
     builder task the limit cut off. The coordinator account is the configured fallback. The builder
     account goes first to preserve coordinator capacity.
  3. Set the clock: run
     `python3 ~/.claude/skills/orchestrate-trifecta/scripts/usage.py --sleep-until-reset builder`
     as a background command with the longest timeout allowed. It sleeps
     until a minute after the reset and its exit wakes this thread. Timers
     such as ScheduleWakeup do not fire in a T3 thread; a background command
     does. Exit code 3 means the reset is still ahead: run it again.
- When the clock goes off: send a one-line task to
  `<BUILDER_PROVIDER_ID>` to confirm it answers, read `usage.py`,
  and from then on every new builder goes to the builder account again. Builders
  already running on the coordinator account finish where they are. Record the switch back.
- Only one clock at a time. If this thread is resumed after a break, check
  the progress file for a recorded reset time and compare it with `date`
  before choosing an account.
- If the coordinator account itself runs out while the builder account is still closed, nothing can
  build: keep reviews and checks going, leave the clock running, and tell
  the user.
- If the builder account gateway itself is failing (errors that are not limits),
  the same seat is reachable without it as `<BUILDER_DIRECT_PROVIDER_ID>`.
  Usage is then not visible, so go by failures alone.

A reading older than 20 minutes is marked STALE. The builder account reading
refreshes whenever a builder runs. To refresh the coordinator account or Codex, send a one-line
`delegate_task` to `<COORDINATOR_GATEWAY_PROVIDER_ID>` or `<REVIEWER_GATEWAY_PROVIDER_ID>`; do this only when the
number changes a decision.

## Reviews

Nothing a builder produces is accepted on its own word. Every unit of work
gets an independent review before it merges.

- Seven of every ten reviews go to Sol and three to Claude on the builder account.
  Keep the tally in the progress file. With one reviewer per round, default
  to Sol and give Claude the rounds where a second kind of reader matters
  most: the final pass, a finding the builder disputes, anything Sol passed
  that still looks wrong to you. With several reviewers on one round, split
  that round 70/30.
- If the builder account is exhausted, the Claude share goes to Sol, not to the coordinator account.
- A reviewer is never the builder of the thing it reviews, and it gets the
  work, not your opinion of it: the brief, the diff or the artifact paths,
  and what done means.
- Ask for defects, not a score: up to five, ranked, each with the file and
  location, what is wrong, and why it matters. Scores do not converge.
- One review, the fixes, one confirming review, then close the item. Each
  round is a new `delegate_task` whose prompt carries the original brief, the
  earlier findings, what was done about each, and any objection still open.
  Do not continue a review by messaging the child's thread.
- Sol can look at images. Give it file paths; do not look yourself.

## Running to the end

The user starts a run and expects not to hear about it until it is done. A run
that stops early and waits for the user is the failure this workflow exists to
prevent.

- No time caps. Do not write "stop after N hours" into a goal, a plan or a
  child's brief. Usage limits are handled by the rules above, not by a clock.
- Never end a turn with nothing in flight before done is met: a child task
  or a background clock must be running, or the next step must be started
  in the same turn. A run whose last turn ends idle has stopped.
- Do not hand the user a choice the brief already answers or that a builder and
  a review can settle. Decide, record why in the progress file, go on.
  Stop only for what only the user can authorize: merging to main, spending money,
  anything outward-facing, or a change to what the work is.
- If an item will not pass, keep working it (diagnose, fix, review, measure
  again) until it passes or the evidence shows it cannot without breaking a
  rule. Report the second case at the end with that evidence; do not stop
  the rest of the run for it.
- If the coordinator account's weekly reading reaches 95% before the run is done, do not stop:
  hand coordination to a new thread on `<BUILDER_PROVIDER_ID>`
  through `t3_thread_launch`, briefed to resume from the progress file and
  to follow this skill, and record the handoff there.

## Finishing

- Run the checks you wrote down at the start, yourself, on the merged result.
- PRs: follow the repository's rules, call `link_pull_request` for every PR
  the run creates, and keep questions and asks for the user out of the PR.
- Report to the user: what is done and verified, what is left, the review tally,
  and the three usage readings at the end.

## Rules that do not bend

- Only use the accounts selected for this workflow. Keep unrelated employer
  accounts and their work separate.
- Never restart T3, change its providers, or alter remote-access services
  from a run. Follow the applicable local AGENTS.md instructions.
- Moving builders to the coordinator account while the builder account's window is closed, and back
  when it reopens, is the one account switch this workflow makes. Any other
  limit is reported, not routed around.
