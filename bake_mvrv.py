"""
Bake the full-history MVRV Z-Score for BTC into mvrv-history.json.

Source: Coin Metrics community API (free, no key).
  - CapMrktCurUSD = market cap (price x supply)
  - CapRealUSD    = realized cap (each coin valued at its last on-chain move)

MVRV Z-Score = (MarketCap - RealizedCap) / stdev(MarketCap, expanding)

The community tier throttles hard, so we (1) wait until it responds, then
(2) page year-by-year with cooldowns. Output is a static file the site reads
directly -- no live API calls from the browser.
"""
import urllib.request, json, time, sys, statistics, math

HOST = "https://community-api.coinmetrics.io/v4/timeseries/asset-metrics"
HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}


def call(url, retries=4):
    for a in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            return json.load(urllib.request.urlopen(req, timeout=60))
        except Exception as e:
            print(f"  attempt {a+1}/{retries} failed: {e}", flush=True)
            time.sleep(20 * (a + 1))
    return None


def wait_for_api():
    """Block until a tiny probe request succeeds."""
    probe = (f"{HOST}?assets=btc&metrics=CapRealUSD&frequency=1d"
             f"&start_time=2024-06-01&end_time=2024-06-02")
    n = 0
    while True:
        try:
            req = urllib.request.Request(probe, headers=HEADERS)
            json.load(urllib.request.urlopen(req, timeout=30))
            print("API_RECOVERED", flush=True)
            return
        except Exception as e:
            n += 1
            print(f"  waiting for API ({n}): {e}", flush=True)
            time.sleep(45)


def fetch_all():
    rows = {}
    for yr in range(2011, 2027):
        url = (f"{HOST}?assets=btc&metrics=CapMrktCurUSD,CapRealUSD&frequency=1d"
               f"&start_time={yr}-01-01&end_time={yr}-12-31&page_size=10000")
        r = call(url)
        if not r:
            print(f"FAILED year {yr}", flush=True)
            continue
        for x in r.get("data", []):
            d = x["time"][:10]
            mc = x.get("CapMrktCurUSD")
            rc = x.get("CapRealUSD")
            if mc and rc:
                rows[d] = {"t": int(time.mktime(time.strptime(d, "%Y-%m-%d"))),
                           "mc": float(mc), "rc": float(rc)}
        print(f"{yr}: total {len(rows)}", flush=True)
        time.sleep(8)
    return rows


def compute_zscore(rows):
    """MVRV Z = (MarketCap - RealizedCap) / expanding-stdev(MarketCap)."""
    ks = sorted(rows)
    mcs = []
    out = []
    for k in ks:
        mc = rows[k]["mc"]
        mcs.append(mc)
        sd = statistics.pstdev(mcs) if len(mcs) > 1 else 0.0
        z = (mc - rows[k]["rc"]) / sd if sd > 0 else 0.0
        out.append({"t": rows[k]["t"], "z": round(z, 4)})
    return out


def main():
    wait_for_api()
    rows = fetch_all()
    if not rows:
        print("NO DATA — aborting", flush=True)
        sys.exit(1)
    z = compute_zscore(rows)
    json.dump(z, open("mvrv-history.json", "w"), separators=(",", ":"))
    ks = sorted(rows)
    zs = [x["z"] for x in z]
    print(f"DONE rows={len(z)} range={ks[0]}..{ks[-1]} "
          f"z_min={min(zs):.2f} z_max={max(zs):.2f} z_current={zs[-1]:.2f}",
          flush=True)


if __name__ == "__main__":
    main()
