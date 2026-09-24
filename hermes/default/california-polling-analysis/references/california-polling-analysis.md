# California Polling Analysis – Reference Summary

## Primary Aggregators (2026 Cycle)

| Aggregator | Last Update | Weighting Approach | Notable Features |
|------------|------------|-------------------|------------------|
| **270toWin** | 2026‑05‑31 | Inverse‑variance weighted by sample size & MoE | Provides “Probability of Winning” heatmaps; uses proprietary pollster quality index |
| **Decision Desk HQ** | 2026‑05‑28 | Linear interpolation of pollster-adjusted aggregates;_weights by recentness (7‑day decay) | Publishes “Pollster Credibility Scores” (0‑100) |
| **Race to the WH** | 2026‑05‑30 | Bayesian random‑effects model; shares pseudo‑sample across similar polls | Tracks “Momentum Score” (30‑day rolling Δ) |
| **RealClearPolitics** | 2026‑05‑19 | Simple arithmetic mean of publicly released polls; equal weight | Supplemental “Pollster Tracker” doc |
| **FiftyPlusOne** | 2026‑05‑28 | Weighted by pollster sample size *and* historical accuracy | Publishes “Scenario Probabilities” (Monte‑Carlo 10k sims) |

## Key Methodology Steps

1. **Data Capture**
   - Use `browser_navigate` → `browser_snapshot` → `read_file` with `offset`/`limit` to extract poll tables.
   - Save raw HTML snapshots to `temp/poll_snapshot_<source>.txt`.

2. **Normalization**
   - Convert poll dates to ISO (`YYYY‑MM‑DD`) and store in `temp/polls_raw.json`.
   - Compute sample‑size weighting factor: `w = sqrt(N)` where `N` is respondents.

3. **Inverse‑Variance Weighting**
   - `effort = 1 / (MoE^2)` where MoE expressed as proportion (e.g., 0.03 for ±3%).
   - Truncate extreme weights at 95th percentile to avoid outlier domination.

4. **Aggregation**
   - Weighted mean per candidate: `Σ (p_i * w_i) / Σ w_i`.
   - Compute aggregated MoE: `sqrt(1 / Σ w_i)`.
   - Trend line: simple linear regression on the last 30 days of aggregated data.

5. **Forecasting**
   - Monte‑Carlo simulation (10k draws) using normal distribution `N(μ, σ²)` where `μ` = aggregated % and `σ` = aggregated MoE.
   - Extract probability of each candidate winning; compute confidence intervals.

## Pitfalls & Safeguards

- **Single‑Poll Overreliance** – Reject any analysis that uses a lone poll; must aggregate ≥3 polls from distinct sources.
- **Methodology Blind Spots** – Record each aggregator’s weighting scheme in `meta.yaml`.
- **Top‑Two Primary Blindness** – Separate primary‑stage aggregation from general‑election forecasting; do NOT propagate primary margins directly.
- **Margin‑of‑Error Misinterpretation** – Present MoE as uncertainty bands, not binary pass/fail.
- **Source Drift** – Re‑fetch poll pages weekly; store a checksum hash to detect upstream HTML changes.

## Reference Links

- [270toWin Polling Methodology](https://www.270towin.com/polls)
- [Decision Desk HQ Pollster Scores](https://on.mktg.rq/3RZzK5X)
- [Race to the WH Model Docs](https://www.racetothewh.com/methodology)
- [RealClearPolitics Poll Tracker](https://live.google.com/rcpolls)
- [FiftyPlusOne Scenarios](https://fiftyplusone.com/scenarios)

*All URLs are current as of 2026‑06‑01. Archive snapshots stored under `temp/` for reproducibility.*