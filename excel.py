import pandas as pd

# Read input from a text file
with open('/Users/ozanbozkurt/git/python/nginx/internal.txt', 'r') as file:
    lines = file.readlines()

# Process the input and create a DataFrame
data = []
current_server_name = None

for line in lines:
    line = line.strip()

    if line.startswith('Server Name:'):
        server_name_parts = line.split(': ', 1)
        if len(server_name_parts) > 1:
            current_server_name = server_name_parts[1]
        else:
            current_server_name = None
    elif line.startswith('Endpoint:'):
        endpoint_parts = line.split(': ', 1)
        if current_server_name and len(endpoint_parts) > 1:
            endpoint = endpoint_parts[1]
            data.append((current_server_name, endpoint, ''))

# Create a DataFrame
df = pd.DataFrame(data, columns=['URL', 'Endpoint', 'Host'])

# Save DataFrame to Excel file
df.to_excel('internal.xlsx', index=False)