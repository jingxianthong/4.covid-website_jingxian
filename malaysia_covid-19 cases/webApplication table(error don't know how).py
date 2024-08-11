import pandas as pd
from dash import Dash, dcc, html, Input, Output, dash_table

# Read the CSV file
df = pd.read_csv('cases_state.csv')

# Convert the 'date' column to datetime format and extract the year
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

# Format the 'date' column to remove the time part
df['date'] = df['date'].dt.strftime('%Y-%m-%d')

# Define the columns to use
columns_to_use = ['date', 'state','cases_new','cases_import','cases_recovered','cases_active']

# Get unique states and years
states = df['state'].unique()
years = df['year'].unique()

# Initialize the Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("COVID Cases by State and Year"),
    html.Div([
        html.Div([
            html.Label('Choose a state:', style={'margin-right': '10px'}),
            dcc.Dropdown(
                id='state-filter',
                options=[{'label': state, 'value': state} for state in states],
                value='',  # Default value is empty
                clearable=True,
                placeholder="Select a state",
                style={'width': '200px', 'font-size': '16px'}
            ),
        ], style={'display': 'flex', 'align-items': 'center', 'margin-right': '20px'}),
        html.Div([
            html.Label('Choose a year:', style={'margin-right': '10px'}),
            dcc.Dropdown(
                id='year-filter',
                options=[{'label': year, 'value': year} for year in sorted(years)],
                value='',  # Default value is empty
                clearable=True,
                placeholder="Select a year",
                style={'width': '200px', 'font-size': '16px'}
            ),
        ], style={'display': 'flex', 'align-items': 'center'}),
    ], style={'display': 'flex', 'margin-bottom': '20px'}),
    dash_table.DataTable(
        id='table',
        columns=[{"name": col, "id": col} for col in columns_to_use],
        data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        page_action="native",
        page_size=20,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '5px'},
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
    )
])

@app.callback(
    Output('table', 'data'),
    [Input('state-filter', 'value'),
     Input('year-filter', 'value')]
)
def update_table(selected_state, selected_year):
    filtered_df = df.copy()
    if selected_state:
        filtered_df = filtered_df[filtered_df['state'] == selected_state]
    if selected_year:
        filtered_df = filtered_df[filtered_df['year'] == selected_year]
    return filtered_df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
