import streamlit as st
import pandas as pd

def calc_general_metrics(df):
    df_data = df.groupby(by="Data")[["Valor"]].sum()
    df_data["lag_1"] = df_data["Valor"].shift(1)

    df_data["Diferenca Mensal Abs."] = df_data["Valor"] - df_data["lag_1"]
    df_data["Média 6M Diferenca Mensal Abs."] = df_data["Diferenca Mensal Abs."].rolling(window=6).mean()
    df_data["Média 12M Diferenca Mensal Abs."] = df_data["Diferenca Mensal Abs."].rolling(window=12).mean()
    df_data["Média 24M Diferenca Mensal Abs."] = df_data["Diferenca Mensal Abs."].rolling(window=24).mean()
    df_data["Diferenca Mensal Rel."] = df_data["Valor"] / df_data["lag_1"]
    df_data["Evolução 6M total"] = df_data["Valor"].rolling(window=6).apply(lambda x: x[-1] - x[0])
    df_data["Evolução 12M total"] = df_data["Valor"].rolling(window=12).apply(lambda x: x[-1] - x[0])
    df_data["Evolução 24M total"] = df_data["Valor"].rolling(window=24).apply(lambda x: x[-1] - x[0])
    df_data["Evolução Relativa 6M total"] = df_data["Valor"].rolling(window=6).apply(lambda x: x[-1] / x[0] - 1)
    df_data["Evolução Relativa 12M total"] = df_data["Valor"].rolling(window=12).apply(lambda x: x[-1] / x[0] - 1)
    df_data["Evolução Relativa 24M total"] = df_data["Valor"].rolling(window=24).apply(lambda x: x[-1] / x[0] - 1)

    df_data = df_data.drop("lag_1", axis=1)
    return df_data



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




    df_stats = calc_general_metrics(df)

    exp3 = st.expander("Estatísticas Gerais")

    # Formatação das colunas por dicionário
    columns_config = {  
        "Valor" : st.column_config.NumberColumn("Valor", format="R$%.2f"),
        "Diferenca Mensal Abs." : st.column_config.NumberColumn("Diferenca Mensal Abs.", format="R$%.2f"),
        "Média 6M Diferenca Mensal Abs." : st.column_config.NumberColumn("Média 6M Diferenca Mensal Abs.", format="R$%.2f"),
        "Média 12M Diferenca Mensal Abs." : st.column_config.NumberColumn("Média 12M Diferenca Mensal Abs.", format="R$%.2f"),
        "Média 24M Diferenca Mensal Abs." : st.column_config.NumberColumn("Média 24M Diferenca Mensal Abs.", format="R$%.2f"),
        "Evolução 6M total" : st.column_config.NumberColumn("Evolução 6M total", format="R$%.2f"),
        "Evolução 12M total" : st.column_config.NumberColumn("Evolução 12M total", format="R$%.2f"),
        "Evolução 24M total" : st.column_config.NumberColumn("Evolução 24M total", format="R$%.2f"),
        "Diferenca Mensal Rel." : st.column_config.NumberColumn("Diferenca Mensal Rel.", format="percent"),
        "Evolução Relativa 6M total" : st.column_config.NumberColumn("Evolução Relativa 6M total", format="percent"),
        "Evolução Relativa 12M total" : st.column_config.NumberColumn("Evolução Relativa 12M total", format="percent"),
        "Evolução Relativa 24M total" : st.column_config.NumberColumn("Evolução Relativa 24M total", format="percent")
    }

    exp3.dataframe(df_stats, column_config=columns_config)

    tab_stats, tab_abs, tab_rel = exp3.tabs(tabs=["Dados", "Historico de Evolucao", "Crescimento Relativo"])

    with tab_stats:
        st.dataframe(df_stats, column_config=columns_config)

    with tab_abs:
        abs_cols = [
            "Diferenca Mensal Abs.",
            "Média 6M Diferenca Mensal Abs.",
            "Média 12M Diferenca Mensal Abs.",
            "Média 24M Diferenca Mensal Abs."
        ]
        st.line_chart(df_stats[abs_cols])

    with tab_rel:
        rel_cols = [
            "Diferenca Mensal Rel.",
            "Evolução Relativa 6M total",
            "Evolução Relativa 12M total",
            "Evolução Relativa 24M total"
        ]
        st.line_chart(df_stats[rel_cols])


    


    
