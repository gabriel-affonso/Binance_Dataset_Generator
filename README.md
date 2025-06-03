
# Coleta e Processamento de Dados Históricos de Criptomoedas (1 Minuto)

Este repositório contém um script Python (`gerdor.data.set.2.py`) que automatiza a coleta de dados históricos de velas (klines) em intervalo de 1 minuto para diversos pares de criptomoedas usando a API da Binance. Após baixar os dados, o script transforma o resultado em um DataFrame pandas, gera colunas úteis para análise e Machine Learning (retorno percentual, variação de preço, volatilidade e direção de preço), e salva cada conjunto de dados em um arquivo CSV separado.

---

## Índice

1. [Descrição Geral](#descri%C3%A7%C3%A3o-geral)  
2. [Pré-requisitos](#pr%C3%A9-requisitos)  
3. [Instalação](#instala%C3%A7%C3%A3o)  
4. [Configuração de API Keys](#configura%C3%A7%C3%A3o-de-api-keys)  
5. [Listagem de Pares e Períodos](#listagem-de-pares-e-per%C3%ADodos)  
6. [Explicação do Script passo a passo](#explica%C3%A7%C3%A3o-do-script-passo-a-passo)  
   1. [1) Importações e Configurações Iniciais](#1-importa%C3%A7%C3%B5es-e-configura%C3%A7%C3%B5es-iniciais)  
   2. [2) Inicializar Cliente Binance](#2-inicializar-cliente-binance)  
   3. [3) Função `fetch_data` (Coleta de Kl ines)](#3-fun%C3%A7%C3%A3o-fetch_data-coleta-de-klines)  
   4. [4) Loop Principal por Símbolo e Intervalos de Data](#4-loop-principal-por-s%C3%ADmbolo-e-intervalos-de-data)  
   5. [5) Transformação para DataFrame pandas](#5-transforma%C3%A7%C3%A3o-para-dataframe-pandas)  
   6. [6) Geração de Colunas de Feature para ML](#6-gera%C3%A7%C3%A3o-de-colunas-de-feature-para-ml)  
   7. [7) Remoção de Valores nulos](#7-remo%C3%A7%C3%A3o-de-valores-nulos)  
   8. [8) Salvamento em CSV e Pré-visualização](#8-salvamento-em-csv-e-pr%C3%A9-visualiza%C3%A7%C3%A3o)  
7. [Como Executar](#como-executar)  
8. [Saídas Geradas](#sa%C3%ADdas-geradas)  
9. [Estrutura dos CSVs](#estrutura-dos-csvs)  
10. [Possíveis Melhorias](#poss%C3%ADveis-melhorias)  
11. [Licença e Créditos](#licen%C3%A7a-e-cr%C3%A9ditos)

---

## Descrição Geral

O script `gerdor.data.set.2.py` tem como objetivo:

1. Conectar-se à API da Binance usando chaves de acesso (API_KEY e API_SECRET).
2. Para cada par de criptomoeda em uma lista predefinida (`PARES`), coletar dados de klines de 1 minuto desde uma data de início (`INICIO = "2019-01-01"`) até uma data de fim (`FIM = "2025-04-20"`).  
3. Dividir o intervalo total em blocos de 5 dias para não estourar limites de requisições da API.  
4. Agregar todos os klines obtidos em uma lista e converter para um DataFrame pandas.  
5. Selecionar apenas as colunas de interesse (tempo de abertura, preços de abertura/fechamento/alta/baixa e volume).  
6. Converter timestamps em formato legível (`datetime`) e colunas numéricas para `float`.  
7. Gerar colunas adicionais:
   - **return**: retorno percentual (`pct_change()`) de fechamento entre períodos consecutivos.  
   - **price_change**: diferença entre preço de fechamento e preço de abertura (`close - open`).  
   - **volatility**: diferença entre preço máximo e mínimo (`high - low`).  
   - **direction**: variável binária (1 se o próximo fechamento for maior que o atual, 0 caso contrário).  
8. Remover linhas com valores ausentes (`NaN`) gerados pelo cálculo de retorno ou pelo `shift`.  
9. Salvar o DataFrame final em um arquivo CSV específico para cada par (ex.: `btc_usdt_1min_dataset.01.01.19_20.04.25.csv`).  
10. Exibir uma prévia (`head()`) de cada DataFrame no console.

---

## Pré-requisitos

Para executar este script, você precisará:

- Python 3.7 ou superior  
- Uma conta Binance com chave de API (key e secret) válidas e permissão de leitura de dados de mercado.  
- Biblioteca `python-binance` instalada (para conectar à API).  
- Bibliotecas `pandas` e `datetime` (parte da biblioteca padrão) instaladas.

---

## Instalação

1. **Crie e ative um ambiente virtual (recomendado)**:
   ```bash
   python3 -m venv .venv
   # No Linux/Mac:
   source .venv/bin/activate
   # No Windows PowerShell:
   .venv\Scripts\Activate.ps1

2. **Instale as dependências necessárias**:

   ```bash
   pip install python-binance pandas
   ```
3. **Verifique se o script `gerdor.data.set.2.py` está no diretório de trabalho**.

---

## Configuração de API Keys

No início do script, preencha as variáveis `API_KEY` e `API_SECRET` com as suas credenciais da Binance:

```python
API_KEY = 'SUA_API_KEY_AQUI'
API_SECRET = 'SEU_API_SECRET_AQUI'
```

Sem essas credenciais, o script não conseguirá se autenticar e buscar dados históricos. Para criar chaves de API:

1. Acesse sua conta Binance.
2. No painel de usuário, vá em “API Management” (Gerenciamento de API).
3. Crie um novo par de chaves (label/descritivo de sua preferência).
4. Copie e cole nos campos acima.

---

## Listagem de Pares e Períodos

* **PARES**: lista de strings contendo os símbolos (pairs) a serem baixados da Binance.

  ```python
  PARES = [
      'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT',
      'XRPUSDT', 'LTCUSDT', 'DOTUSDT', 'MATICUSDT', 'AVAXUSDT',
      'USDCUSDT', 'BUSDUSDT', 'DAIUSDT',
      'DOGEUSDT', 'SHIBUSDT',
      'ETHBTC', 'BCHUSDT', 'UNIUSDT',
      'LINKUSDT', 'ATOMUSDT', 'AAVEUSDT', 'COMPUSDT', 'SANDUSDT',
      'MANAUSDT', 'NEARUSDT', 'FTMUSDT', 'ZILUSDT', 'FILUSDT'
  ]
  ```
* **INTERVALO**: intervalo de tempo para cada vela, definido como `Client.KLINE_INTERVAL_1MINUTE` (1 minuto).
* **INICIO** e **FIM**: strings no formato “YYYY-MM-DD” definindo o período total de coleta.

  ```python
  INICIO = "2019-01-01"
  FIM    = "2025-04-20"
  ```
* O script subdivide o período em blocos de 5 dias (`delta = timedelta(days=5)`) para coletar gradualmente e evitar limites de taxa da API.

---

## Explicação do Script passo a passo

### 1) Importações e Configurações Iniciais

```python
import pandas as pd
from binance.client import Client
from datetime import datetime, timedelta
import os

API_KEY = '...'
API_SECRET = '...'

PARES = [ 'BTCUSDT', 'ETHUSDT', … ]  # lista de símbolos
INTERVALO = Client.KLINE_INTERVAL_1MINUTE
INICIO = "2019-01-01"
FIM = "2025-04-20"
```

* Importa `pandas` para manipulação de DataFrames.
* Importa `Client` da `python-binance` para conexão à API Binance.
* Importa `datetime` e `timedelta` para manipular datas.
* Define constantes de configuração: `API_KEY`, `API_SECRET`, `PARES`, `INTERVALO`, `INICIO` e `FIM`.

### 2) Inicializar Cliente Binance

```python
client = Client(API_KEY, API_SECRET)
```

* Cria uma instância do cliente Binance autenticado com suas credenciais.
* A partir deste objeto `client`, será possível fazer requisições de dados de mercado.

### 3) Função `fetch_data` (Coleta de Kl ines)

```python
def fetch_data(symbol, start_str, end_str):
    print(f"🔄 Obtendo dados de {symbol} de {start_str} até {end_str}...")
    return client.get_historical_klines(symbol, INTERVALO, start_str, end_str)
```

* Recebe como entrada:

  * `symbol`: string do par (ex.: "BTCUSDT").
  * `start_str`: data de início no formato “YYYY-MM-DD”.
  * `end_str`: data de fim no formato “YYYY-MM-DD”.
* Imprime uma mensagem indicando qual par e intervalo está sendo baixado.
* Chama `get_historical_klines` do cliente Binance, que retorna uma lista de listas, cada uma contendo dados de uma vela no intervalo especificado.

### 4) Loop Principal por Símbolo e Intervalos de Data

```python
for symbol in PARES:
    start = datetime.strptime(INICIO, "%Y-%m-%d")
    end = datetime.strptime(FIM, "%Y-%m-%d")
    delta = timedelta(days=5)  # evita limites da API

    all_klines = []
    while start < end:
        interval_end = min(start + delta, end)
        klines = fetch_data(symbol, start.strftime("%Y-%m-%d"), interval_end.strftime("%Y-%m-%d"))
        all_klines.extend(klines)
        start = interval_end
```

* Para cada `symbol` na lista `PARES`, converte `INICIO` e `FIM` em objetos `datetime`.
* Define `delta = timedelta(days=5)` para baixar no máximo 5 dias por requisição.
* Inicializa `all_klines` como lista vazia.
* Enquanto `start < end`, define um `interval_end = min(start + delta, end)` para não ultrapassar a data final.
* Chama `fetch_data(symbol, start, interval_end)` e adiciona o resultado em `all_klines`.
* Avança `start` para o próximo bloco (`interval_end`), repetindo até completar o período total.

### 5) Transformação para DataFrame pandas

```python
df = pd.DataFrame(all_klines, columns=[
    "open_time", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "number_of_trades",
    "taker_buy_base_vol", "taker_buy_quote_vol", "ignore"
])
```

* Transforma a lista de listas `all_klines` em um DataFrame com as colunas originais retornadas pela Binance.
* As colunas iniciais (até `volume`) serão utilizadas; as demais podem ser descartadas posteriormente.

### 6) Ajustar Colunas de Interesse

```python
df = df[["open_time", "open", "high", "low", "close", "volume"]].copy()
df["open_time"] = pd.to_datetime(df["open_time"], unit='ms')
df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
```

* Seleciona somente as colunas `open_time`, `open`, `high`, `low`, `close` e `volume`.
* Converte `open_time` (timestamp em milissegundos) para `datetime`.
* Converte as colunas de preço e volume para tipo `float`, garantindo operações numéricas posteriores.

### 7) Geração de Colunas de Feature para ML

```python
df["return"] = df["close"].pct_change()
df["price_change"] = df["close"] - df["open"]
df["volatility"] = df["high"] - df["low"]
df["direction"] = (df["close"].shift(-1) > df["close"]).astype(int)
```

* **return**: cálculo de retorno percentual de fechamento em relação ao fechamento anterior.
* **price\_change**: diferença absoluta de preço entre fechamento e abertura.
* **volatility**: diferença entre preço máximo e mínimo (indicador de volatilidade intramenis).
* **direction**: variável binária (0 ou 1) indicando se o preço de fechamento do próximo período (shifted by –1) será maior (`1`) ou não (`0`) em relação ao fechamento atual. Útil para modelos de classificação de direção.

### 8) Remoção de Valores nulos

```python
df.dropna(inplace=True)
```

* Remove todas as linhas que contiverem `NaN`.
* Esse `NaN` pode aparecer, por exemplo, na primeira linha (onde não há `pct_change`) ou na última linha (onde `shift(-1)` não encontra próximo valor).

### 9) Salvamento em CSV e Pré-visualização

```python
nome_arquivo = f"{symbol.lower()}_1min_dataset.01.01.19_20.04.25.csv"
df.to_csv(nome_arquivo, index=False)
print(f"✅ Dados salvos em: {nome_arquivo}")
print(df.head())
```

* Define `nome_arquivo` formatado como `{symbol_lowercase}_1min_dataset.01.01.19_20.04.25.csv`.

  * Exemplo para `symbol = 'BTCUSDT'`: `btcusdt_1min_dataset.01.01.19_20.04.25.csv`.
* Salva o DataFrame em CSV sem índice.
* Imprime uma mensagem de confirmação no console e exibe as primeiras 5 linhas (`df.head()`) para checar rapidamente as colunas e valores.

---

## Como Executar

1. Garanta que você configurou corretamente as chaves `API_KEY` e `API_SECRET` no início do script.
2. Ajuste, se necessário, as variáveis `PARES`, `INICIO` e `FIM` de acordo com o período e os símbolos que deseja coletar.
3. No terminal (console), navegue até a pasta onde o script está salvo:

   ```bash
   cd /caminho/para/o/diretório
   ```
4. Execute o script com Python:

   ```bash
   python gerdor.data.set.2.py
   ```
5. Durante a execução, você verá mensagens de progresso:

   ```
   🔄 Obtendo dados de BTCUSDT de 2019-01-01 até 2019-01-06...
   🔄 Obtendo dados de BTCUSDT de 2019-01-06 até 2019-01-11...
   …
   ✅ Dados salvos em: btcusdt_1min_dataset.01.01.19_20.04.25.csv
   ```
6. Ao final, haverá um CSV para cada par listado em `PARES`, armazenado no diretório atual, contendo todas as colunas processadas.

---

## Saídas Geradas

Para cada símbolo em `PARES`, o script gera:

* Um arquivo CSV chamado:

  ```
  {symbol_em_minusculo}_1min_dataset.01.01.19_20.04.25.csv
  ```

  Exemplo:

  ```
  btcusdt_1min_dataset.01.01.19_20.04.25.csv
  ethusdt_1min_dataset.01.01.19_20.04.25.csv
  …
  filusdt_1min_dataset.01.01.19_20.04.25.csv
  ```

Cada CSV terá a seguinte estrutura de colunas:

| open\_time          | open    | high    | low     | close   | volume   | return     | price\_change | volatility | direction |
| ------------------- | ------- | ------- | ------- | ------- | -------- | ---------- | ------------- | ---------- | --------- |
| 2019-01-01 00:00:00 | 3800.00 | 3810.00 | 3795.00 | 3805.00 | 125.3456 | 0.00131579 | 5.00          | 15.00      | 0 or 1    |
| 2019-01-01 00:01:00 | 3805.00 | 3812.00 | 3800.00 | 3808.00 | 98.7654  | 0.00078802 | 3.00          | 12.00      | 0 or 1    |
| …                   | …       | …       | …       | …       | …        | …          | …             | …          | …         |

* **open\_time**: timestamp de abertura da vela (convertido para datetime).
* **open**, **high**, **low**, **close**, **volume**: valores de preço (float) e volume (float) para aquele minuto.
* **return**: retorno percentual do fechamento em relação ao fechamento anterior (`(close_t / close_{t-1}) - 1`).
* **price\_change**: diferença absoluta (`close - open`).
* **volatility**: amplitude da vela (`high - low`).
* **direction**: rótulo binário (1 se `close_{t+1} > close_t`, caso contrário 0).

---

## Estrutura dos CSVs

1. Cada arquivo CSV fica na mesma pasta onde o script foi executado.
2. O nome segue o padrão `{symbol_lower}_1min_dataset.01.01.19_20.04.25.csv`.
3. Valores de `open_time` já estão em formato legível (yyyy-mm-dd hh\:mm\:ss).
4. Não há colunas desnecessárias (as colunas originais `close_time`, `quote_asset_volume`, etc. foram descartadas).
5. As colunas finais (return, price\_change, volatility, direction) facilitam a criação de modelos de Machine Learning ou análise exploratória.

---

## Possíveis Melhorias

* **Paralelização**: baixar múltiplos símbolos em paralelo (threads ou processos) para acelerar a coleta total.
* **Tratamento de Erros**: implementar `try/except` nas requisições à API para capturar timeouts ou limites de taxa e aplicar “backoff” automático.
* **Batch Size Dinâmico**: ajustar o tamanho do bloco (`delta = timedelta(days=5)`) dinamicamente caso a API retorne muito ou pouco dado.
* **Persistência de Logs**: salvar logs detalhados em arquivo, registrando o horário de início e fim de cada download, quantidade de linhas obtidas, eventuais falhas etc.
* **Opções de Parâmetros via CLI**: usar `argparse` para permitir passar `--start`, `--end`, `--symbols` diretamente pela linha de comando.
* **Armazenamento em Banco de Dados**: em vez de CSV, gravar direto em um banco SQL (PostgreSQL, SQLite) ou NoSQL (MongoDB), com índices para consultas rápidas.
* **Cálculo de Indicadores Avançados**: adicionar ao DataFrame colunas como médias móveis, RSI, MACD, bandeiras de candle patterns, etc., já durante a fase de coleta.

---

## Licença e Créditos

Este script foi desenvolvido como parte de meu portfólio pessoal de projetos de análise e Machine Learning em criptomoedas.
Sinta‐se à vontade para usar, adaptar ou redistribuir este código, desde que mantenha a referência ao autor original.

---

> **Autor**: Gabriel Affonso
> **Contato**: [gabriel.affonso1@gmail.com](mailto:gabriel.affonso1@gmail.com)

```
```
