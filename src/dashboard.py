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
    dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format = '%d/%m/%Y')
    return dados

def tabelas(dados):
    receita_estados = dados.groupby('Local da compra')[['Preço']].sum()
    receita_estados = dados.drop_duplicates(subset= 'Local da compra')[['Local da compra', 'lat', 'lon']].merge(receita_estados, left_on = 'Local da compra', right_index = True).sort_values('Preço', ascending= False)

    fig_receita_estados = px.bar(receita_estados.head(),
                                 x = 'Local da compra',
                                 y = 'Preço',
                                 text_auto= True,
                                 title= 'Top Estados (receita)')
    fig_receita_estados.update_layout(yaxis_title = 'Receita')
    return fig_receita_estados

def kpi_receita_mensal(dados):
    receita_mensal = dados.set_index('Data da Compra').groupby(pd.Grouper(freq='ME'))['Preço'].sum().reset_index()
    receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year
    receita_mensal['Mes'] = receita_mensal['Data da Compra'].dt.month_name()
    
    fig_receita_mensal = px.line(receita_mensal,
                                 x = 'Mes',
                                 y = 'Preço',
                                 markers= True,
                                 range_y= (0,receita_mensal.max()),
                                 color='Ano',
                                 line_dash= 'Ano',
                                 title = 'Receita mensal')
    
    
    
    return fig_receita_mensal

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

def receita_categoria(dados):
    receita_por_categoria = dados.groupby('Categoria do Produto')[['Preço']].sum().sort_values('Preço', ascending=False)
    
    fig_receita_categorias = px.bar(receita_por_categoria,
                                    text_auto= True,
                                    title='Receita por categoria')
    
    fig_receita_categorias.update_layout(yaxis_title='Receita')
    
    return fig_receita_categorias
    
def tabela_vendedores(dados):
    vendedores = pd.DataFrame(dados.groupby('Vendedor')['Preço'].agg(['sum','count']))
    return vendedores   

def tabela_vendas_estados(dados):
    vendas_estados = pd.DataFrame(dados.groupby('Local da compra')['Preço'].count())
    vendas_estados = dados.drop_duplicates(subset = 'Local da compra')[['Local da compra','lat', 'lon']].merge(vendas_estados, left_on = 'Local da compra', right_index = True).sort_values('Preço', ascending = False)
    
    return vendas_estados
    
def tabela_vendas_mensal(dados):
    vendas_mensal = pd.DataFrame(dados.set_index('Data da Compra').groupby(pd.Grouper(freq= 'M'))['Preço'].count()).reset_index()
    vendas_mensal['Ano'] = vendas_mensal['Data da Compra'].dt.year
    vendas_mensal['Mes'] = vendas_mensal['Data da Compra'].dt.month_name()
    
    return vendas_mensal

def tabela_vendas_categoria(dados):
    vendas_categoria = pd.DataFrame(dados.groupby('Categoria do Produto')['Preço'].count().sort_values(ascending=False))
    
    return vendas_categoria
       
