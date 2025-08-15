import hashlib, re, unicodedata, math

def _norm_text(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").lower()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^\w\s:/.-]", "", s).strip()
    return s

def _clean(v) -> str:
    # Turn None/NaN into "", everything else into a trimmed string
    if v is None:
        return ""
    # avoid importing pandas here; handle floats explicitly
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return ""
    s = str(v).strip()
    # pandas may stringify NaN as "nan"
    return "" if s.lower() == "nan" else s

def _get(row, key):
    try:
        return row[key]
    except Exception:
        return row.get(key) if hasattr(row, "get") else None

def make_stable_id(row) -> str:
    for key, pref in (("doi", "doi:"), ("arxiv_id", "arxiv:"), ("repec_id", "repec:")):
        val = _clean(_get(row, key))
        if val:
            return f"{pref}{_norm_text(val)}"
    year  = _clean(_get(row, "year"))
    title = _clean(_get(row, "title"))
    key = f"{year}|{_norm_text(title)}"
    h = hashlib.sha1(key.encode("utf-8")).hexdigest()[:16]
    return f"hash:{h}"
