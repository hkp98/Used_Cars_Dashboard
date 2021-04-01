import dash  # use Dash version 1.16.0 or higher for this app to work
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from numpy.core.shape_base import stack
import plotly.express as px
import pandas as pd 

df = pd.read_csv("page2.csv")
df_1 = pd.read_csv("bar_plot.csv")
df = df.groupby(["car_year","state"]).mean()
df = df.add_suffix('_Average').reset_index()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Dropdown(id='dpdn2', value=['NJ','NY'], multi=True,
                 options=[{'label': x, 'value': x} for x in
                          df.state.unique()]),
    html.Div([
        dcc.Graph(id='pie-graph', figure={}, className='six columns'),
        dcc.Graph(id='my-graph', figure={}, clickData=None, hoverData=None, # I assigned None for tutorial purposes. By defualt, these are None, unless you specify otherwise.
                  config={
                      'staticPlot': False,     # True, False
                      'scrollZoom': True,      # True, False
                      'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                      'showTips': False,       # True, False
                      'displayModeBar': True,  # True, False, 'hover'
                      'watermark': True,
                      # 'modeBarButtonsToRemove': ['pan2d','select2d'],
                        },
                  className='six columns'
                  ),
        dcc.Graph(id='bar-graph',figure={},className='six columns')
    ])
])


@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='dpdn2', component_property='value'),
)
def update_graph(state_chosen):
    dff = df[df.state.isin(state_chosen)]
    fig = px.line(data_frame=dff, x='car_year', y='price_Average', color='state',
                  custom_data=['state', 'car_year', 'price_Average','odometer_Average'])
    fig.update_traces(mode='lines+markers')
    return fig


# Dash version 1.16.0 or higher
@app.callback(
    Output(component_id='pie-graph', component_property='figure'),
    Input(component_id='my-graph', component_property='hoverData'),
    Input(component_id='my-graph', component_property='clickData'),
    Input(component_id='my-graph', component_property='selectedData'),
    Input(component_id='dpdn2', component_property='value')
)
def update_side_graph(hov_data, clk_data, slct_data, state_chosen):
    if hov_data is None:
        dff2 = df[df.state.isin(state_chosen)]
        dff2 = dff2[dff2.car_year == 2000]
        print(dff2)
        fig2 = px.pie(data_frame=dff2, values='price_Average', names='state',
                      title='Average Odometer Comparison for 2000')
        return fig2
    else:
        print(f'hover data: {hov_data}')
        # print(hov_data['points'][0]['customdata'][0])
        # print(f'click data: {clk_data}')
        # print(f'selected data: {slct_data}')
        dff2 = df[df.state.isin(state_chosen)]
        hov_year = hov_data['points'][0]['x']
        dff2 = dff2[dff2.car_year == hov_year]
        fig2 = px.pie(data_frame=dff2, values='odometer_Average', names='state', title=f'Average Odometer Comparison: {hov_year}')
        return fig2

@app.callback(
    Output(component_id='bar-graph', component_property='figure'),
    Input(component_id='dpdn2', component_property='value'),
    
)
def update_graph_bottom(state_chosen):
    dff = df_1[df_1.state.isin(state_chosen)]
    fig3 = px.bar(data_frame=dff, x='manufacturer', y='count_manufacturer', color='state',barmode="stack",orientation='v')
    return fig3


if __name__ == '__main__':
    app.run_server(debug=True)