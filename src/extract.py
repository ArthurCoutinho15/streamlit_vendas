import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

def extracao_api():
    url = 'https://labdados.com/produtos'
    response = requests.get(url, stream=True)
    dados = pd.DataFrame.from_dict(response.json())
    dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format = '%d/%m/%Y')
    return dados

def connect_mysql():
    USER = os.getenv('USER')
    PASSWORD = os.getenv('PASSWORD')
    HOST = os.getenv('HOST')
    DATABASE = os.getenv('DB_NAME_PROD')
    
    try:
        connection_url = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}'
        engine = create_engine(connection_url)
        print("Sucesso ao conectar")
    except Exception as err:
        print(f'Erro: {err}')
        
    return engine

def load_data(dados,engine):
   pass

dados = extracao_api()
connect_mysql()