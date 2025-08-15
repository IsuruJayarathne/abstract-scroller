import numpy as np

def make_order_by_recency(df):
    # stable sort by date desc; mergesort preserves input order for equal dates
    df = df.sort_values("date", ascending=False, kind="mergesort").reset_index(drop=True)
    order_idx = np.arange(len(df), dtype=np.uint32)
    return df, order_idx