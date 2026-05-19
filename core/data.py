# core/data.py
import requests
import pandas as pd
import numpy as np

def get_commodity_prices(indicator: str, fallback_base: float) -> pd.DataFrame:
    """Fetch from World Bank API with synthetic fallback."""
    url = (f"https://api.worldbank.org/v2/en/indicator/{indicator}"
           f"?format=json&per_page=120&mrv=120")
    try:
        r = requests.get(url, timeout=8)
        data = r.json()[1]
        records = [
            {'date': pd.to_datetime(d['date']), 'price': float(d['value'])}
            for d in data if d['value']
        ]
        df = pd.DataFrame(records).sort_values('date').reset_index(drop=True)
        if len(df) > 10:
            return df
        raise ValueError("Insufficient data")
    except Exception:
        return _synthetic(fallback_base)


def _synthetic(base: float) -> pd.DataFrame:
    np.random.seed(42)
    dates  = pd.date_range('2015-01-01', '2025-12-01', freq='ME')
    prices = base + np.cumsum(np.random.randn(len(dates)) * 7)
    prices = np.clip(prices, base * 0.4, base * 2.5)
    return pd.DataFrame({'date': dates, 'price': prices.round(2)})


def get_coal_prices() -> pd.DataFrame:
    return get_commodity_prices("PCOALSA_USD", fallback_base=180)

def get_ore_prices() -> pd.DataFrame:
    return get_commodity_prices("PIORECR_USD", fallback_base=120)