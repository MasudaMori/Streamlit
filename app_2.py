import timeit
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO  # Importar BytesIO para manipular dados em memória
import os

# Configuração da página deve ser a primeira chamada
st.set_page_config(
    page_title='Telemarketing analysis',
    page_icon="C:\\Users\\morid\\OneDrive\\Documentos\\Python Scripts\\Material_de_apoio_M19_Cientista de Dados\\img\\telmarketing_icon.png",
    layout="wide",
    initial_sidebar_state='expanded'
)

# Função para ler os dados
@st.cache_data(show_spinner=True)
def load_data(file_data):
    try:
        return pd.read_csv(file_data, sep=';')
    except FileNotFoundError:
        st.error(f"Erro: Arquivo não encontrado: {file_data}")
        return None
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return None

@st.cache_data
def multiselect_filter(relatorio, col, selecionados):
    if 'all' in selecionados:
        return relatorio
    else:
        return relatorio[relatorio[col].isin(selecionados)].reset_index(drop=True)

@st.cache_data
def df_toString(df):
    return df.to_csv(index=False)

@st.cache_data
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()  # Usar close() ao invés de save()
    processed_data = output.getvalue()
    return processed_data

def main():
    start = timeit.default_timer()

    bank_raw = load_data("C:\\Users\\morid\\OneDrive\\Documentos\\Python Scripts\\Material_de_apoio_M19_Cientista de Dados\\data\\input\\bank-additional-full.csv")

    if bank_raw is not None:
        csv = df_toString(bank_raw)
        st.write(type(csv))
        st.write(csv[:100])

        st.write('### Download CSV')
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='df_csv.csv',
            mime='text/csv',
        )

        df_xlsx = to_excel(bank_raw)
        st.write(type(df_xlsx))
        st.write(df_xlsx[:100])

        st.write('### Download Excel')
        st.download_button(label='📥 Download data as EXCEL',
                           data=df_xlsx,
                           file_name='df_excel.xlsx')

        st.write('Time: ', timeit.default_timer() - start)  

if __name__ == '__main__':
    main()

