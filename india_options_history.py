# india_options_history.py
import argparse, time, math, sys
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, MONTHLY, WEEKLY, TH
import pandas as pd
from pathlib import Path
from tenacity import retry, wait_exponential, stop_after_attempt
from tqdm import tqdm

# --- install hints for Cursor (handled by tool) ---
# pip: nsepy==0.8 pandas>=2.0 pyarrow tenacity python-dateutil tqdm

try:
    from nsepy import get_history
    from nsepy.derivatives import get_expiry_date
except Exception as e:
    print("Import error: make sure nsepy installed. Error:", e)
    sys.exit(1)

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", nargs="+", default=["NIFTY", "BANKNIFTY"])
    ap.add_argument("--start", type=str, required=True)
    ap.add_argument("--end", type=str, required=True)
    ap.add_argument("--outdir", type=str, default="./data")
    ap.add_argument("--monthlies-only", action="store_true")
    return ap.parse_args()

def daterange(d0, d1):
    cur = d0
    while cur <= d1:
        yield cur
        cur += timedelta(days=1)

def month_ends(start, end):
    """All month-end expiry Thursdays via NSE's helper."""
    months = list(rrule(freq=MONTHLY, dtstart=start.replace(day=1), until=end))
    for dtm in months:
        y, m = dtm.year, dtm.month
        try:
            yield get_expiry_date(year=y, month=m)
        except Exception:
            # fallback: last Thursday of month
            last = list(rrule(freq=WEEKLY, byweekday=TH,
                              dtstart=dtm.replace(day=1),
                              until=(dtm + relativedelta(day=31))))
            if last:
                yield last[-1].date()

def weekly_thursdays(start, end):
    for th in rrule(freq=WEEKLY, byweekday=TH, dtstart=start, until=end):
        yield th.date()

@retry(wait=wait_exponential(multiplier=1, min=1, max=10), stop=stop_after_attempt(5))
def safe_get_history(**kwargs):
    df = get_history(**kwargs)
    # nsepy sometimes returns None; turn into empty DataFrame
    return df if isinstance(df, pd.DataFrame) else pd.DataFrame()

def fetch_underlying(symbol, start, end, is_index):
    df = safe_get_history(symbol=symbol, start=start, end=end, index=is_index)
    if df.empty:
        return pd.DataFrame()
    return df.reset_index()[["Date","Close"]].rename(columns={"Close":"underlying_close"})

def round_to_nearest_50(x):
    return int(50 * round(float(x)/50.0))

def discover_strikes(symbol, expiry, start, end, is_index):
    """Find a reasonable strike band per expiry by walking around ATM."""
    ul = fetch_underlying(symbol, start, end, is_index)
    if ul.empty: 
        return []
    atm = round_to_nearest_50(ul["underlying_close"].median())
    strikes = set()
    # search ±40 steps of 50 (i.e., ±2000 points) with early stop
    misses_in_row = 0
    step = 0
    while step <= 40 and misses_in_row < 6:
        for delta in (step, -step) if step else (0,):
            k = atm + 50*delta
            df = safe_get_history(symbol=symbol, start=start, end=end,
                                  index=is_index, option_type="CE",
                                  strike_price=k, expiry_date=expiry)
            if not df.empty:
                strikes.add(k); misses_in_row = 0
            else:
                misses_in_row += 1
            time.sleep(0.7)
        step += 1
    return sorted(strikes)

def fetch_one_combo(symbol, expiry, k, opt, start, end, is_index):
    df = safe_get_history(symbol=symbol, start=start, end=end, index=is_index,
                          option_type=opt, strike_price=k, expiry_date=expiry)
    if df.empty:
        return df
    keep = df.reset_index().rename(columns={"Date":"date"})
    cols = ["date","Open","High","Low","Close","Number of Contracts",
            "Turnover","Open Interest","Change in OI"]
    keep = keep[cols]
    keep.columns = ["date","open","high","low","close",
                    "number_of_contracts","turnover","open_interest","change_in_oi"]
    keep["symbol"] = symbol
    keep["is_index"] = is_index
    keep["expiry"] = expiry
    keep["option_type"] = opt
    keep["strike"] = k
    return keep

def main():
    args = parse_args()
    start = datetime.strptime(args.start, "%Y-%m-%d").date()
    end   = datetime.strptime(args.end,   "%Y-%m-%d").date()
    outdir = args.outdir
    Path(outdir).mkdir(parents=True, exist_ok=True)
    Path(f"{outdir}/parquet").mkdir(parents=True, exist_ok=True)

    grand = []
    for sym in args.symbols:
        is_index = sym in ("NIFTY","BANKNIFTY","NIFTY 50","NIFTY BANK")
        # expiries
        exps = list(month_ends(start, end))
        if not args.monthlies_only and is_index:
            exps = sorted(set(exps).union(weekly_thursdays(start, end)))
        # restrict expiries to within range
        exps = [e for e in exps if start <= e <= end]
        print(f"{sym}: {len(exps)} expiries to try")

        for exp in tqdm(exps, desc=f"{sym} expiries"):
            # nsepy requires start<=end; ensure we look back ~60 trading days prior to expiry
            s_win = max(start, exp - relativedelta(months=2))
            ul = fetch_underlying(sym, s_win, exp, is_index)
            if ul.empty:
                continue

            strikes = discover_strikes(sym, exp, s_win, exp, is_index)
            if not strikes:
                continue

            part = []
            for opt in ("CE","PE"):
                for k in strikes:
                    df = fetch_one_combo(sym, exp, k, opt, s_win, exp, is_index)
                    if not df.empty:
                        part.append(df)
                    time.sleep(0.7)
            if not part:
                continue

            df_exp = pd.concat(part, ignore_index=True)
            # merge underlying close for moneyness
            df_exp = df_exp.merge(ul, left_on="date", right_on="Date", how="left").drop(columns=["Date"])
            df_exp["moneyness"] = df_exp["underlying_close"] / df_exp["strike"]
            # write parquet per expiry
            pq_path = f"{outdir}/parquet/{sym}_{exp.isoformat()}.parquet"
            df_exp.to_parquet(pq_path, index=False)
            grand.append(df_exp)

        if grand:
            all_sym = pd.concat([g for g in grand if g["symbol"].iloc[0]==sym], ignore_index=True)
            # de-dupe & sort
            all_sym = (all_sym
                       .drop_duplicates(subset=["date","symbol","expiry","option_type","strike"])
                       .sort_values(["date","expiry","option_type","strike"]))
            csv_path = f"{outdir}/{sym}_options_daily.csv"
            all_sym.to_csv(csv_path, index=False)
            print(f"{sym}: wrote {len(all_sym):,} rows to {csv_path}")

    if grand:
        all_df = pd.concat(grand, ignore_index=True)
        print("TOTAL rows:", len(all_df))
    else:
        print("No data downloaded (check dates/symbols).")

if __name__ == "__main__":
    main()
