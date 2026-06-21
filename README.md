# Dynamic DCA

A Bitcoin **risk indicator and dynamic dollar-cost-averaging dashboard**, built as a single static page and hosted on GitHub Pages.

**Live:** https://began2.github.io/Dynamic-DCA/

Risk is driven by the **MVRV Z-Score** -- an on-chain metric that measures how stretched Bitcoin's market cap is relative to its realized cap (the aggregate cost basis of all coins). A low Z-Score means BTC is undervalued vs. what people paid for it; a high Z-Score means the market is far above realized value. The score is normalized to 0-1 and turned into a DCA strategy: buy more when risk is low, ease off when risk is high.

> Educational tool, not financial advice.

---

## What it shows

- **Price chart** -- candlestick / line view of BTC with colored Buy Zones.
- **Buy Zones** -- price bands colored by MVRV Z risk (green = accumulate, red = sell).
- **Risk meter** -- the current risk score, its band, and the suggested action.
- **Risk distribution** -- how much of history BTC has spent in each band.
- **Strategy table** -- bands, risk ranges, actions, and buy multipliers.
- **Risk-adjusted price levels** -- what today's price would need to be to sit at each risk level.
- **Backtest** -- MVRV Z DCA vs. Buy & Hold over a date range.

Chart extras: crosshair tooltip, zoom & pan, range presets, fullscreen, drawing tools (trend line, horizontal line, measure box, Fibonacci), click-to-select and drag-to-resize drawings.

---

## How the risk model works

1. **MVRV Z-Score** is baked into `mvrv-history.json` from on-chain data (Coin Metrics community API).
2. The raw Z-Score is normalized 0-1 using an expanding cumulative min/max, so each day's score only reflects data known up to that point.
3. The normalized score maps to bands that drive buy multipliers (3x at Very Low risk, 0x at High, -1x at Extreme).

---

## Data

- **Price history:** daily OHLC baked into [`btc-history.json`](btc-history.json), sourced from Bitstamp's public API.
- **MVRV Z-Score:** baked into [`mvrv-history.json`](mvrv-history.json) from Coin Metrics community API. Re-run `bake_mvrv.py` to update.
- **Live price:** fetched at load from CoinGecko and merged onto the baked history.

---

## Tech

Plain HTML + vanilla JavaScript, no build step. Uses [TradingView Lightweight Charts](https://github.com/tradingview/lightweight-charts) for the price chart and [Chart.js](https://www.chartjs.org/) for the histogram, both via CDN.

---

## License

[MIT](LICENSE)
