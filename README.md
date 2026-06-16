# Dynamic DCA

A Bitcoin **risk indicator and dynamic dollar-cost-averaging dashboard**, built as a single static page and hosted on GitHub Pages.

**Live:** https://began2.github.io/Dynamic-DCA/

It measures how stretched BTC's price is from its long-term trend, normalizes that into a **0–1 risk score**, and turns the score into a DCA strategy: buy more when risk is low, ease off (or sell) when risk is high.

> Educational tool, not financial advice.

---

## What it shows

- **Price & Risk chart** — candlestick / line view of BTC with the long moving-average trend overlaid.
- **Buy Zones** — the price colored by risk (green = accumulate, red = sell).
- **Risk meter** — the current risk score, its band, and the suggested action.
- **Risk distribution** — how much of history BTC has spent in each band.
- **Strategy table** — bands, risk ranges, actions, and buy multipliers.
- **Risk-adjusted price levels** — what today's price would need to be to sit at each risk level.
- **Backtest** — Dynamic DCA vs. flat DCA over a date range, with daily / weekly / monthly / lump-sum contributions.

Chart extras: crosshair tooltip, zoom & pan, range presets, fullscreen, and drawing tools (trend, horizontal line, measure %, Fibonacci).

---

## How the risk model works

A normalized take on the Benjamin Cowen / Into the Cryptoverse risk metric:

1. Compute a long simple moving average of price.
2. `preavg = (ln(price) − ln(MA)) × index^k` — log-distance from the MA, with a time-decay factor so later, smaller cycles still register.
3. Normalize to 0–1 using an expanding (cumulative) min/max, so the score reflects only data known up to each point.

This is a simplified recreation, not the exact production metric — it captures the same shape (price oscillating through the bands each cycle) but won't match published numbers exactly.

---

## Data

- **History:** daily OHLC baked into [`btc-history.json`](btc-history.json), sourced from Bitstamp's public API.
- **Live price:** the latest close is fetched at load from CoinGecko and merged onto the baked history.

The committed history file plus one live price keeps the app fully static — no server or API keys needed.

---

## Tech

Plain HTML + vanilla JavaScript, no build step. Uses [TradingView Lightweight Charts](https://github.com/tradingview/lightweight-charts) for the price chart and [Chart.js](https://www.chartjs.org/) for the histogram, both via CDN. Everything else lives in [`index.html`](index.html).

---

## Run locally

`fetch()` of the local JSON won't work over `file://`, so serve over HTTP:

```bash
python -m http.server 8000
```

Then open http://localhost:8000.

---

## License

[MIT](LICENSE)
