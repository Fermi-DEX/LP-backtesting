# Provenance and reproducibility gaps

Inspection date: 2026-10-19. Connected GitHub identity: cryptohariseldon. Destination Fermi-DEX/LP-backtesting was read-only verified as public, size 0, with an empty-repository response from its contents endpoint. It was created by the user. The user subsequently approved this reviewed package for publication.

## Sources

- [Historical report](https://github.com/cryptohariseldon/mm-bot-new/blob/e59a2a4b179963578aed629c806535e8522c7f0b/testing-results-3-report.md): rounded primary aggregate evidence.
- [Round 3 setup and caveats](https://github.com/cryptohariseldon/mm-bot-new/blob/e59a2a4b179963578aed629c806535e8522c7f0b/testing-results-3.md): validation design, capital caveat and rejected policy.
- [Current recorded-flow accounting](https://github.com/cryptohariseldon/mm-bot-new/blob/43292846e64ec0e0b954dc399eceb48303863f5e/mm/research/backtest.py): fill accounting, marked equity and report output.
- [Matrix](https://github.com/cryptohariseldon/mm-bot-new/blob/43292846e64ec0e0b954dc399eceb48303863f5e/mm/research/matrix.py): days, seeds, zero external depth, flow paths and output schema.
- [Hedge report runner](https://github.com/cryptohariseldon/mm-bot-new/blob/43292846e64ec0e0b954dc399eceb48303863f5e/mm/research/hedge_report.py): aggregate definitions and disabled streams.
- [Simulator](https://github.com/cryptohariseldon/mm-bot-new/blob/43292846e64ec0e0b954dc399eceb48303863f5e/mm/research/sim_exchange.py): relay fee charging and LP role flags.
- [Hedge model](https://github.com/cryptohariseldon/mm-bot-new/blob/43292846e64ec0e0b954dc399eceb48303863f5e/mm/hedge/phoenix_sim.py): historical cost assumptions (not asserted as current venue fees).
- [Dataset fetcher](https://github.com/cryptohariseldon/mm-bot-new/blob/43292846e64ec0e0b954dc399eceb48303863f5e/mm/research/datasources/binance_futures.py): rolling volume reference and seeded resampling.

Exact current branch heads and SHA-256 hashes of inspected files are recorded in provenance.json. 4329284 descends from bc1f2b4. Relevant backtest, matrix, simulator, fee overlay and robust policy overlay files do not differ between e59a2a4 and the research head; the Phoenix model import moved to a research interface. This does not establish that all other strategy dependencies are unchanged. Historical reproduction must pin the historical commit, not latest master.

## Search and missing inputs

No historical rows.json, fills.jsonl, lowfee_best.json or best.json was located in the accessible saved workspace and temporary directories; one daemon-owned temporary directory was unreadable and was not bypassed. No runs/ or data/ files were found in the inspected Git history. Both paths are ignored by source .gitignore. Remote workflow artifacts have not been exhaustively searched: the repository-wide artifact URL was rejected by the connector's endpoint allowlist. No claim is made about inaccessible external machines or backups.

To recover the original results, provide:

1. Original `runs/.../rows.json` and per-run report.json, with full-precision filled notionals, LP maker/taker split, and exact run parameters. If fill streams exist, provide complete timestamped executions and equity samples. Aggregated scalar reports alone cannot reconstruct fee-adjusted drawdown.
2. Fifteen original `data/flow/{sol,eth,btc}-{date}/` datasets for the five dates, including manifests, fills/oracle/funding series and checksums. Pin original sampling seed, probability, 365-day reference volume and as-of date, clipping/filter parameters, exact start/end timestamps, and source data provenance.
3. Exact source commit and full config snapshot used to produce the reported runs. Committed quote and robust hedge overlays exist; raw optimization outputs and dataset manifests do not.
4. Capital ledger for both venues, collateral rules and liquidation assumptions, final positions/marks, closeout-cost assumptions, vault idle reserve and fee/expense policy.
5. Redistribution permission/terms for any raw dataset before it is added to a public payload.

## Faithful rerun assessment

Not presently reproducible from available inputs. The original dataset directory is absent. The fetcher can download free keyless Binance archives, but its default `median_daily_usd` uses the most recent 365 complete days; fetching now silently changes the sampling probability unless the original reference is supplied. Funding-fetch failure can return an empty series, another reason manifests and validation matter. No paid API, data download, wallet call or strategy execution was performed.

When the missing audited datasets and config are restored in a separate source checkout pinned to e59a2a4, the documented base command is:

```sh
python -m mm.research.hedge_report --fee-cap 33.33 --equities 100000 --seeds 1 2 3 --versions phoenix phoenix_4x --quote-params config/overlays/fee100_quote.json --policy-100000 config/overlays/hedge_phoenix_100k.json --out runs/lp-validation
```

This command is conditional guidance, not a successful execution record. Before running, inspect dependencies in that pinned checkout and validate dataset hashes. Extend report output to preserve maker/taker executed volumes and sampled cumulative volumes (or enable streams via the matrix API). Then normalize into the fee_adjust.py schema, retain base marked PnL, and reconcile every component. A separate fee-aware rerun must feed trading costs into equity/risk decisions to assess behavioral effects.
