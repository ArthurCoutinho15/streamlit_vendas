import streamlit as st
import pandas as pd
import requests
import plotly.express as px

def formata_numero(valor, prefixo = ''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhões'

def extracao_api():
    url = 'https://labdados.com/produtos'
    response = requests.get(url, stream=True)
    dados = pd.DataFrame.from_dict(response.json())
    return dados

def tabelas(dados):
    receita_estados = dados.groupby('Local da compra')[['Preço']].sum()
    receita_estados = dados.drop_duplicates(subset='Local da compra')['Local da compra', 'lat', 'lon'].merge(receita_estados, left_on = 'Local da compra', right_index=True).sort_values('Preço', ascending=False)

    return receita_estados

def grafico_mapa(dados_tabela):
    fig_mapa_receita = px.scatter_geo(dados_tabela,
                                      lat = 'lat',
                                      lon='lon',
                                      scope = 'south america',
                                      size='Preço',
                                      template='seaborn',
                                      hover_name = 'Local da compra',
                                      hover_data = {'lat':False,
                                                    'lon': False},
                                      title= 'Receita por estado')
    
    return fig_mapa_receita
    
    
def dashboard(dados, fig_mapa_receita):
    st.title('Dashboard de vendas :shopping_trolley:')

    col_1, col_2 = st.columns(2)

    with col_1:
        st.metric('Receita', formata_numero(dados['Preço'].sum(), 'R$'))
        st.plotly_chart(fig_mapa_receita)
    with col_2:
        st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))

    st.dataframe(dados)


if __name__ == '__main__':
    dados = extracao_api()
    mapa_receita = grafico_mapa(dados)
    dashboard(dados, mapa_receita)
   
    
