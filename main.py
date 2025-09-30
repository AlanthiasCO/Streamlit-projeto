import streamlit as st
import pandas as pd

st.set_page_config(page_title="Finanças", page_icon="💰")

st.title("Finanças")
st.write("Bem-vindo à seção de Finanças! Aqui você pode gerenciar suas finanças pessoais, acompanhar despesas e receitas, e muito mais.")

st.markdown("""
# Finanças
Bem-vindo à seção de Finanças! Aqui você pode gerenciar suas finanças pessoais, acompanhar despesas e receitas, e muito mais.
""")

# Upload de arquivo - widget
file_upload = st.file_uploader(label="Faça upload dos dados", type=["csv", "xlsx"])

# Verifica se um arquivo foi carregado
if file_upload:

    # Lê o arquivo CSV ou Excel
    df = pd.read_csv(file_upload)
    
    # Converte a coluna "Data" para o formato datetime e extrai apenas a data
    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y").dt.date


    exp1 = st.expander("Ver dados brutos")

    # Exibe o DataFrame
    columns_fmt = {"Valor":st.column_config.NumberColumn("Valor", format="R$%d")}
    exp1.dataframe(df, hide_index=True, column_config=columns_fmt)


    exp2 = st.expander("Análise por Instituição")
    df_instituicao = df.pivot_table(index="Data", columns="Instituição", values="Valor")

    # Formatação das colunas - O Teo não fez essa parte do vídeo explicando então fiz por conta e deu certo
    columns_ds = {"Death Star":st.column_config.NumberColumn("Death Star", format="R$%d")}
    columns_ib = {"Iron Bank":st.column_config.NumberColumn("Iron Bank", format="R$%d")}
    columns_rb = {"Republic Bank":st.column_config.NumberColumn("Republic Bank", format="R$%d")}
    columns_tmw = {"TMW Bank":st.column_config.NumberColumn("TMW Bank", format="R$%d")}

    # unificando todos os dicionários de formatação de colunas em um só
    columns_all = columns_ds | columns_ib | columns_rb | columns_tmw

    tab_data, tab_history, tab_share = exp2.tabs(["Dados", "Histórico", "Distribuição"])

    tab_data.dataframe(df_instituicao, column_config=columns_all)

    with tab_history:
        st.line_chart(df_instituicao)

    with tab_share: 
        
        # Opção com date_input - Abre o calendário para selecionar a data

        # date = st.date_input("Data para distribuição",
        #               min_value=df_instituicao.index.min(),
        #               max_value=df_instituicao.index.max())

        # if date not in df_instituicao.index:
        #     st.warning("Data não encontrada nos dados. Entre com uma data válida.")
        # else:
        #     st.bar_chart(df_instituicao.loc[date])

        # Opção com selectbox - Abre uma lista suspensa para selecionar a data
        date = st.selectbox("Filtro data", options=df_instituicao.index)

        st.bar_chart(df_instituicao.loc[date])



            
