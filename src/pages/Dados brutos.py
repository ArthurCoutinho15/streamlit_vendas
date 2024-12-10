import streamlit as st
import requests 
import pandas as pd

st.title('Dados Brutos')
url = 'https://labdados.com/produtos'

response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format= '%d/%m/%Y')

with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as colunas', list(dados.columns), list(dados.columns))

st.sidebar.title('Filtros')

with st.sidebar.expander('Nome do produto'):
    produtos = st.multiselect('Selecione os produtos', dados['Produto'].unique(), dados['Produto'].unique())
with st.sidebar.expander('Categoria do produto'):
    categoria_produtos = st.multiselect('Selecione as categorias', dados['Categoria do Produto'].unique(), dados['Categoria do Produto'].unique())
with st.sidebar.expander('Frete'):
        frete = st.slider('Selecione o frete', 0, 250, (0,250))
with st.sidebar.expander('Preço do produto'):
    preco = st.slider('Selecione o preço', 0, 5000, (0,5000))
with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input('Seleciona a data', (dados['Data da Compra'].min(), dados['Data da Compra'].max()))
with st.sidebar.expander('Vendedor'):
    st.multiselect('Selecione os vendedores', dados['Vendedor'].unique(), dados['Vendedor'].unique())
with st.sidebar.expander('Local da compra'):
    st.multiselect('Selecione o local da compra', dados['Local da compra'].unique(), dados['Local da compra'].unique())
with st.sidebar.expander('Avaliação da compra'):
    st.slider('Selecione a avaliação da compra', 1,5, value=(1,5))
with st.sidebar.expander('Tipo de pagamento'):
    tipo_pagamento = st.multiselect('Selecione o tipo de pagamento',dados['Tipo de pagamento'].unique(), dados['Tipo de pagamento'].unique())
with st.sidebar.expander('Quantidade de parcelas'):
    qtd_parcelas = st.slider('Selecione a quantidade de parcelas', 1, 24, (1,24))
    
st.dataframe(dados)
