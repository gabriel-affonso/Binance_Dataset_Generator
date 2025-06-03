import pandas as pd
from binance.client import Client
from datetime import datetime, timedelta
import os

# ========== CONFIGURAÇÕES ==========
API_KEY = 'v2K6tSlwcynU3AteaNXmjARw3mckhNzmLgoqJD2zycS9lNMtYIbCEJBcnlSjCEm0'
API_SECRET = 'SFHPzYCev4wVE4fp9YqzRWAz5xXhGxpa5SISDJxWVlDElQrMCTfldwB7Bm6epieiI'

PARES = [
    'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT',
    'XRPUSDT', 'LTCUSDT', 'DOTUSDT', 'MATICUSDT', 'AVAXUSDT',
    'USDCUSDT', 'BUSDUSDT', 'DAIUSDT',
    'DOGEUSDT', 'SHIBUSDT',
    'ETHBTC', 'BCHUSDT', 'UNIUSDT',
    # 10 adicionais:
    'LINKUSDT', 'ATOMUSDT', 'AAVEUSDT', 'COMPUSDT', 'SANDUSDT',
    'MANAUSDT', 'NEARUSDT', 'FTMUSDT', 'ZILUSDT', 'FILUSDT'
]
INTERVALO = Client.KLINE_INTERVAL_1MINUTE
INICIO = "2019-01-01"
FIM = "2025-04-20"

# ========== INICIALIZAR CLIENT ==========
client = Client(API_KEY, API_SECRET)

# ========== OBTER DADOS ==========
def fetch_data(symbol, start_str, end_str):
    print(f"🔄 Obtendo dados de {symbol} de {start_str} até {end_str}...")
    return client.get_historical_klines(symbol, INTERVALO, start_str, end_str)

# ========== COLETA POR PAR E INTERVALOS ==========
for symbol in PARES:
    start = datetime.strptime(INICIO, "%Y-%m-%d")
    end = datetime.strptime(FIM, "%Y-%m-%d")
    delta = timedelta(days=5)  # evita limite da API

    all_klines = []
    while start < end:
        interval_end = min(start + delta, end)
        klines = fetch_data(symbol, start.strftime("%Y-%m-%d"), interval_end.strftime("%Y-%m-%d"))
        all_klines.extend(klines)
        start = interval_end

    # ========== TRANSFORMAR EM DATAFRAME ==========
    df = pd.DataFrame(all_klines, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_vol", "taker_buy_quote_vol", "ignore"
    ])

    # ========== AJUSTAR COLUNAS ==========
    df = df[["open_time", "open", "high", "low", "close", "volume"]].copy()
    df["open_time"] = pd.to_datetime(df["open_time"], unit='ms')
    df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)

    # ========== GERAR COLUNAS ÚTEIS PARA ML ==========
    df["return"] = df["close"].pct_change()
    df["price_change"] = df["close"] - df["open"]
    df["volatility"] = df["high"] - df["low"]
    df["direction"] = (df["close"].shift(-1) > df["close"]).astype(int)

    # ========== REMOVER NaN ==========
    df.dropna(inplace=True)

    # ========== SALVAR CSV ==========
    nome_arquivo = f"{symbol.lower()}_1min_dataset.01.01.19_20.04.25.csv"
    df.to_csv(nome_arquivo, index=False)
    print(f"✅ Dados salvos em: {nome_arquivo}")

    # ========== PRÉVIA ==========
    print(df.head())