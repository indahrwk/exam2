import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from sqlalchemy import create_engine
# from categoryplot import dfPokemon, getPlot
from dash.dependencies import Input, Output

engine = create_engine("mysql+mysqlconnector://root:1234@localhost/titanic?host=localhost?port=3306")
conn = engine.connect()

color_set = ['#000000','#FCE63D']

app = dash.Dash(__name__)

def generate_table(dataframe, max_rows=10) :
    return html.Table(
         # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(str(dataframe[col][i])) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )
app.title = 'Dashboard Titanic'

# LAYOUT
app.layout = html.Div(children=[
    html.H1(children='Dashboard Titanic',className='titleDashboard'),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Titanic Dataset', value='tab-1',children=[
            html.Div([
                html.H1('Data Titanic', className='h1'),
                generate_table(df_titanic)
            ])
        ]),
        dcc.Tab(label='Categorical Plot', value='tab-1',children=[
            html.Div([
                html.H1('Categorical Plot Titanic', className='h1'),
                html.Div(children=[
                    html.Div([
                        dcc.Dropdown(
                            id='jenisPlot',
                            options=[{'label': i.capitalize(), 'value': i} for i in ['bar','box','violin']],
                            value='bar'
                        )
                    ],className='col-6')
                ],className='row'),
                dcc.Graph(
                    id='categoricalPlot'
                )
            ])
        ])
        ], style={
        'fontFamily': 'system-ui'
    }, content_style={
        'fontFamily': 'Arial',
        'borderBottom': '1px solid #d6d6d6',
        'borderLeft': '1px solid #d6d6d6',
        'borderRight': '1px solid #d6d6d6',
        'padding': '44px'
    })
], style={
    'maxWidth': '1200px',
    'margin': '0 auto'
})

@app.callback(
    Output(component_id='categoricalPlot', component_property='figure'),
    [Input(component_id='jenisPlot', component_property='value')]
)
def update_graph_categorical(jenisPlot):
    return {
        'data': getPlot(jenisPlot),
        'layout': go.Layout(
                    xaxis={'title': 'Generation'},
                    yaxis={'title': 'Total Stat'},
                    margin=dict(l=40,b=40,t=10,r=10),
                    # legend=dict(x=0,y=1), 
                    hovermode='closest',
                    boxmode='group',violinmode='group'
                )
    }
