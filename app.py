import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import timedelta

#load data
@st.cache_data
def carregar_dados(empresas):
    texto_tickers = " ".join(empresas)
    dados_acao = yf.Tickers(texto_tickers)
    cotacoes_acao = dados_acao.history(period="1d", start='2010-01-01', end='2025-03-10')
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
O gráfico abaixo representa o preço das ações ao longo dos anos.
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

texto_performance_ativos = ""

if len(lista_acoes) == 0:
    lista_acoes = list(dados.columns)
elif len(lista_acoes) == 1:
    dados = dados.rename(columns={"Close": acao_unica})

carteira = [1000 for acao in lista_acoes]
total_inicial_carteira = sum(carteira)

for i, acao in enumerate(lista_acoes):
    perfomance_ativo = dados[acao].iloc[-1] / dados[acao].iloc[0] - 1
    perfomance_ativo = float(perfomance_ativo)

    carteira[i] = carteira[i] * ( 1 + perfomance_ativo)

    if perfomance_ativo > 0:
        texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: :green[{perfomance_ativo:.1%}]"
    elif perfomance_ativo < 0:
        texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: :red[{perfomance_ativo:.1%}]"
    else:
        texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: {perfomance_ativo:.1%}"

total_final_carteira = sum(carteira)
performance_carteira = total_final_carteira / total_inicial_carteira - 1

texto_performance_carteira = ""

if performance_carteira > 0:
    texto_performance_carteira = f" Performance da carteira :green[{performance_carteira:.1%}]"
elif performance_carteira < 0:
    texto_performance_carteira = f" Performance da carteira :red[{performance_carteira:.1%}]"
else:
    texto_performance_carteira = f" Performance da carteira {performance_carteira:.1%}"


st.write(f"""
### Performance ativos
Essa foi a performance de cada ativo no periodo selecionado
         
{texto_performance_ativos}

#### Carteira
{texto_performance_carteira}
""")