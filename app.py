# dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px

# ========================
# Carregar os Dados
# ========================
df = pd.read_csv('vgsales.csv')
df = df.dropna(subset=['Year'])

# ========================
# Funções auxiliares
# ========================
def resumo_eda():
    st.title('Resumo da Análise Exploratória')

    genero_mais_vendido = df.groupby('Genre')['Global_Sales'].sum().idxmax()
    plataforma_mais_vendida = df.groupby('Platform')['Global_Sales'].sum().idxmax()
    ano_mais_vendas = int(df.groupby('Year')['Global_Sales'].sum().idxmax())

    st.subheader('Principais Indicadores')
    st.write(f'**Gênero Mais Vendido:** {genero_mais_vendido}')
    st.write(f'**Plataforma Mais Vendida:** {plataforma_mais_vendida}')
    st.write(f'**Ano com Mais Vendas:** {ano_mais_vendas}')

    st.subheader('Distribuição de Jogos por Plataforma')
    fig = px.bar(df.groupby('Platform').size().reset_index(name='Quantidade'),
                 x='Platform', y='Quantidade')
    st.plotly_chart(fig)

    st.subheader('Distribuição das Vendas Globais por Plataforma')
    fig = px.pie(df, names='Platform', values='Global_Sales')
    st.plotly_chart(fig)

    st.subheader('Top 10 Jogos Mais Vendidos')
    top10 = df.sort_values(by='Global_Sales', ascending=False).head(10)
    fig = px.bar(top10, x='Name', y='Global_Sales', color='Platform')
    st.plotly_chart(fig)

    st.subheader('Vendas por Região - América do Norte')
    fig = px.bar(df.groupby('Platform')['NA_Sales'].sum().reset_index(),
                 x='Platform', y='NA_Sales', labels={'NA_Sales': 'Vendas (milhões)'})
    st.plotly_chart(fig)

    st.subheader('Vendas por Região - Europa')
    fig = px.bar(df.groupby('Platform')['EU_Sales'].sum().reset_index(),
                 x='Platform', y='EU_Sales', labels={'EU_Sales': 'Vendas (milhões)'})
    st.plotly_chart(fig)

    st.subheader('Vendas por Região - Japão')
    fig = px.bar(df.groupby('Platform')['JP_Sales'].sum().reset_index(),
                 x='Platform', y='JP_Sales', labels={'JP_Sales': 'Vendas (milhões)'})
    st.plotly_chart(fig)

    st.subheader('Vendas por Região - Outras')
    fig = px.bar(df.groupby('Platform')['Other_Sales'].sum().reset_index(),
                 x='Platform', y='Other_Sales', labels={'Other_Sales': 'Vendas (milhões)'})
    st.plotly_chart(fig)

    st.subheader('Evolução das Vendas Globais por Ano')
    fig = px.line(df.groupby('Year')['Global_Sales'].sum().reset_index(),
                  x='Year', y='Global_Sales')
    st.plotly_chart(fig)


def vendas_por_genero():
    st.title('Vendas por Gênero')

    genero = st.selectbox('Selecione o Gênero:', df['Genre'].unique())
    ano = st.slider('Selecione o Ano:', int(df['Year'].min()), int(df['Year'].max()), int(df['Year'].min()))

    filtered_df = df[(df['Genre'] == genero) & (df['Year'] == ano)]

    if filtered_df.empty:
        st.warning('Nenhum dado encontrado para os filtros selecionados.')
    else:
        fig = px.bar(filtered_df, x='Name', y='Global_Sales',
                     title=f'Vendas Globais - {genero} ({ano})')
        st.plotly_chart(fig)


def vendas_por_plataforma():
    st.title('Vendas por Plataforma')

    plataforma = st.selectbox('Selecione a Plataforma:', df['Platform'].unique())

    filtered_df = df[df['Platform'] == plataforma]

    if filtered_df.empty:
        st.warning('Nenhum dado encontrado para a plataforma selecionada.')
    else:
        fig = px.histogram(filtered_df, x='Genre', y='Global_Sales', color='Genre',
                           title=f'Vendas por Gênero na Plataforma {plataforma}')
        st.plotly_chart(fig)

# ========================
# Menu lateral
# ========================
st.sidebar.title('Menu')
page = st.sidebar.radio('Navegar para:', ['Resumo da EDA', 'Vendas por Gênero', 'Vendas por Plataforma'])

if page == 'Resumo da EDA':
    resumo_eda()
elif page == 'Vendas por Gênero':
    vendas_por_genero()
elif page == 'Vendas por Plataforma':
    vendas_por_plataforma()
