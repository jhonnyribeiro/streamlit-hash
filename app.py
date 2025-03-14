import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import timedelta

#load data
@st.cache_data
def carregar_dados(empresas):
    texto_tickers = " ".join(empresas)
    dados_acao = yf.Tickers(texto_tickers)
    cotacoes_acao = dados_acao.history(period="1d", start='2010-01-01', end='2025-03-13')
    print(cotacoes_acao)
    cotacoes_acao = cotacoes_acao['Close']
    return cotacoes_acao

@st.cache_data
def carregar_tickers_acoes():
    base_tickers = pd.read_csv("IBOV.csv", sep=";")
    tickers = list(base_tickers["Código"])
    tickers = [item + ".SA" for item in tickers]
    return tickers

# acoes = ['ITSA4.SA', 'PETR4.SA', 'MGLU3.SA', 'VALE3.SA', 'ABEV3.SA', 'GGBR4.SA']
acoes = carregar_tickers_acoes()
dados = carregar_dados(acoes)

st.write("""
# App Preço de Ações
O gráfico abaixo representa o preço das ações do xxxx (Tiker) ao longo dos anos.
         """)

st.sidebar.header("Filtros")
#prepare vizualization
#filtro de ações
lista_acoes = st.sidebar.multiselect("Ações",dados.columns)
if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "Close"})
 
 #filtro de datas
data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()
intervalo_data = st.sidebar.slider("Selecione o período", min_value=data_inicial, max_value=data_final, value=(data_inicial, data_final), step=timedelta(days=1))

dados =  dados.loc[intervalo_data[0]:intervalo_data[1]]

st.line_chart(dados)