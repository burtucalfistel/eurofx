#!/usr/bin/env python3
"""eurofx — fetch ECB reference rates and compare currencies over time.

Small CLI around the ECB's public XML feed (no API key):

    eurofx latest          # today's reference rates
    eurofx compare USD 90  # EUR/USD, 90-day trend + min/max/avg
    eurofx convert 100 USD # convert 100 EUR -> USD at the latest rate
"""
from __future__ import annotations
import argparse
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

FEED = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml"
NS = "{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}"


def _series() -> list[tuple[str, dict[str, float]]]:
    with urllib.request.urlopen(FEED, timeout=20) as r:
        root = ET.fromstring(r.read())
    out = []
    for time_el in root.iter(f"{NS}Cube"):
        d = time_el.get("time")
        if not d:
            continue
        rates = {"EUR": 1.0}
        for c in time_el:
            rates[c.get("currency")] = float(c.get("rate"))
        out.append((d, rates))
    return sorted(out)


def latest(ccy: str) -> float:
    series = _series()
    _, rates = series[-1]
    if ccy not in rates:
        raise SystemExit(f"no rate for {ccy} on {series[-1][0]}")
    return rates[ccy]


def cmd_latest():
    d, rates = _series()[-1]
    print(f"ECB reference rates — {d}")
    for c, v in sorted(rates.items()):
        if c != "EUR":
            print(f"  EUR/{c:<3} {v:.4f}")


def cmd_compare(ccy: str, days: int):
    series = _series()[-days:]
    vals = [(d, r[ccy]) for d, r in series if ccy in r]
    if not vals:
        raise SystemExit(f"no data for {ccy}")
    first, last = vals[0], vals[-1]
    nums = [v for _, v in vals]
    chg = (last[1] / first[1] - 1) * 100
    print(f"EUR/{ccy} over {len(vals)} sessions")
    print(f"  first {first[0]} {first[1]:.4f}")
    print(f"  last  {last[0]} {last[1]:.4f}  ({chg:+.2f}%)")
    print(f"  min {min(nums):.4f}  max {max(nums):.4f}  avg {sum(nums)/len(nums):.4f}")


def cmd_convert(amount: float, ccy: str):
    rate = latest(ccy)
    print(f"{amount:.2f} EUR = {amount * rate:.2f} {ccy}")


def main(argv=None):
    p = argparse.ArgumentParser(prog="eurofx")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("latest")
    c = sub.add_parser("compare"); c.add_argument("currency"); c.add_argument("days", type=int, nargs="?", default=90)
    v = sub.add_parser("convert"); v.add_argument("amount", type=float); v.add_argument("currency")
    ns = p.parse_args(argv)
    if ns.cmd == "latest": cmd_latest()
    elif ns.cmd == "compare": cmd_compare(ns.currency.upper(), ns.days)
    elif ns.cmd == "convert": cmd_convert(ns.amount, ns.currency.upper())


if __name__ == "__main__":
    sys.exit(main())
