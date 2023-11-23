import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc

# datos de acciones y calcular retornos
def obtener_datos_acciones(tickers, inicio, fin):
    datos = yf.download(tickers, start=inicio, end=fin)['Adj Close']
    retornos = datos.pct_change().dropna()
    return datos, retornos


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server=app.server

# tickers y rango de fechas
tickers = ['NSRGY', 'PEP', 'KO', 'MSFT', 'JNJ', 'TSLA']
fecha_inicio = '2022-01-01'
fecha_fin = '2023-01-01'


datos_acciones, retornos_acciones = obtener_datos_acciones(tickers, fecha_inicio, fecha_fin)





# Layout de la aplicación
app.layout = html.Div(children=[
    html.H1(children='Dashboard de Acciones'),

    dcc.RangeSlider(
        id='date-slider',
        marks={i: {'label': str(date.strftime('%Y-%m-%d')), 'style':{"transform": "rotate(90deg)"}
                  } for i, date in enumerate(datos_acciones.index, start=1) if i % 15 == 0
               },
        min=1,
        max=len(datos_acciones),
        step=1,
        value=[1, len(datos_acciones)],
        tooltip={'placement': 'bottom', 'always_visible': True}
    ),

    dcc.Graph(
        id='precios-grafico',
    ),

    dcc.Graph(
        id='retornos-grafico',
    )
])

#filtro temporal
@app.callback(
    [Output('precios-grafico', 'figure'),
     Output('retornos-grafico', 'figure')],
    [Input('date-slider', 'value')]
)
def update_graph(selected_dates):
    start_date = datos_acciones.index[selected_dates[0]-1]
    end_date = datos_acciones.index[selected_dates[1]-1]

    filtered_prices = datos_acciones[start_date:end_date]
    filtered_returns = retornos_acciones[start_date:end_date]

    fig_prices = go.Figure()
    for columna in filtered_prices.columns:
        fig_prices.add_trace(go.Scatter(x=filtered_prices.index, y=filtered_prices[columna],
                                       mode='lines', name=columna))

    fig_prices.update_layout(title='Precios de Acciones',
                             xaxis_title='Fecha',
                             yaxis_title='Precio')

    fig_returns = go.Figure()
    for columna in filtered_returns.columns:
        fig_returns.add_trace(go.Scatter(x=filtered_returns.index, y=filtered_returns[columna],
                                        mode='lines', name=columna))

    fig_returns.update_layout(title='Retornos de Acciones',
                              xaxis_title='Fecha',
                              yaxis_title='Retorno')

    return fig_prices, fig_returns

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0',port=10000)