def dashboard( dados, fig_mapa_receita, fig_receita_mensal, fig_receita_estados, fig_receita_categorias, vendedores, vendas_estado, vendas_mensal, vendas_categoria):
    
    
    st.title('Dashboard de vendas :shopping_trolley:')

    aba_1, aba_2, aba_3 = st.tabs(['Receita', 'Quantidade de vendas', 'Vendedores'])

    with aba_1:
        st.subheader("Análise de Receita")
        col_1, col_2 = st.columns(2)
        with col_1:
            st.metric('Receita', formata_numero(dados['Preço'].sum(), 'R$'))
            st.plotly_chart(fig_mapa_receita, use_container_width=True)
            st.plotly_chart(fig_receita_estados, use_container_width=True)
        with col_2:
            st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))
            st.plotly_chart(fig_receita_mensal, use_container_width=True)
            st.plotly_chart(fig_receita_categorias, use_container_width=True)

    with aba_2:
        st.subheader("Quantidade de Vendas")
        col_1, col_2 = st.columns(2)
        with col_1:
            st.metric('Receita', formata_numero(dados['Preço'].sum(), 'R$'))
            fig_mapa_vendas = px.scatter_geo(vendas_estado,
                                            lat = 'lat',
                                            lon = 'lon',
                                            scope = 'south america',
                                            #fitbounds = 'locations',
                                            template = 'seaborn',
                                            size = 'Preço',
                                            hover_name = 'Local da compra',
                                            hover_data= {'lat':False,'lon':False},
                                            title='Vendas por estado')
            fig_vendas_estados = px.bar(vendas_estado.head(),
                                        x = 'Local da compra',
                                        y = 'Preço',
                                        text_auto = True,
                                        title = 'Top 5 estados',
                                        )
            fig_vendas_estados.update_layout(yaxis_title='Quantidade de vendas')
            
            st.plotly_chart(fig_mapa_vendas, use_container_width=True)
            st.plotly_chart(fig_vendas_estados, use_container_width=True)
            
            
        with col_2:
            st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))
            fig_vendas_mensal = px.line  (vendas_mensal,
                                           x = 'Mes',
                                           y = 'Preço',
                                           markers = True,
                                           range_y = (0, vendas_mensal.max()),
                                           color = 'Ano',
                                           line_dash = 'Ano',
                                           title = 'Quantidade de vendas mensal')
            fig_vendas_mensal.update_layout(yaxis_title = 'Quantidade de vendas')
            fig_vendas_categoria = px.bar(vendas_categoria,
                                          text_auto = True,
                                          title = 'Vendas por categoria')
            fig_vendas_categoria.update_layout(showlegend=False,yaxis_title='Quantidade de vendas')
            st.plotly_chart(fig_vendas_mensal, use_container_width = True)
            st.plotly_chart(fig_vendas_categoria, use_container_width = True)

    with aba_3:
        qtd_vendedores = st.number_input('Quantidade de vendedores', 2, 10, 5)
        st.subheader("Informações dos Vendedores")
        col_1, col_2 = st.columns(2)
        with col_1:
            st.metric('Receita Total', formata_numero(dados['Preço'].sum(), 'R$'))
            fig_receita_vendedores = px.bar(vendedores[['sum']].sort_values('sum', ascending= False).head(qtd_vendedores),
                                            x = 'sum',
                                            y = vendedores[['sum']].sort_values('sum', ascending= False).head(qtd_vendedores).index,
                                            text_auto= True,
                                            title= f'Top {qtd_vendedores} vendedores (Receita)')
            st.plotly_chart(fig_receita_vendedores)  
        with col_2:
            st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))
            fig_vendas_vendedores = px.bar(vendedores[['count']].sort_values('count', ascending= False).head(qtd_vendedores),
                                            x = 'count',
                                            y = vendedores[['count']].sort_values('count', ascending= False).head(qtd_vendedores).index,
                                            text_auto= True,
                                            title= f'Top {qtd_vendedores} vendedores (Quantidade de vendas)')
            st.plotly_chart(fig_vendas_vendedores)  


if __name__ == '__main__':
    st.set_page_config(layout='wide')
    dados = extracao_api()
    receita_estados = tabelas(dados)
    receita_categorias = receita_categoria(dados)
    mapa_receita = grafico_mapa(dados)
    receita_mensal = kpi_receita_mensal(dados)
    vendedores = tabela_vendedores(dados)
    vendas_estado = tabela_vendas_estados(dados)
    vendas_mensal = tabela_vendas_mensal(dados)
    vendas_categoria = tabela_vendas_categoria(dados)
    dashboard(dados, mapa_receita, receita_mensal, receita_estados, receita_categorias,vendedores, vendas_estado, vendas_mensal, vendas_categoria)
   
    
