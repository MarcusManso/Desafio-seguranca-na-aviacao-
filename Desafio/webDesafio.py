import folium.map
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from pathlib import Path
import numpy as np
import seaborn as sns
import pydeck as pdk
import matplotlib.pyplot as plt
import geopandas as gpd
from streamlit_folium import folium_static
import folium

# CONFIGURANDO PG
st.set_page_config(layout="wide")
st.title('Asas de Ícaro')

# CARREGANDO ARQ
pasta_datasets = Path(__file__).parent.parent / 'DESAFIO'
caminho_acidentes = pasta_datasets / 'acidentesTransito_cenipa_2010a2021.xlsx'
df_acidentes = pd.read_excel(caminho_acidentes)

# LIMPANDO DATA
df_acidentes_cleaned = df_acidentes.dropna()

colunas = list(df_acidentes_cleaned.columns)
colunas_selecionadas = st.sidebar.multiselect('Selecione as colunas:', colunas, colunas)
col1, col2 = st.sidebar.columns(2)
col_filtro = col1.selectbox('Selecione a coluna', [c for c in colunas if c != 'id_colunas'])
valor_filtro = col2.selectbox('Selecione o valor', list(df_acidentes_cleaned[col_filtro].unique()))
status_filtrar = col1.button('Filtrar')
status_limpar = col2.button('Limpar')

# FiltrO
if status_filtrar:
    df_filtrado = df_acidentes_cleaned.loc[df_acidentes_cleaned[col_filtro] == valor_filtro, colunas_selecionadas]
elif status_limpar:
    df_filtrado = df_acidentes_cleaned[colunas_selecionadas]
else:
    df_filtrado = df_acidentes_cleaned[colunas_selecionadas]

st.dataframe(df_filtrado, height=800)

# Criando o mapa
def main():
    st.title("Mapa de Ocorrências")

    # Ler os dados
    latlon = pd.read_excel('lat lon.xlsx')

    # Extrair coordenadas
    latitude = latlon['ocorrencia_latitude']
    longitude = latlon['ocorrencia_longitude']

    # Criar o mapa com Folium 
    mapa = folium.Map(location=[latitude.mean(), longitude.mean()], zoom_start=10)

    for lat, lon in zip(latitude, longitude):
        # Adicionar marcador personalizado
        folium.Marker(
            location=[lat, lon],
            icon=folium.Icon(color='red', icon='info-sign')  # Personalize o marcador aqui
        ).add_to(mapa)
    
    # Exibir o mapa no Streamlit
    folium_static(mapa)

if __name__ == "__main__":
    main()

# Carregar os dados do arquivo Excel
file_path = 'morte x estado.xlsx'
data = pd.read_excel(file_path)

# Título da aplicação
st.title('Histograma de Fatalidades por Estado')

# Filtrar as colunas necessárias
selected_columns = ['aeronave_fatalidades_total', 'ocorrencia_uf']
filtered_data = data[selected_columns]

# Agrupar os dados por estado e somar as fatalidades
fatalities_by_state = filtered_data.groupby('ocorrencia_uf')['aeronave_fatalidades_total'].sum().reset_index()

# Ordenar os dados por número de fatalidades (opcional)
fatalities_by_state = fatalities_by_state.sort_values(by='aeronave_fatalidades_total', ascending=False)

# Configurações visuais usando Seaborn
plt.figure(figsize=(10, 6))  # Ajustar tamanho da figura
sns.barplot(data=fatalities_by_state, x='ocorrencia_uf', y='aeronave_fatalidades_total', palette='viridis')  # Usar paleta de cores "viridis"
plt.xlabel('Estado', fontsize=12)  # Ajustar tamanho da fonte do rótulo do eixo x
plt.ylabel('Fatalidades', fontsize=12)  # Ajustar tamanho da fonte do rótulo do eixo y
plt.title('Fatalidades por Estado', fontsize=14)  # Ajustar tamanho da fonte do título
plt.xticks(rotation=45, ha='right')  # Rotacionar os rótulos do eixo x para facilitar a leitura
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Adicionar linhas de grade no eixo y
plt.tight_layout()  # Ajustar layout para evitar que os rótulos fiquem cortados

# Exibir o gráfico na aplicação Streamlit
fig, ax = plt.subplots()  # Criar nova figura
ax = sns.barplot(data=fatalities_by_state, x='ocorrencia_uf', y='aeronave_fatalidades_total', palette='viridis')  # Plotar gráfico
plt.xlabel('Estado', fontsize=12)  # Ajustar tamanho da fonte do rótulo do eixo x
plt.ylabel('Fatalidades', fontsize=12)  # Ajustar tamanho da fonte do rótulo do eixo y
plt.title('Fatalidades por Estado', fontsize=14)  # Ajustar tamanho da fonte do título
plt.xticks(rotation=45, ha='right')  # Rotacionar os rótulos do eixo x para facilitar a leitura
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Adicionar linhas de grade no eixo y
plt.tight_layout()  # Ajustar layout para evitar que os rótulos fiquem cortados
st.pyplot(fig)  # Exibir o gráfico na aplicação Streamlit

