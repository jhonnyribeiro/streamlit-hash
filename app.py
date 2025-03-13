import streamlit as st
import pandas as pd
import yfinance as yf

#load data
@st.cache_data
def carregar_dados(empresa):
    dados_acao = yf.Ticker(empresa)
    cotacoes_acao = dados_acao.history(period="1d", start='2010-01-01', end='2024-07-01')
    cotacoes_acao = cotacoes_acao[['Close']]
    return cotacoes_acao

#prepare vizualization
dados = carregar_dados("ITUB4.SA")
    

st.write("""
# App Preço de Ações
O gráfico abaixo representa o preço das ações do xxxx (Tiker) ao longo dos anos.
         """)

st.line_chart(dados)