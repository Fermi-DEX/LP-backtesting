# Fermi LP backtesting evidence

Evidence package prepared on 2026-10-19. Publication destination: https://github.com/Fermi-DEX/LP-backtesting.

**Historical fee-adjusted returns remain unavailable. This package does not support an investor-facing return table.** It contains an offline accounting tool, tests, selected reported aggregates, provenance, and explicitly hypothetical sensitivities. No historical run was fabricated or rerun.

The September 26 robust policy report gives approximately $150 per market-day at $100,000 test capital, or $115 under 4x hedge impact. Both exclude Fermi trading fees/rebates and terminal closeout. The correct adjustment is:

`adjusted marked PnL = base marked PnL + 0.0003 * Fermi maker executed USD notional - 0.0006 * Fermi taker executed USD notional`

The protocol's taker fee is not extra LP revenue. External hedge fees are already in base marked PnL. Executed volume is price times base quantity, not collateral or margin. Counterparties taking the LP's quotes produce LP maker volume.

## Reproduce the deliverable

Python 3.11+; no installs, network, wallet, credentials, or API calls:

```sh
python -m unittest discover -s tests -v
python fee_adjust.py data/sensitivity_inputs.json --output sensitivity_check.json
cmp data/sensitivity_results.json sensitivity_check.json
```

For recovered runs, supply a JSON array using the input keys in `data/sensitivity_inputs.json`, replace all illustrative values with audited run values, and set an accurate status. The CLI requires explicit fee exclusion and executed-notional basis. It outputs only whitelisted accounting fields; metadata and component reconciliation belong in the evidence ledger described in METHODOLOGY.md. Never relabel sensitivity rows as historical runs. `executed_volumes` accepts normalized Fermi executions, and `adjusted_curve` supports sampled drawdown when timestamped cumulative executions and base equity exist.

The tool is a post-hoc accounting adjustment. Fees do not feed back into strategy sizing, risk limits, or fill decisions. A fee-aware strategy rerun is a separate validation requirement. Source bot files have not been modified or copied into this package.

See METHODOLOGY.md for accounting and scaling limits, PROVENANCE.md for source and missing inputs, RIGHTS.md for redistribution scope, and data/reported_aggregates.csv for rounded source facts. All sensitivity volumes are assumptions, not measurements.
