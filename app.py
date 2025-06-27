pip install dash dash-bootstrap-components plotly pandas
pip install pyngrok
# app.py

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from pyngrok import conf,ngrok


ngrok.set_auth_token("4WQGSVMEexxXk7iauHwRK_28e18qc5jUemtjphkFDBP")
# ==============================
# Carregar os Dados
# ==============================
df = pd.read_csv('vgsales.csv')
df = df.dropna(subset=['Year'])

# Métricas principais
genero_mais_vendido = df.groupby('Genre')['Global_Sales'].sum().idxmax()
plataforma_mais_vendida = df.groupby('Platform')['Global_Sales'].sum().idxmax()
ano_mais_vendas = int(df.groupby('Year')['Global_Sales'].sum().idxmax())

# Listas para filtros
genres = df['Genre'].dropna().unique()
platforms = df['Platform'].dropna().unique()
anos = sorted(df['Year'].dropna().unique())

# ==============================
# Configurar o App
# ==============================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = 'Dashboard de Vendas de Jogos'

# ==============================
# Layout
# ==============================
app.layout = dbc.Container([
    dbc.Row([
        # Sidebar fixo
        html.Div([
            html.H2('Dashboard de Jogos', className='display-6 text-center my-4'),
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink('Resumo da EDA', href='/', active='exact'),
                    dbc.NavLink('Vendas por Gênero', href='/vendas-genero', active='exact'),
                    dbc.NavLink('Vendas por Plataforma', href='/vendas-plataforma', active='exact'),
                ],
                vertical=True,
                pills=True
            )
        ], style={
            'position': 'fixed',
            'top': 0,
            'left': 0,
            'bottom': 0,
            'width': '220px',
            'padding': '20px',
            'background-color': '#f8f9fa',
            'overflow-y': 'auto'
        }),

        # Conteúdo principal
        dbc.Col([
            dcc.Location(id='url'),
            html.Div(id='page-content', style={'margin-left': '240px', 'padding': '20px'})
        ])
    ], className='gx-0')
], fluid=True)

# ==============================
# Páginas do Dashboard
# ==============================
resumo_layout = dbc.Container([
    html.H3('Resumo da Análise Exploratória', className='text-center my-4'),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader('Gênero Mais Vendido'),
            dbc.CardBody(html.H4(f'{genero_mais_vendido}', className='card-title'))
        ], color='primary', inverse=True), width=4),

        dbc.Col(dbc.Card([
            dbc.CardHeader('Plataforma Mais Vendida'),
            dbc.CardBody(html.H4(f'{plataforma_mais_vendida}', className='card-title'))
        ], color='success', inverse=True), width=4),

        dbc.Col(dbc.Card([
            dbc.CardHeader('Ano com Mais Vendas'),
            dbc.CardBody(html.H4(f'{ano_mais_vendas}', className='card-title'))
        ], color='warning', inverse=True), width=4)
    ], className='mb-4'),

    dbc.Row([
        dbc.Col(dcc.Graph(
            figure=px.bar(df.groupby('Platform').size().reset_index(name='Quantidade'),
                          x='Platform', y='Quantidade',
                          title='Distribuição de Jogos por Plataforma')), width=6),

        dbc.Col(dcc.Graph(
            figure=px.pie(df, names='Platform', values='Global_Sales',
                          title='Distribuição das Vendas Globais por Plataforma')), width=6)
    ], className='mb-4'),

    dbc.Row([
        dbc.Col(dcc.Graph(
            figure=px.bar(df.sort_values(by='Global_Sales', ascending=False).head(10),
                          x='Name', y='Global_Sales', color='Platform',
                          title='Top 10 Jogos Mais Vendidos no Mundo'))),
    ], className='mb-4'),

    dbc.Row([
        dbc.Col(dcc.Graph(
            figure=px.bar(df.groupby('Platform')['NA_Sales'].sum().reset_index(),
                          x='Platform', y='NA_Sales',
                          title='Vendas na América do Norte por Plataforma',
                          labels={'NA_Sales': 'Vendas (milhões)'})), width=6),

        dbc.Col(dcc.Graph(
            figure=px.bar(df.groupby('Platform')['EU_Sales'].sum().reset_index(),
                          x='Platform', y='EU_Sales',
                          title='Vendas na Europa por Plataforma',
                          labels={'EU_Sales': 'Vendas (milhões)'})), width=6)
    ], className='mb-4'),

    dbc.Row([
        dbc.Col(dcc.Graph(
            figure=px.bar(df.groupby('Platform')['JP_Sales'].sum().reset_index(),
                          x='Platform', y='JP_Sales',
                          title='Vendas no Japão por Plataforma',
                          labels={'JP_Sales': 'Vendas (milhões)'})), width=6),

        dbc.Col(dcc.Graph(
            figure=px.bar(df.groupby('Platform')['Other_Sales'].sum().reset_index(),
                          x='Platform', y='Other_Sales',
                          title='Vendas em Outras Regiões por Plataforma',
                          labels={'Other_Sales': 'Vendas (milhões)'})), width=6)
    ], className='mb-4'),

    dbc.Row([
        dbc.Col(dcc.Graph(
            figure=px.line(df.groupby('Year')['Global_Sales'].sum().reset_index(),
                           x='Year', y='Global_Sales',
                           title='Evolução das Vendas Globais por Ano')), width=12)
    ], className='mb-4'),

    dbc.Row([
        dbc.Col(dcc.Graph(
            figure=px.bar(df, x='Platform', y='Global_Sales', color='Platform',
                          animation_frame='Year', range_y=[0, df['Global_Sales'].max()],
                          title='Evolução Anual das Vendas Globais por Plataforma')), width=12)
    ])
])

