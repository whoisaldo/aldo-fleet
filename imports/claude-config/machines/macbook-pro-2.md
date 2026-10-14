# Example control laptop

The laptop is a control and review device. Configure your own user, checkout, SSH aliases and addresses in fleet.json. Files on another worker belong to that worker's filesystem; do not assume paths are shared.

Use authorized SSH access for remote work. Keep each worker's T3 database, environment and account state separate. Native GPU/display tests run in the Windows worker's interactive session; macOS and iOS tests run on a configured Mac.

Choose personal or work identity at thread creation. Do not switch accounts or copy authentication into another profile. Author commits using the repository's human identity without agent attribution.
