import os
import re

def extract_config(file_path):
    server_names = set()
    endpoints = set()

    with open(file_path, 'r') as f:
        config_content = f.read()

        # Extract server_name
        server_name_match = re.search(r'\bserver_name\s+([^;]+);', config_content)
        if server_name_match:
            server_names.update(server_name_match.group(1).split())

        # Extract locations
        location_matches = re.findall(r'\blocation\s+([^{}]+)\s*{([^}]+)}', config_content)
        for location_match in location_matches:
            location_path = location_match[0].strip()
            # Remove signs: ~, ^, (.*) from locations
            location_path = re.sub(r'~|\^|\(.*\)', '', location_path).strip()
            endpoints.add(location_path)

    return server_names, endpoints

def process_directory(directory_path, output_file_path):
    with open(output_file_path, 'w') as output_file:
        for file_name in os.listdir(directory_path):
            if file_name.endswith('.conf'):
                file_path = os.path.join(directory_path, file_name)
                server_names, endpoints = extract_config(file_path)

                output_file.write(f"Server Name: {', '.join(server_names)}\n")
                
                unique_endpoints = set()
                for endpoint in endpoints:
                    # Avoid duplicate entries
                    if endpoint not in unique_endpoints:
                        output_file.write(f"Endpoint: {endpoint}\n")
                        unique_endpoints.add(endpoint)
                
                output_file.write("\n")

if __name__ == "__main__":
    input_directory = "/Users/ozanbozkurt/stage-nginx-configs/sites-enabled/"
    output_file = "/Users/ozanbozkurt/git/python/nginx/stage.txt"

    process_directory(input_directory, output_file)
    print(f"Configuration details written to {output_file}")