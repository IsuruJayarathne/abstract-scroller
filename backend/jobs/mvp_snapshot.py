import argparse, pathlib, pandas as pd
from backend.publish import ids, order, tiles, manifest, writer

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(
    args.input,
    dtype=str,               # read everything as string; no implicit NaN
    keep_default_na=False,   # don’t convert "" to NaN
    )
    # normalize types we care about
    df["year"] = pd.to_numeric(df.get("year", 0), errors="coerce").fillna(0).astype(int)
    df["has_code"] = pd.to_numeric(df.get("has_code", 0), errors="coerce").fillna(0).astype(int)
    # parse date for robust ordering; missing dates go last
    df["date"] = pd.to_datetime(df.get("date"), errors="coerce")

    df["doc_id"] = df.apply(ids.make_stable_id, axis=1)
    df, ord_idx = order.make_order_by_recency(df)

    writer.write_order(out, ord_idx)
    # empty dirs for contracts
    (out / "bitsets").mkdir(exist_ok=True, parents=True)
    (out / "bitsets" / "index.json").write_text('{"families":{}}', encoding="utf-8")
    (out / "nodes").mkdir(exist_ok=True, parents=True)
    (out / "nodes" / "summaries").mkdir(exist_ok=True, parents=True)
    (out / "nodes" / "tree.json.br").write_bytes(b"")

    tile_count = tiles.emit_tiles(out, df, ord_idx, snapshot_id=out.name)
    mani = manifest.build(out, out.name, {"docs": len(df), "tiles": tile_count})
    print("snapshot ready:", out, "docs:", mani["counts"]["docs"], "tiles:", mani["counts"]["tiles"])

if __name__ == "__main__":
    main()