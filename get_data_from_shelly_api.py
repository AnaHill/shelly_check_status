import requests
import pandas as pd

BASE_URL = "https://api.spot-hinta.fi/SmartMonitoring"


def fetch_shelly_data(api_key: str) -> pd.DataFrame:
    url = f"{BASE_URL}?PrivateKey={api_key}&PrivateKeyData=true"
    response = requests.get(url)
    response.raise_for_status()

    records = []
    for item in response.json():
        records.append((
            item['ShellyName'],
            item['TimeStampUtc'],
            item['RelayNumber'],
            item['RelayName'],
            item['RelayIsActiveNow'],
            item['PriceWithTaxInCents'],
            item['RankNow'],
        ))

    df = pd.DataFrame(
        records,
        columns=['shellynimi', 'pvm', 'relenro', 'relenimi', 'relestatus', 'hinta_snt', 'hinta_rank'],
    )
    df['pvm'] = pd.to_datetime(df['pvm'])
    return df
