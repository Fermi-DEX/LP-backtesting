# Accounting and interpretation

## Evidence available

The source report describes SOL, ETH and BTC; seeds 1, 2, 3; five selected dates: calm 2026-08-15, typical 2026-09-20, downtrend 2026-02-05, uptrend 2026-09-18, cascade 2025-10-10. Each policy row covers 45 market/date/seed observations, not 45 independent days. Exact start/end timestamps and durations require the missing manifests. Report dated 2026-09-26; containing historical commit dated 2026-09-28.

The primary policy uses $100,000 starting test equity per market ($300,000 across three independently simulated markets), Phoenix hedge impact at 2x or 4x, and rebalance at 1x N_soft. Separately funded hedge collateral is not modeled or established. The simulator tracks hedge cash and position but has no demonstrated collateral lock, margin sufficiency, or liquidation simulation for that leg.

| Reported metric | Robust 2x impact | Robust 4x impact |
|---|---:|---:|
| Mean marked PnL, USD/market-day | 150 | 115 |
| Worst individual run PnL, USD | -3103 | -2990 |
| Runs with PnL >= 0, rounded | 58% | 56% |
| Gross maker edge, mean USD | 428 | 424 |
| Relay fees, mean USD | 31 | 31 |
| Hedge fees plus impact, mean USD | 151 | 195 |
| Hedge marked PnL, mean USD | 37 | 105 |
| Largest sampled run drawdown, USD | 4818 | 4285 |
| Peak absolute Fermi position, USD | 139912 | 139912 |

Figures are rounded source aggregates, before Fermi trading fees/rebates. Neither losses nor drawdowns can be fee-adjusted from the table alone. Final inventory marks and individual funding components are missing. Gross maker edge is a fill-time diagnostic; it does not reconcile by simple subtraction to final marked PnL. The rejected $1,260/day policy retained directional hedges and is not a basis for fund estimates.

## Accounting audit

`FlowBacktest._equity` computes initial equity + Fermi cash PnL + signed Fermi inventory at oracle - relay fees + hedge mark. Fermi cash includes proxy funding. Phoenix hedge mark already includes execution impact in fill prices, fees, transaction costs, funding, and marked open inventory. Do not subtract those costs again. Do not add gross edge to cash PnL. Do not call `RunReport.finalize()` on marked backtest results: its generic edge-minus-fees calculation replaces the inventory-aware PnL.

The simulator's `fees_usd_total` charges operations or batches; these are relay fees, not the requested 6 bps/3 bps trading schedule. Apply trading fees to each LP execution's `price * size`. Keep external Phoenix executions outside these Fermi volumes. A `taker_flow` tag labels the counterparty action, while `is_taker` labels the LP role.

The historical matrix fixes `ext_depth_usd=0`; its LP IOC path cannot execute with zero external depth. Thus Fermi taker volume is expected to be zero under that exact model. This is a code-based inference, not recovered execution evidence. Maker volume still cannot be recovered from edge or venue target volume. If raw matrix rows are recovered, `fills_notional` is rounded to whole dollars; prefer full run reports or fills for precise fees. The report runner disables fill streams by default, so a `fills.jsonl` file may never have been written.

Correct per-run post-hoc result: `P' = P + 0.0003*M - 0.0006*T`. With complete time series, add cumulative fee adjustments to each corresponding marked equity sample, then calculate maximum running-peak-minus-equity. Sampled drawdown can miss intratick losses. Initial equity must be included. Deduplicate fills upstream using actual execution identifiers, not order IDs (partial fills can share order IDs). Do not count both maker and taker sides as LP executions.

A complete run evidence ledger needs run ID, source commit, config/dataset hashes, market, seed, UTC start/end, elapsed days, initial capital, initial inventory, separately required hedge collateral, Fermi maker/taker volumes, gross edge, cash trade PnL, Fermi funding, relay fees, hedge fees/impact/funding/marked PnL, both final signed inventory marks, realized/marked PnL, terminal liquidation cost, equity curve, peak exposure, drawdown, and loss outcomes. Missing values must remain unknown, never zero by default.

## Annualization and fund scaling

For one run: simple annualized test-capital return (%) = `100 * adjusted PnL / initial test capital * 365 / elapsed days`. For a comparable-capital collection: `100 * 365 * sum(adjusted PnL) / sum(initial capital * elapsed days)`. Seeds are alternative paths, not additive allocations. No compounded APY is asserted. The selected dates are not a representative year or an out-of-sample estimate.

Mechanical annualization of the unadjusted rounded means is 54.75% (150*365/100000) or 41.975% (115*365/100000). These are not funded-vault APRs, not fee-adjusted historical results, and do not verify the recalled 17–25% range. A vault denominator must include idle capital, reserves and required hedge collateral without double counting collateral already inside deposits; numerator must include closeout, management/operating costs, and any performance fees. All are unresolved here.

No supported mapping exists from this test to $250k, $1M or $2.5M deposits. Scaling changes participation, inventory risk and hedge impact. The prior 1.6x daily turnover cap and 2 bps net edge are unverified and are not used.

No supported return estimates exist for $2M, $20M, $50M or $100M venue daily volume. The source uses approximately $2M median-day proxy flow per sampled symbol, not guaranteed LP fills or a verified venue-wide aggregate. An increase in venue volume does not determine this LP's capture share. Fee-only algebra at venue volume V, LP maker participation c and LP taker execution T is `0.0003*c*V - 0.0006*T`; c and T are unknown. At c=100% and T=0 the maker rebates would be $600/$6,000/$15,000/$30,000 per day, respectively. These are conditional fee-only illustrations, not PnL or achievable returns.

## Sensitivity, not recovered backtest results

For assumed maker/taker execution of $100,000/$0 per market-day, fees add $30: the two rounded base scenarios become $180/$145. For assumed $1M/$100k they add $240: $390/$355. For assumed $1M/$500k the fee adjustment is zero. The JSON files reproduce these scenarios and additional cases; they provide no evidence that those volumes occurred. Fee break-even is M=2*T. Terminal closeout remains excluded in every scenario.
