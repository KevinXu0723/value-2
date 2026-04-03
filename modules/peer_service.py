import re
import pandas as pd
import akshare as ak

SPECIAL_NAMES = {"行业平均", "行业中值"}

def normalize_symbol(symbol: str) -> str:
    s = str(symbol).strip().upper()
    if s.startswith(("SZ", "SH", "BJ")) and len(s) == 8:
        return s
    if len(s) == 6 and s.isdigit():
        if s.startswith(("6", "5", "9")):
            return "SH" + s
        elif s.startswith(("8", "4")):
            return "BJ" + s
        else:
            return "SZ" + s
    raise ValueError("symbol 格式错误，应为 000895 或 SZ000895")

def _to_float(x):
    if pd.isna(x):
        return pd.NA
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x).strip().replace(",", "").replace("%", "")
    if s in {"", "-", "--", "nan", "None"}:
        return pd.NA
    m = re.search(r"-?\d+(\.\d+)?", s)
    return float(m.group()) if m else pd.NA

def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        if col in ["代码", "简称", "排名"]:
            continue
        out[col] = out[col].apply(_to_float)
    return out

def split_rows(df: pd.DataFrame, symbol: str):
    code6 = symbol[-6:]
    code_str = df["代码"].astype(str).str[-6:]
    is_special = df["简称"].astype(str).isin(SPECIAL_NAMES) | df["代码"].astype(str).isin(SPECIAL_NAMES)
    is_target = code_str == code6

    target = df[is_target]
    special = df[is_special]
    peers = df[~is_special].copy()
    return target, special, peers

def fetch_peer_pack(symbol: str) -> dict:
    sym = normalize_symbol(symbol)

    growth = clean_df(ak.stock_zh_growth_comparison_em(symbol=sym))
    valuation = clean_df(ak.stock_zh_valuation_comparison_em(symbol=sym))
    dupont = clean_df(ak.stock_zh_dupont_comparison_em(symbol=sym))
    scale = clean_df(ak.stock_zh_scale_comparison_em(symbol=sym))

    return {
        "symbol": sym,
        "growth": growth,
        "valuation": valuation,
        "dupont": dupont,
        "scale": scale,
    }
