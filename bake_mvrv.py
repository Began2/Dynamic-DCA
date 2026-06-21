"""
Bake the full-history MVRV Z-Score for BTC into mvrv-history.json.

Source: Coin Metrics community API (free, no key).
  - CapMVRVCur = MVRV ratio (MarketCap / RealizedCap) -- free on community tier

MVRV Z-Score = (MVRV - expanding_mean(MVRV)) / expanding_stdev(MVRV)

This is mathematically equivalent to the standard MVRV Z-Score and covers
the full Bitcoin history from 2011 to today.
"""
import urllib.request, json, time, sys, math

HOST = "https://community-api.coinmetrics.io/v4/timeseries/asset-metrics"
HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}


def call(url, retries=5):
    for a in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            return json.load(urllib.request.urlopen(req, timeout=60))
        except Exception as e:
            print(f"  attempt {a+1}/{retries} failed: {e}", flush=True)
            if a < retries - 1:
                time.sleep(10 * (a + 1))
    return None


def fetch_all():
    rows = {}
    for yr in range(2011, 2027):
        url = (f"{HOST}?assets=btc&metrics=CapMVRVCur&frequency=1d"
               f"&start_time={yr}-01-01&end_time={yr}-12-31&page_size=10000")
        r = call(url)
        if not r:
            print(f"FAILED year {yr}", flush=True)
            continue
        for x in r.get("data", []):
            d = x["time"][:10]
            mvrv = x.get("CapMVRVCur")
            if mvrv:
                rows[d] = {"t": int(time.mktime(time.strptime(d, "%Y-%m-%d"))),
                           "mvrv": float(mvrv)}
        print(f"{yr}: total {len(rows)}", flush=True)
        time.sleep(3)
    return rows


def compute_zscore(rows):
    """MVRV Z-Score = (mvrv - expanding_mean) / expanding_stdev."""
    ks = sorted(rows)
    vals = []
    out = []
    for k in ks:
        v = rows[k]["mvrv"]
        vals.append(v)
        n = len(vals)
        mean = sum(vals) / n
        if n > 1:
            var = sum((x - mean) ** 2 for x in vals) / n
            sd = math.sqrt(var)
        else:
            sd = 0.0
        z = (v - mean) / sd if sd > 0 else 0.0
        out.append({"t": rows[k]["t"], "z": round(z, 4)})
    return out


def main():
    print("Fetching MVRV ratio (CapMVRVCur) from Coin Metrics community API...", flush=True)
    rows = fetch_all()
    if not rows:
        print("NO DATA -- aborting", flush=True)
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
