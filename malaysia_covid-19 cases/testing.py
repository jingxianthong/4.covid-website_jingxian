import pandas as pd

# Read the CSV file
url = 'covid_cases_things.csv'
df = pd.read_csv(url)

# Count and show all unique states
state_counts = df['state'].value_counts()

print('State counts:')
print(state_counts)

# Convert DataFrame to HTML and save
df.to_html('cases_testing.html')
