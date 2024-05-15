from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import requests
import uvicorn

def filter_by_types(data, types: list):
    filter = []
    for type in types:
        filter.append(data.loc[data['type'] == type])
    res = pd.concat(filter, ignore_index=True)
    return res

def data_by_param(data, param, filter_list: list):
    filter = []
    for f in filter_list:
        filter.append(data.loc[param == f])
    services_res = pd.concat(filter, ignore_index=True)
    return services_res

df = pd.DataFrame(requests.get('http://server:8000/houses_all').json())
df2 = pd.DataFrame(requests.get('http://server:8000/services_all').json())
df3 = pd.DataFrame(requests.get('http://server:8000/prices_all').json())
print(df['lat'])


app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(df['type'].unique(), id='types_filter', value=df['type'].unique(), multi=True, style={'width': '100%'}),
            dcc.Dropdown(df2['name'].unique(), id='services_filter', value=df2['name'].unique(), multi=True, style={'width': '100%'}),

        ], style={'display': 'flex', 'flexDirection': 'row'}),
     dcc.RangeSlider(df3['price'].min(), df3['price'].max(), step=1, marks=None,
                        tooltip={"always_visible": True, "template": "{value} руб/сутки"},
                        value=[df3['price'].min(), df3['price'].max()], id='prices_filter'),

    ], style={'display': 'flex', 'flexDirection': 'column'}),
    html.Div([
        dcc.Graph(id='map', style={'width': '100%'}),
        html.Div([
            dcc.Graph(id='services', style={'width': '100%', 'height': '10%'}),
            html.Div([
                html.Div([
                    dcc.Dropdown(['Тип объекта', 'Тип услуг'], id='pie_param', value='Тип объекта',
                                 style={'width': '100%'}),
                    dcc.Graph(id='types', style={'width': '100%'}),
                ], style={'display': 'flex', 'flexDirection': 'column', 'width': '100%'}),

                dcc.Graph(id='price', style={'width': '100%'})
            ], style={'display': 'flex', 'flexDirection': 'row', 'width': '100%'}),

        ], style={'display': 'flex', 'flexDirection': 'column', 'width': '100%', 'height': '10%'}),

    ], style={'display': 'flex', 'flexDirection': 'row'})

], style={'display': 'flex', 'flexDirection': 'column'})


@callback(
        Output('map', 'figure'),
        Input('types_filter', 'value'),
        Input('services_filter', 'value'),
        Input('prices_filter', 'value'))
def update_map(types, services, prices):
        filter = pd.DataFrame(requests.post("http://server:8000/filter_houses",
                                        json={'types': types, 'services': services,
                                              'min_price': prices[0],
                                              'max_price': prices[1]}).json())
        fig = px.scatter_mapbox(zoom=5, lat=filter['lat'], lon=filter['lon'],
            color=filter['type'], title='Карта средств размещения' )
        fig.update_layout(
                        mapbox_style='carto-positron',
                        mapbox_center={'lat': filter['lat'].mean(),
                                       'lon': filter['lon'].mean()})
        return fig

@callback(
        Output('types', 'figure'),
        Input('pie_param', 'value'),
        Input('types_filter', 'value'),
        Input('services_filter', 'value'),
        Input('prices_filter', 'value'))
def update_types(pie_param, types, services, prices):
        if pie_param == 'Тип объекта':
            filter = pd.DataFrame(requests.post("http://server:8000/filter_houses",
                                                json={'types': types, 'services': services, 'min_price': prices[0],
                                                      'max_price': prices[1]}).json())


            fig = px.pie(filter, values='id', names='type', title=f'{pie_param}: процентное соотношение')
        else:
            filter = pd.DataFrame(requests.post("http://server:8000/filter_services",
                                                json={'types': types, 'services': services, 'min_price': prices[0],
                                                      'max_price': prices[1]}).json())
            fig = px.pie(filter, values='id', names='service_type', title=f'{pie_param}: процентное соотношение')
        return fig


@callback(
        Output('services', 'figure'),
        Input('types_filter', 'value'),
        Input('services_filter', 'value'),
        Input('prices_filter', 'value'))
def update_serv(types, services, prices):
        filter = pd.DataFrame(requests.post("http://server:8000/filter_services",
                                            json={'types': types, 'services': services, 'min_price': prices[0],
                                                  'max_price': prices[1]}).json())
        fig = px.histogram(x=filter['name'], y=filter['id'], histfunc='count', title='Популярность предоставляемых услуг', labels={'x': 'Услуга', 'y': 'Количество'} )
        return fig

@callback(
        Output('price', 'figure'),

        Input('types_filter', 'value'),
        Input('services_filter', 'value'),
        Input('prices_filter', 'value'))
def update_price(types, services, prices):
        filter = requests.post("http://server:8000/filter_mean_prices", json={'types': types, 'services': services, 'min_price': prices[0],
                                                      'max_price': prices[1]}).json()
        print(filter)
        fig = px.line(x=filter.keys(), y=filter.values(), title='Динамика цен\nотносительно типа объекта', labels={'x': 'Тип объекта', 'y': 'Средняя цена, руб/сутки'} )
        return fig





if __name__ == '__main__':
    app.run('0.0.0.0', 8050)



