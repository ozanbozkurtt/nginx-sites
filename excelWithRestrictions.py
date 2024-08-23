import pandas as pd
import re

# Read input from the text file
with open('/Users/ozanbozkurt/git/python/nginx/internal.txt', 'r') as file:
    lines = file.readlines()

# Process the input and create lists for Server Name, Endpoint, Allow, and Deny
data = []

current_record = {}

for line in lines:
    line = line.strip()

    if line.startswith('Server Name:'):
        server_name_parts = line.split(': ', 1)
        if len(server_name_parts) > 1 and server_name_parts[1].strip():
            current_record['Server Name'] = server_name_parts[1]
    elif line.startswith('Endpoint:'):
        endpoint_parts = line.split(': ', 1)
        if len(endpoint_parts) > 1:
            current_record['Endpoint'] = endpoint_parts[1]
    elif line.startswith('Allow:'):
        allow_parts = line.split(': ', 1)
        if len(allow_parts) > 1:
            current_record['Allow'] = re.findall(r'Allow:\s+(.+)', line)[0]
    elif line.startswith('Deny:'):
        deny_parts = line.split(': ', 1)
        if len(deny_parts) > 1:
            current_record['Deny'] = re.findall(r'Deny:\s+(.+)', line)[0]

    # If we have a complete record, add it to the list and start a new one
    if 'Server Name' in current_record and 'Endpoint' in current_record and ('Allow' in current_record or 'Deny' in current_record):
        data.append(current_record)
        current_record = {'Server Name': current_record.get('Server Name', 'Unknown')}

# Create a DataFrame
df = pd.DataFrame(data)

# Save DataFrame to Excel file
df.to_excel('internal_with_access.xlsx', index=False)