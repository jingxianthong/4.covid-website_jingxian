import pandas as pd

# Read the CSV file
df = pd.read_csv('cases_state.csv')

# Convert DataFrame to HTML table with DataTables ID
table_html = df.to_html(index=False, table_id="dataTable")  # Add table_id for DataTables

# Define the columns to use
columns_to_use = ['date', 'state', 'cases_new', 'cases_import', 'cases_recovered', 'cases_active']

# Get the correct column names
state_column = 'state'  # This is the correct column name based on your earlier check
date_column = 'date'  # Assuming the date column is named 'date'

# Convert the 'date' column to datetime format and extract the year
df[date_column] = pd.to_datetime(df[date_column])
df['year'] = df[date_column].dt.year

# Get unique states and years
states = df[state_column].unique()
years = df['year'].unique()

html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <title>COVID Cases by State and Year</title>
    <style>
        table {{
            border-collapse: collapse;
            width: 100%;
            margin-top: 20px;
        }}
        th, td {{
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        select {{
            margin: 0 10px 0 0;  /* Adjust margin to bring dropdowns closer */
            padding: 8px;
            font-size: 16px;
        }}
        .dropdown-container {{
            margin: 20px 0;
            display: flex;
            align-items: center;
        }}
        .dropdown-container label {{
            margin-right: 10px;  /* Space between label and dropdown */
        }}
    </style>
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.12.1/css/jquery.dataTables.min.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.12.1/js/jquery.dataTables.min.js"></script>
</head>
<body>
    <h1>COVID Cases by State and Year</h1>
    <div class="dropdown-container">
        <label for="stateFilter">Choose a state:</label>
        <select id="stateFilter">
            <option value="">All</option>
            {''.join([f'<option value="{state}">{state}</option>' for state in states])}
        </select>
        <label for="yearFilter">Choose a year:</label>
        <select id="yearFilter">
            <option value="">All</option>
            {''.join([f'<option value="{year}">{year}</option>' for year in sorted(years)])}
        </select>
    </div>
    <br><br>
    {table_html}
    <script>
        $(document).ready(function() {{
            var table = $('#dataTable').DataTable();

            // Debugging step: Log the table structure to find column indexes
            console.log('Table columns:', table.columns().header().toArray().map(header => $(header).text()));

            $('#stateFilter, #yearFilter').on('change', function() {{
                var selectedState = $('#stateFilter').val();
                var selectedYear = $('#yearFilter').val();

                // Use column indexes based on the actual table structure
                table
                    .column(1).search(selectedState === "" ? "" : selectedState)
                    .column(0).search(selectedYear === "" ? "" : selectedYear)
                    .draw();
            }});
        }});
    </script>
</body>
</html>
"""

# Save the HTML to a file
with open('cases_testing.html', 'w') as file:
    file.write(html_template)
