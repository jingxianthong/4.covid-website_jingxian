import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Read the CSV file
read_local_csv = 'cases_state.csv'
df = pd.read_csv(read_local_csv)

# Correct column names
columns_to_use = ['date', 'state', 'cases_new', 'cases_import', 'cases_recovered', 'cases_active']

# Filter columns
df_filtered = df.loc[:, columns_to_use]

# Convert the 'date' column to datetime format and format to only show the date part
df_filtered['date'] = pd.to_datetime(df_filtered['date']).dt.date

# Extract years
df_filtered['year'] = df_filtered['date'].apply(lambda x: x.year)

# Get unique states and years
states = df_filtered['state'].unique()
years = df_filtered['year'].unique()

# Initialize the Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("New COVID-19 Cases Over Time by State"),
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
    dcc.Graph(id='cases-graph'),
])

@app.callback(
    Output('cases-graph', 'figure'),
    [Input('state-dropdown', 'value')]
)
def update_graph(selected_states):
    if 'all' in selected_states:
        filtered_df = df_filtered  # Select all states
    else:
        filtered_df = df_filtered[df_filtered['state'].isin(selected_states)]
    
    fig = px.line(filtered_df, x='date', y='cases_new', color='state', title="New COVID-19 Cases Over Time by State")
    fig.update_layout(
        width=800,  # Set the width of the graph
        height=400,  # Set the height of the graph
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