# ==============================
# Página Vendas por Gênero
# ==============================
vendas_genero_layout = dbc.Container([
    html.H3('Vendas por Gênero', className='text-center my-4'),

    dbc.Row([
        dbc.Col([
            html.Label('Selecione o Gênero:'),
            dcc.Dropdown(
                id='dropdown-genero',
                options=[{'label': g, 'value': g} for g in genres],
                value='Action'
            )
        ], width=6),

        dbc.Col([
            html.Label('Selecione o Ano:'),
            dcc.Slider(
                id='slider-ano',
                min=int(min(anos)),
                max=int(max(anos)),
                step=1,
                value=int(min(anos)),
                marks={str(int(year)): str(int(year)) for year in anos}
            )
        ], width=6)
    ], className='mb-4'),

    dbc.Row([
        dbc.Col(dcc.Graph(id='grafico-vendas-genero'), width=12)
    ])
])

# ==============================
# Página Vendas por Plataforma
# ==============================
vendas_plataforma_layout = dbc.Container([
    html.H3('Vendas por Plataforma', className='text-center my-4'),

    dbc.Row([
        dbc.Col([
            html.Label('Selecione a Plataforma:'),
            dcc.Dropdown(
                id='dropdown-plataforma',
                options=[{'label': p, 'value': p} for p in platforms],
                value='PS4'
            )
        ], width=6)
    ], className='mb-4'),

    dbc.Row([
        dbc.Col(dcc.Graph(id='grafico-vendas-plataforma'), width=12)
    ])
])

# ==============================
# Navegação entre Páginas
# ==============================
@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/vendas-genero':
        return vendas_genero_layout
    elif pathname == '/vendas-plataforma':
        return vendas_plataforma_layout
    else:
        return resumo_layout

# ==============================
# Callback Vendas por Gênero
# ==============================
@app.callback(
    Output('grafico-vendas-genero', 'figure'),
    [Input('dropdown-genero', 'value'),
     Input('slider-ano', 'value')]
)
def update_graph_genero(selected_genre, selected_year):
    filtered_df = df[(df['Genre'] == selected_genre) & (df['Year'] == selected_year)]

    if filtered_df.empty:
        fig = px.bar(title='Nenhum dado encontrado para os filtros selecionados.')
    else:
        fig = px.bar(filtered_df, x='Name', y='Global_Sales',
                     title=f'Vendas Globais - {selected_genre} ({selected_year})')

    return fig

# ==============================
# Callback Vendas por Plataforma
# ==============================
@app.callback(
    Output('grafico-vendas-plataforma', 'figure'),
    Input('dropdown-plataforma', 'value')
)
def update_graph_plataforma(selected_platform):
    filtered_df = df[df['Platform'] == selected_platform]

    if filtered_df.empty:
        fig = px.histogram(title='Nenhum dado encontrado para a plataforma selecionada.')
    else:
        fig = px.histogram(filtered_df, x='Genre', y='Global_Sales', color='Genre',
                           title=f'Vendas por Gênero na Plataforma {selected_platform}')

    return fig

# ==============================
# Rodar o servidor local
# ==============================
if __name__ == '__main__':
    app.run(debug=True)

public_url = ngrok.connect(8050)
print('Public URL:', public_url)
