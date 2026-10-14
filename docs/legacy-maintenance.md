# Legacy maintenance reference

Use the current [maintenance guide](maintenance.md) for supported commands. Older helpers are retained for adaptation, not automatic execution.

Skill migration requires an authorized idle window. Preview the change, preserve unrelated settings and histories, and retain a private backup manifest. Exempt only the maintenance thread from activity checks. New unused profiles can use ordinary `fleet apply`; native homes and profiles with history remain protected.

Keep dependency caches outside immutable releases. macOS can use symlinks and Windows directory junctions to provide one canonical custom skill source. Provider-managed skills and plugins remain under their own managers.

Preserve T3's existing application, service ownership, provider entries and database. Never launch a second backend against a live home. Use supported settings APIs for additive changes; neither a skill update nor a quota reset requires restarting the app. Keep remote service recovery procedures in private machine notes.
