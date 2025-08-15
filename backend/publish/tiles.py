import brotli, json, math, pathlib, hashlib

TILE_SIZE = 1000

def _tile_path(out_dir: pathlib.Path, tid: int) -> pathlib.Path:
    return out_dir / "tiles" / f"tile_{tid:05d}.json.br"

def emit_tiles(out_dir, df, order_idx, snapshot_id):
    tiles_dir = pathlib.Path(out_dir) / "tiles"
    tiles_dir.mkdir(parents=True, exist_ok=True)
    n = len(df); tcount = math.ceil(n / TILE_SIZE)
    sha_lines = []
    for t in range(tcount):
        start = t * TILE_SIZE; end = min(start + TILE_SIZE, n)
        docs = []
        for oi in range(start, end):
            row = df.iloc[oi]
            docs.append({
                "order_index": int(oi),
                "doc_id": row["doc_id"],
                "title": (row.get("title") or "")[:300],
                "abstract_300": (row.get("abstract") or "").replace("\n"," ")[:300],
                "year": int(row.get("year",0) or 0),
                "venue": row.get("venue") or "",
                "tags": [],
                "badges": ["has_code"] if int(row.get("has_code",0) or 0)==1 else []
            })
        payload = {"snapshot_id":snapshot_id,"tile_id":t,"start_index":start,"docs":docs}
        raw = json.dumps(payload, ensure_ascii=False, separators=(",",":")).encode("utf-8")
        comp = brotli.compress(raw, quality=9)
        kb = len(comp)/1024
        # size band check (warn only for tiny datasets)
        if not (200 <= kb <= 400) and n >= 5000:
            raise RuntimeError(f"Tile {t} size {kb:.1f} KB out of 200–400 KB band")
        p = _tile_path(out_dir, t)
        p.write_bytes(comp)
        sha = hashlib.sha256(comp).hexdigest()
        sha_lines.append(f"{p.name} {sha}\n")
    (tiles_dir / "index.sha256").write_text("".join(sha_lines), encoding="utf-8")
    return tcount