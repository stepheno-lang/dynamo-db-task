A Python command-line tool located in `/app/project` analyzes software package dependency graphs stored as property graphs.

The implementation is intentionally incomplete. The current shortest-path algorithm incorrectly treats every dependency edge as valid and therefore produces dependency chains that violate repository and trust constraints.

Repair the existing implementation without changing the overall program structure.

The repaired analyzer must:

- compute the minimum-cost dependency path from the start package to the target package;
- ignore dependency edges whose target repository is not listed in `/app/data/rules.json`;
- ignore dependency edges whose target trust level is below the configured minimum;
- ignore optional dependencies when `allow_optional` is false;
- preserve the existing command-line interface.

After repairing the analyzer, execute the program and produce the following files:

- `/app/output/path.json`
- `/app/output/summary.json`
- `/app/output/validation.json`

`path.json` must contain the selected dependency chain.

`summary.json` must contain:

- total_cost
- path_length
- valid

`validation.json` must contain:

- constraints_satisfied
- minimum_cost

Do not modify the input data in `/app/data`.