import pandas as pd

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

# Generate HTML with dropdowns for state and year
html_str = """
<!DOCTYPE html>
<html>
<head>
    <title>COVID-19 Cases in Malaysia</title>
    <!-- Include jQuery and DataTables CSS/JS -->
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.12.1/css/jquery.dataTables.min.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.12.1/js/jquery.dataTables.min.js"></script>
    <script>
        $(document).ready(function() {
            var table = $('#dataTable').DataTable({
                "paging": true,
                "searching": true,
                "info": false,
                "ordering": true
            }); // Initialize DataTables

            // Filtering function
            $('#stateDropdown, #yearDropdown').change(function() {
                var state = $('#stateDropdown').val();
                var year = $('#yearDropdown').val();
                
                table
                    .columns(1).search(state === "All" ? "" : state)
                    .columns(0).search(year === "All" ? "" : year)
                    .draw();
            });
        });
    </script>

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
</head>
<body>
    <h1>COVID-19 Cases in Malaysia</h1>
    <div class="dropdown-container">
        <label for="stateDropdown">Select State:</label>
        <select id="stateDropdown">
            <option value="All">All</option>
"""

# Add options to the state dropdown
for state in states:
    html_str += f'<option value="{state}">{state}</option>\n'

html_str += """
        </select>
        <label for="yearDropdown">Select Year:</label>
        <select id="yearDropdown">
            <option value="All">All</option>
"""

# Add options to the year dropdown
for year in sorted(years):
    html_str += f'<option value="{year}">{year}</option>\n'

html_str += """
        </select>
    </div>
    <br><br>
"""

# Convert the full DataFrame to HTML and append to the HTML string
html_str += df_filtered.to_html(index=False, table_id="dataTable", classes='display')

html_str += """
</body>
</html>
"""

# Save the HTML string to a file
with open('cases_state.html', 'w') as f:
    f.write(html_str)

print("HTML file generated successfully")
