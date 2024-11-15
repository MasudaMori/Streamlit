import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# URL do arquivo pickle "raw"
try:
    with open('model_final.pkl', 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    st.error(f"Erro ao carregar o modelo local: {e}")
    model = None


# Baixar o arquivo do modelo pickle
response = requests.get(url)
if response.status_code == 200:
    try:
        model = pickle.loads(response.content)
        st.write("Modelo carregado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao carregar o modelo: {e}")
        model = None
else:
    st.error(f"Falha ao baixar o arquivo. Status code: {response.status_code}")
    model = None


# Função para o pré-processamento dos dados
def preprocessamento(df, model):
    try:
        # Convertendo colunas categóricas e de data/hora para numéricas
        for col in df.columns:
            if df[col].dtype == 'object' or df[col].dtype.name == 'category':
                df[col] = df[col].astype('category').cat.codes
            elif df[col].dtype.name == 'datetime64[ns]':
                df[col] = df[col].values.astype(np.int64) // 10 ** 9

        # Adiciona colunas faltantes que o modelo espera, se necessário
        model_feature_names = model.feature_names_in_
        for feature in model_feature_names:
            if feature not in df.columns:
                # Adiciona a coluna faltante com valor padrão (ajuste conforme necessário)
                df[feature] = 0

        # Reordenar colunas para corresponder à ordem do modelo
        df = df.reindex(columns=model_feature_names)

        # Inicializando o imputador para preencher valores NaN com a média da coluna
        imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
        df_imputed = imputer.fit_transform(df)

        # Padronização dos dados
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df_imputed)
        return df_scaled
    except Exception as e:
        st.error(f"Ocorreu um erro durante o pré-processamento: {e}")
        return None

# Função para realizar a escoragem
def escoragem(df, model):
    if model is None:
        st.error("O modelo não está disponível para realizar a escoragem.")
        return None
    # Pré-processamento dos dados
    df_processed = preprocessamento(df, model)
    if df_processed is not None:
        # Realizar as previsões com o modelo carregado
        predictions = model.predict(df_processed)
        return predictions
    else:
        return None

# Interface Streamlit
def main():
    if model is None:
        st.error("O modelo não foi carregado. Por favor, verifique o arquivo ou o link fornecido.")
        return

    st.title("Aplicação para Escoragem de Dados")

    # Carregador de arquivos FTR
    uploaded_file = st.file_uploader("Escolha um arquivo FTR para escoragem", type="ftr")
    if uploaded_file is not None:
        # Carregar o FTR para um DataFrame
        df = pd.read_feather(uploaded_file)
        
        # Mostrar o DataFrame no Streamlit (opcional)
        if st.checkbox('Mostrar dados brutos'):
            st.write(df)
        
        # Botão para realizar a escoragem
        if st.button('Escorar'):
            result = escoragem(df, model)
            if result is not None:
                # Adicionar as previsões ao DataFrame
                df['Previsão'] = result
                
                # Mostrar os resultados
                st.write("Resultados da Escoragem:")

                # Define um número máximo de linhas para exibir, por exemplo, 1000
                max_rows_to_display = 1000
                if len(df) > max_rows_to_display:
                    st.warning(f"Mostrando apenas as primeiras {max_rows_to_display} linhas devido ao limite de tamanho de dados.")
                    st.write(df.head(max_rows_to_display))
                else:
                    st.write(df)
                
                # Download dos resultados como CSV
                st.download_button(
                    label='Baixar resultados como CSV',
                    data=df.to_csv(index=False).encode('utf-8'),
                    file_name='resultados_escoragem.csv',
                    mime='text/csv'
                )
            else:
                st.error("Não foi possível realizar a escoragem devido a um erro no pré-processamento.")

# Rodar a aplicação
if __name__ == "__main__":
    main()
