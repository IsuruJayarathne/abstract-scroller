import pathlib, shutil, os

def write_order(out_dir, order_idx):
    p = pathlib.Path(out_dir) / "order"
    p.mkdir(parents=True, exist_ok=True)
    (p / "ORDER.bin").write_bytes(order_idx.tobytes(order="C"))

def promote(staging_dir, snapshot_id):
    staging = pathlib.Path(staging_dir)
    root = staging.parent
    target = root / snapshot_id
    tmp = root / (snapshot_id + ".tmp")
    if tmp.exists():
        shutil.rmtree(tmp)
    shutil.copytree(staging, tmp)
    if target.exists():
        shutil.rmtree(target)
    os.replace(tmp, target)
    latest = root / "latest"
    if latest.exists() or latest.is_symlink():
        try: os.unlink(latest)
        except FileNotFoundError: pass
    os.symlink(snapshot_id, latest, target_is_directory=True)