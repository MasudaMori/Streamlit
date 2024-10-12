import timeit
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
import os

# Configuração da página (deve ser a primeira função Streamlit a ser chamada)
st.set_page_config(
    page_title='Telemarketing Analysis', 
    page_icon="C:/Users/morid/OneDrive/Documentos/Python Scripts/img/Bank-Branding.jpg",
    layout='wide', 
    initial_sidebar_state='expanded'
)

# Configuração do tema Seaborn
custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)

# Função para carregar os dados
@st.cache_data(show_spinner=True)
def load_data(file_data):
    try:
        return pd.read_csv(file_data, sep=';')
    except Exception as e:
        st.error(f"Erro ao carregar arquivo: {e}")
        return pd.read_excel(file_data)

# Função para aplicar múltiplos filtros
@st.cache_data
def multiselect_filter(relatorio, col, selecionados):
    if 'all' in selecionados:
        return relatorio
    else:
        return relatorio[relatorio[col].isin(selecionados)].reset_index(drop=True)

# Função principal
def main():
    st.title('Telemarketing Analysis')
    st.markdown("---")

    # Verifica se o arquivo de imagem existe antes de carregá-lo
    image_path = "C:\\Users\\morid\\OneDrive\\Documentos\\Python Scripts\\Material_de_apoio_M19_Cientista de Dados\\img\\Bank-Branding.jpg"
    if os.path.exists(image_path):
        image = Image.open(image_path)
        st.sidebar.image(image)
    else:
        st.sidebar.warning("Imagem não encontrada.")

    # Upload de dados
    st.sidebar.write("## Suba o arquivo")
    data_file_1 = st.sidebar.file_uploader("Bank marketing data", type=['csv', 'xlsx'])

    if data_file_1 is not None:
        start = timeit.default_timer()
        bank_raw = load_data(data_file_1)
        st.write('Tempo de carregamento: ', timeit.default_timer() - start)

        bank = bank_raw.copy()
        st.write(bank_raw.head())

        # Filtros laterais
        with st.sidebar.form(key='my_form'):
            # IDADES
            max_age = int(bank.age.max())
            min_age = int(bank.age.min())
            idades = st.slider(label='Idade', min_value=min_age, max_value=max_age, value=(min_age, max_age), step=1)

            # Filtros múltiplos
            filters = {
                "Profissão": bank.job,
                "Estado civil": bank.marital,
                "Default": bank.default,
                "Tem financiamento imob?": bank.housing,
                "Tem empréstimo?": bank.loan,
                "Meio de contato": bank.contact,
                "Mês do contato": bank.month,
                "Dia da semana": bank.day_of_week
            }

            selected_filters = {}
            for label, col in filters.items():
                unique_vals = col.unique().tolist()
                unique_vals.append('all')
                selected = st.multiselect(label, unique_vals, ['all'])
                selected_filters[label] = selected

            # Aplicar os filtros selecionados
            bank = bank.query("age >= @idades[0] and age <= @idades[1]")
            for label, col in filters.items():
                bank = bank.pipe(multiselect_filter, col.name, selected_filters[label])

            submit_button = st.form_submit_button(label='Aplicar')

        # Gráficos
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))

        # Gráfico para os dados brutos
        bank_raw_target_perc = bank_raw.y.value_counts(normalize=True).to_frame() * 100
        bank_raw_target_perc = bank_raw_target_perc.rename(columns={'y': 'proportion'}).sort_index()
        sns.barplot(x=bank_raw_target_perc.index, y='proportion', data=bank_raw_target_perc, ax=ax[0])  # Usando 'proportion'
        ax[0].bar_label(ax[0].containers[0])
        ax[0].set_title('Dados brutos', fontweight="bold")

        # Gráfico para os dados filtrados
        try:
            bank_target_perc = bank.y.value_counts(normalize=True).to_frame() * 100
            bank_target_perc = bank_target_perc.rename(columns={'y': 'proportion'}).sort_index()
            sns.barplot(x=bank_target_perc.index, y='proportion', data=bank_target_perc, ax=ax[1])  # Usando 'proportion'
            ax[1].bar_label(ax[1].containers[0])
            ax[1].set_title('Dados filtrados', fontweight="bold")
        except Exception as e:
            st.error(f"Erro nos filtros: {e}")

        # Ajuste o layout
        plt.tight_layout()

        # Exibindo o gráfico no Streamlit
        st.pyplot(fig)

if __name__ == "__main__":
    main()
