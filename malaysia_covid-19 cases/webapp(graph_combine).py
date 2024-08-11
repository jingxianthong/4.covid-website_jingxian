import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Read the CSV files
df_cases = pd.read_csv('cases_state.csv')
df_deaths = pd.read_csv('cases_deadcCovid.csv')

# Process the cases data
columns_cases = ['date', 'state', 'cases_new', 'cases_import', 'cases_recovered', 'cases_active']
df_cases_filtered = df_cases.loc[:, columns_cases]
df_cases_filtered['date'] = pd.to_datetime(df_cases_filtered['date']).dt.date
df_cases_filtered['year'] = df_cases_filtered['date'].apply(lambda x: x.year)
states = df_cases_filtered['state'].unique()

# Process the deaths data
columns_deaths = ['date', 'deaths_new']
df_deaths_filtered = df_deaths.loc[:, columns_deaths]
df_deaths_filtered['date'] = pd.to_datetime(df_deaths_filtered['date']).dt.date

# Initialize the Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("COVID-19 Dashboard"),
    
    html.Div([
        html.H2("New COVID-19 Cases"),
        dcc.Dropdown(
            id='state-dropdown',
            options=[
                {'label': 'Select All', 'value': 'all'},
                * [{'label': state, 'value': state} for state in states]
            ],
            value=['all'],  # Default selected state is "Select All"
            multi=True,
            placeholder="Select state(s)"
        ),
        dcc.Graph(id='cases-graph')
    ]),
    
    html.Div([
        dcc.Graph(
            id='deaths-graph',
            figure=px.line(df_deaths_filtered, x='date', y='deaths_new', title=" Death Cases ")
        )
    ])
])

@app.callback(
    Output('cases-graph', 'figure'),
    [Input('state-dropdown', 'value')]
)
def update_cases_graph(selected_states):
    if 'all' in selected_states:
        filtered_df = df_cases_filtered  # Select all states
    else:
        filtered_df = df_cases_filtered[df_cases_filtered['state'].isin(selected_states)]
    
    fig = px.line(filtered_df, x='date', y='cases_new', color='state', title="Cases - State")
    fig.update_layout()
    return fig


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)
