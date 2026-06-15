# Dynamic DCA

A Bitcoin **risk indicator and dynamic dollar-cost-averaging dashboard**, built as a single static page and hosted on GitHub Pages.

**Live:** https://began2.github.io/Dynamic-DCA/

It fits a log-regression trend to 14+ years of daily BTC price history, normalizes how far price sits above or below that trend into a **0–1 risk score**, and turns that score into a DCA strategy: buy more when risk is low, ease off (or sell) when risk is high.

> Educational tool, not financial advice.

---

## What it shows

- **Price & Risk chart** — candlestick / line view of BTC with the log-regression *Fair Value* trend line overlaid.
- **Buy Zones mode** — the price chart colored into accumulation bands (deep green = buy hard, red = sell), curving up with the regression.
- **Risk meter** — the current 0–1 risk score, its band (Very Low → Extreme), and the suggested action.
- **Risk distribution** — how much of history BTC has spent in each risk band.
- **Strategy table** — the bands, their risk ranges, actions, and buy multipliers.
- **Backtest** — Dynamic DCA vs. flat DCA over a date range you choose, with daily / weekly / monthly / lump-sum contributions.

### Chart tools
Candles ↔ line toggle · Buy Zones · optional risk line · always-on crosshair tooltip (O/H/L/C, Fair Value, risk) · log price scale · zoom & pan · range presets (1Y / 3Y / 5Y / All) with smooth animation · drawing tools (trend line, horizontal line, measure %, Fibonacci retracement) — hold and drag to draw.

---

## How the model works

1. **Fit a trend.** Ordinary least-squares regression on log-log axes:
   `ln(price) = slope · ln(daysSinceGenesis) + intercept`
   (genesis = 2009-01-03). This is the long-run growth curve — the *Fair Value* line.
2. **Measure deviation.** For each day, `dev = ln(price / trend)` — how far above/below the curve price sits.
3. **Normalize to 0–1.** Min/max scale the deviation across all history into a risk score. 0 = the cheapest BTC has ever been relative to trend, 1 = the most expensive.
4. **Map to a strategy.** Lower risk → larger buy multiplier; higher risk → reduce or sell.

> The risk score is always *relative to the data window it's fit on*. Adding more early history shifts the regression and the normalization, so the same day can read a different score.

### Strategy bands

| Band      | Risk range | Action          | Multiplier |
|-----------|------------|-----------------|------------|
| Very Low  | 0.00–0.20  | Accumulate Hard | 3.0×       |
| Low       | 0.20–0.40  | Accumulate      | 2.0×       |
| Moderate  | 0.40–0.55  | DCA Normal      | 1.0×       |
| Elevated  | 0.55–0.70  | Reduce / Hold   | 0.5×       |
| High      | 0.70–0.85  | Take Profits    | 0×         |
| Extreme   | 0.85–1.01  | Sell / Exit     | −1.0×      |

---

## Data

- **History:** ~5,390 daily OHLC bars from **2011-09-13 to today**, baked into [`btc-history.json`](btc-history.json) (sourced from Bitstamp's public OHLC API; a handful of early thin-liquidity flash-print wicks are clamped).
- **Live price:** the latest close is fetched at load from the free CoinGecko `simple/price` endpoint and appended/updated onto the baked history.

This hybrid approach (committed history file + one live price) is what keeps the app fully static — no server, no API keys, no CORS problems on GitHub Pages.

---

## Tech

- Plain HTML + vanilla JavaScript, no build step.
- [TradingView Lightweight Charts](https://github.com/tradingview/lightweight-charts) (v4.1.3) for the price chart.
- [Chart.js](https://www.chartjs.org/) (v4.4.0) for the risk-distribution histogram.
- Both loaded from CDNs; everything else is in [`index.html`](index.html).

---

## Run locally

`fetch()` of the local JSON won't work over `file://`, so serve the folder over HTTP:

```bash
python -m http.server 8000
```

Then open http://localhost:8000.

---

## Updating the history file

Re-bake `btc-history.json` from Bitstamp by paging its daily OHLC endpoint
(`/api/v2/ohlc/btcusd/?step=86400`), writing each bar as `{t,o,h,l,c}` with `t`
in **seconds** (Lightweight Charts requires seconds, not milliseconds).

---

## License

[MIT](LICENSE)
