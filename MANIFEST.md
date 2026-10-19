# Publication payload manifest

This is the complete intended payload. Only these 13 files are in scope. No source checkout, .git history, Python bytecode, local audit output, environment file or other workspace content is included. SHA-256 hashes and scan evidence are retained in a separate local review record, excluded from this publication payload.

| File | Exactly what it discloses | Provenance and redistribution assessment |
|---|---|---|
| MANIFEST.md | Exact publication allowlist and file-by-file disclosure/rights summary | Newly authored audit metadata |
| LICENSE | MIT license for fee_adjust.py and tests/test_fees.py only | Owner-approved licensing for newly authored code |
| .gitignore | Exclusion patterns for local bytecode, environment and private/run data | Newly authored; no third-party content |
| README.md | Evidence status, accounting formula, reproduction commands, destination URL and limitations | Original analysis and public report facts |
| METHODOLOGY.md | Selected dates/markets/seeds, rounded primary aggregate statistics, accounting audit, missing capital/volume data, conditional fee and volume sensitivities | Original analysis; public factual aggregates attributed in PROVENANCE.md; no strategy source or configurations copied |
| PROVENANCE.md | Source URLs/commits, branch relationship, search scope, missing inputs, conditional original-harness invocation, connected public GitHub username and destination status | Original audit notes; public source references; no credentials or private identifiers |
| RIGHTS.md | Publication scope, no source license found, no copied upstream code/data, MIT license limited to newly authored code | Newly authored rights assessment |
| provenance.json | Branch names/full commit IDs, inspected source-path hashes, inspection date and evidence-status flags | Public repository metadata; no file contents copied |
| fee_adjust.py | Generic Fermi fee arithmetic, input guards, execution notional helper, sampled drawdown helper and offline CLI | Newly authored standard-library code; no upstream source copied |
| tests/test_fees.py | Twelve synthetic accounting test cases, including rates, exclusions, errors and drawdown | Newly authored; synthetic numbers |
| data/reported_aggregates.csv | Two rows of rounded robust-policy report statistics; unknown volume/collateral/adjusted results left blank | Selected publicly reported factual aggregates, linked source; not independently reproduced |
| data/sensitivity_inputs.json | Ten explicitly hypothetical base-PnL/maker/taker/capital/day combinations | Newly authored assumptions; base means attributed to source |
| data/sensitivity_results.json | Deterministic outputs of the fee tool for those ten assumptions, including mechanical annualizations | Newly computed sensitivity, not historical data; no vault APR asserted |

Privacy inspection found no wallet addresses, customer data, counterparty identities, private operational endpoints, credentials, raw fills, production logs or third-party data files in these files. Automated patterns and manual inspection are limited checks, not proof that unknown secrets cannot exist. The user approved publication of this package and MIT licensing for newly authored code.
