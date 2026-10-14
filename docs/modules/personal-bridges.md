# Personal image, 3D and browser QA bridges

Keep these if you want Claude to coordinate specialized native Codex work. Skip them when built-in image/3D/browser tools are enough or when working in an employer environment.

The bank keeps codex-image, codex-3d and codex-computer-use, including older standalone scripts, examples, tests and references. They use a Mac/POSIX worker with your own native personal Codex authentication. From Windows, explicitly configure a compatible worker rather than assuming the source owner's SSH alias exists.

Keep their explicit model and reasoning requirements intact. On an access failure, report the actual error instead of switching accounts or models. The `.claude-only` marker excludes these bridges from Codex and non-personal fleet profiles.

Read each SKILL.md for dependencies and usage. A skill selection is not permission to install browser/Blender helpers into an existing live environment or modify a shared process. Check a small output and its artifact paths before using the workflow in your project.
