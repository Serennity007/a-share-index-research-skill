#!/usr/bin/env python3
"""Describe an explicitly supplied A-share constituent snapshot, not an index return."""
import argparse
from datetime import timedelta, timezone
from pathlib import Path
import re

from market_io import timestamp, number, records, provenance, emit, kind


def analyze(raw, as_of, universe_label, expected_count, data_kind):
    cutoff = timestamp(as_of)
    if not universe_label.strip() or expected_count <= 0:
        raise ValueError("declare the universe and positive expected member count")
    rows = records(raw, ["code", "close", "previous_close", "turnover_cny", "sector", "observed_at"])
    selected, excluded, seen = [], 0, set()
    for row in rows:
        observed = timestamp(row["observed_at"])
        if observed > cutoff:
            excluded += 1
            continue
        if not re.fullmatch(r"[0-9]{6}", row["code"]) or row["code"] in seen:
            raise ValueError("constituent codes must be unique six-digit codes")
        seen.add(row["code"])
        close, previous = number(row["close"], positive=True), number(row["previous_close"], positive=True)
        turnover = number(row["turnover_cny"])
        if turnover < 0 or not row["sector"].strip():
            raise ValueError("turnover cannot be negative; sector is required")
        selected.append({"code": row["code"], "return": close / previous - 1,
                         "turnover_cny": turnover, "sector": row["sector"].strip(), "time": observed})
    if not selected or len(selected) > expected_count:
        raise ValueError("no included members or more observations than the declared universe")
    market_tz = timezone(timedelta(hours=8))
    if len({row["time"].astimezone(market_tz).date() for row in selected}) != 1:
        raise ValueError("cash-equity breadth snapshot mixes local market dates")
    sectors = []
    for sector in sorted({row["sector"] for row in selected}):
        group = [row for row in selected if row["sector"] == sector]
        sectors.append({"sector": sector, "count": len(group),
                        "advancing": sum(row["return"] > 0 for row in group),
                        "equal_weight_return": sum(row["return"] for row in group) / len(group),
                        "turnover_cny": sum(row["turnover_cny"] for row in group)})
    times = [row["time"] for row in selected]
    total = sum(row["turnover_cny"] for row in selected)
    top = sorted(selected, key=lambda row: (-row["turnover_cny"], row["code"]))[:5]
    count = len(selected)
    return {"schema_version": 1, "data_kind": kind(data_kind), "as_of_utc": cutoff.isoformat(),
            "universe_label": universe_label, "expected_count": expected_count, "observed_count": count,
            "coverage": count / expected_count, "declared_sample_complete": count == expected_count,
            "advancing": sum(row["return"] > 0 for row in selected),
            "declining": sum(row["return"] < 0 for row in selected),
            "unchanged": sum(row["return"] == 0 for row in selected),
            "advance_fraction": sum(row["return"] > 0 for row in selected) / count,
            "sample_equal_weight_return": sum(row["return"] for row in selected) / count,
            "turnover_cny": total, "top5_turnover_share": sum(row["turnover_cny"] for row in top) / total if total else None,
            "observation_span_seconds": (max(times) - min(times)).total_seconds(),
            "oldest_observation_age_seconds": (cutoff - min(times)).total_seconds(),
            "sectors": sectors, "excluded_future_rows": excluded, "source_sha256": provenance(raw),
            "scope": "Imported constituent-sample breadth only; equal-weight return is not the official weighted index return.",
            "limitations": ["Declared universe count and current/historical membership not independently verified",
                            "Provider units, price adjustments, suspensions and zero-change reasons require checking",
                            "No futures basis, hedge order, margin or short-sale implementation"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--universe", required=True)
    parser.add_argument("--expected-count", type=int, required=True)
    parser.add_argument("--data-kind", required=True, choices=("synthetic", "imported_observations"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = analyze(args.csv.read_bytes(), args.as_of, args.universe, args.expected_count, args.data_kind)
        emit(result, args.out, [args.csv])
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(2, f"ERROR: {exc}\n")
    print(f"Saved {result['observed_count']}/{result['expected_count']} breadth observations / {result['data_kind']}.")


if __name__ == "__main__":
    main()
