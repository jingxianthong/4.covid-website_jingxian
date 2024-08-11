import pandas as pd
import plotly.express as px

# Load data from CSV file
CSV_FILE = 'cases_state.csv'
df = pd.read_csv(CSV_FILE)

# Create a line chart using Plotly Express for all states
fig = px.line(
    df,
    x='date',
    y='cases_new',
    color='state',
    title='Daily New COVID-19 Cases by State',
    labels={'cases_new': 'Daily New Cases', 'date': 'Date'},
    line_shape='linear'  # You can choose a different line shape if needed
)

# Save the plot as an HTML file
fig.write_html('cases_state_in_line_chart.html')
