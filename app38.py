import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# Definir a URL do modelo pickle
url = 'https://raw.githubusercontent.com/jeffersonsilva11/Cientista-de-Dados/main/modulo-38/model_final.pkl'

# Baixar o arquivo do modelo pickle
try:
    response = requests.get(url)
    if response.status_code == 200:
        model = pickle.loads(response.content)
        st.write("Modelo carregado com sucesso!")
    else:
        st.error(f"Falha ao baixar o modelo. Código de status: {response.status_code}")
        model = None
except Exception as e:
    st.error(f"Erro ao carregar o modelo: {e}")
    model = None
