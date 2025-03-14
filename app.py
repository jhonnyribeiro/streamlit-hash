import streamlit as st
import pandas as pd
import yfinance as yf

#load data
@st.cache_data
def carregar_dados(empresas):
    texto_tickers = " ".join(empresas)
    dados_acao = yf.Tickers(texto_tickers)
    cotacoes_acao = dados_acao.history(period="1d", start='2010-01-01', end='2024-07-01')
    print(cotacoes_acao)
    cotacoes_acao = cotacoes_acao['Close']
    return cotacoes_acao

acoes = ['ITSA4.SA', 'PETR4.SA', 'MGLU3.SA', 'VALE3.SA', 'ABEV3.SA', 'GGBR4.SA']
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


st.line_chart(dados)