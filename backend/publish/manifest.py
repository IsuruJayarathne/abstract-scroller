import json, pathlib, hashlib

def _sha(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1<<20), b""):
            h.update(chunk)
    return h.hexdigest()

def build(out_dir, snapshot_id, counts):
    out = pathlib.Path(out_dir)
    order_path = out / "order" / "ORDER.bin"
    tiles_index = out / "tiles" / "index.sha256"
    mani = {
        "snapshot_id": snapshot_id,
        "counts": {"docs": counts["docs"], "tiles": counts["tiles"], "tile_size": 1000},
        "order": {"path": "order/ORDER.bin", "dtype":"uint32", "endianness":"little", "sha256": _sha(order_path)},
        "tiles": {"pattern":"tiles/tile_{tile_id}.json.br", "sha256_index": f"tiles/{tiles_index.name}"},
        "bitsets": {"dir":"bitsets/", "index":"bitsets/index.json"},
        "nodes": {"tree":"nodes/tree.json.br", "dir":"nodes/summaries/", "schema_version":"1"}
    }
    (out / "manifest.json").write_text(json.dumps(mani, separators=(",",":")), encoding="utf-8")
    return mani

def main_validate():
    import sys, jsonschema, json
    snap = pathlib.Path(sys.argv[-1])
    mani = json.loads((snap / "manifest.json").read_text())
    schema = json.loads(pathlib.Path("contracts/schemas/manifest.schema.json").read_text())
    jsonschema.validate(mani, schema)
    print("manifest OK")

if __name__ == "__main__":
    main_validate()