import requests

# URL of the CSV file
url = 'https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_state.csv'

# Send a GET request to the URL
response = requests.get(url)

# Raise an exception if the request was unsuccessful
response.raise_for_status()

# Write the content to a local file
with open('cases_state.csv', 'wb') as file:
    file.write(response.content)

print("File downloaded successfully")