# Definir estilo do seaborn
sns.set_style("whitegrid")

# Título da aplicação
st.title('Análise de Ocorrências de Acidentes Aéreos')

# Carregar os dados do arquivo Excel
file_path = 'acidentesTransito_cenipa_2010a2021.xlsx'
data = pd.read_excel(file_path)

# Distribuição dos tipos de ocorrência (Gráfico de Pizza)
st.subheader('Distribuição dos Tipos de Ocorrência')
occurrence_types_count = data['ocorrencia_classificacao'].value_counts()
fig_pie, ax_pie = plt.subplots()
ax_pie.pie(occurrence_types_count, labels=occurrence_types_count.index, autopct='%1.1f%%', startangle=140)
ax_pie.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig_pie)

# Top 5 cidades com maior número de ocorrências (Gráfico de Barras)
st.subheader('Top 5 Cidades com Maior Número de Ocorrências')
top_cities = data['ocorrencia_cidade'].value_counts().nlargest(5)
fig_bar, ax_bar = plt.subplots()
top_cities.plot(kind='bar', ax=ax_bar, color='skyblue')
ax_bar.set_xlabel('Cidade')
ax_bar.set_ylabel('Número de Ocorrências')
ax_bar.set_title('Top 5 Cidades com Maior Número de Ocorrências')
st.pyplot(fig_bar)

# Número de ocorrências por estado (Gráfico de Barras)
st.subheader('Ocorrências por Estado')
occurrences_by_state = data['ocorrencia_uf'].value_counts()
fig_bar_state, ax_bar_state = plt.subplots()
occurrences_by_state.plot(kind='bar', ax=ax_bar_state, color='lightgreen')
ax_bar_state.set_xlabel('Estado')
ax_bar_state.set_ylabel('Número de Ocorrências')
ax_bar_state.set_title('Ocorrências por Estado')
st.pyplot(fig_bar_state)

# Média de recomendações por ocorrência
st.subheader('Média de Recomendações por Ocorrência')
avg_recommendations = data['total_recomendacoes'].mean()
st.write(f"A média de recomendações por ocorrência é de: **{avg_recommendations:.2f}**")

# Tipo de ocorrência mais comum (Gráfico de Pizza)
st.subheader('Tipo de Ocorrência Mais Comum')
most_common_type = data['ocorrencia_tipo_categoria'].mode().values[0]
count_most_common_type = data['ocorrencia_tipo_categoria'].value_counts().max()
st.write(f"O tipo de ocorrência mais comum é: *{most_common_type}*, com um total de {count_most_common_type} ocorrências.")

# Fase de operação com maior número de fatalidades (Gráfico de Barras)
st.subheader('Fase de Operação com Maior Número de Fatalidades')
phase_fatalities = data.groupby('aeronave_fase_operacao')['aeronave_fatalidades_total'].sum().nlargest(5)
fig_bar_fatalities, ax_bar_fatalities = plt.subplots()
phase_fatalities.plot(kind='bar', ax=ax_bar_fatalities, color='salmon')
ax_bar_fatalities.set_xlabel('Fase de Operação')
ax_bar_fatalities.set_ylabel('Fatalidades')
ax_bar_fatalities.set_title('Fase de Operação com Maior Número de Fatalidades')
st.pyplot(fig_bar_fatalities)

#grafico barras
fig_ano = px.bar(df_acidentes_cleaned, x='ocorrencia_dia', y='total_aeronaves_envolvidas', title='Distribuição de Acidentes Aéreos por Ano')
st.plotly_chart(fig_ano)

df = pd.read_excel("acidentesTransito_cenipa_2010a2021.xlsx")

x_column = st.selectbox("Selecione a coluna para o eixo x:", df.columns)
y_column = st.selectbox("Selecione a coluna para o eixo y:", df.columns)

# Criando um gráfico de dispersão com regressão linear
# Verifica se as colunas selecionadas são numéricas
if pd.api.types.is_numeric_dtype(df[x_column]) and pd.api.types.is_numeric_dtype(df[y_column]):
    # Criando um gráfico de dispersão com regressão linear apenas se ambas as colunas forem numéricas
    fig = px.scatter(df, x=x_column, y=y_column, trendline='ols', title='Gráfico de Dispersão com Regressão Linear')
    st.plotly_chart(fig)
else:
    st.write("Erro: Uma ou ambas as colunas selecionadas não são numéricas.")
