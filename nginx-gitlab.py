import os
import subprocess
import socket
import pandas as pd
import requests

def clone_repos(repo_urls, destination_dir):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    
    for url in repo_urls:
        repo_name = url.split('/')[-1].replace('.git', '')
        repo_path = os.path.join(destination_dir, repo_name)
        
        if os.path.exists(repo_path):
            print(f"Repository '{repo_name}' already exists in {destination_dir}. Skipping...")
        else:
            print(f"Cloning repository '{repo_name}'...")
            try:
                subprocess.run(['git', 'clone', url, repo_path], check=True)
                print(f"Successfully cloned '{repo_name}' to '{repo_path}'.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to clone '{repo_name}'. Error: {e}")

def extract_server_names(directory):
    server_names = []
    sites_enabled_dir = os.path.join(directory, 'sites-enabled')
    
    if os.path.exists(sites_enabled_dir):
        for root, dirs, files in os.walk(sites_enabled_dir):
            for file in files:
                if file.endswith('.conf'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        for line in f:
                            if 'server_name' in line:
                                names = [name.strip(';') for name in line.split()[1:]]
                                server_names.extend(names)  # Append each name to the list
    else:
        print(f"No 'sites-enabled' directory found in {directory}. Skipping...")
    
    return server_names

def check_dns_availability(server_name):
    try:
        socket.gethostbyname(server_name)
        print(f"{server_name} available")
        try:
            response = requests.get(f"http://{server_name}", timeout=10)
            if response.status_code == 502:
                print(f"{server_name} returned 502 Bad Gateway")
                return "502 by NGINX"
            else:
                return "Available"
        except requests.exceptions.Timeout:
            print(f"{server_name} request timed out")
            return "Timeout"
        except requests.exceptions.RequestException as e:
            print(f"Error accessing {server_name}: {e}")
            return "NOT Available"
    except socket.error:
        print(f"{server_name} not available")
        return "NOT Available"

def create_excel_for_repo(repo_name, server_names):
    results = []
    for name in server_names:
        dns_status = check_dns_availability(name)
        results.append({"Server Name": name, "DNS Status": dns_status})

    df = pd.DataFrame(results)
    excel_filename = f"{repo_name}_server_status.xlsx"
    df.to_excel(excel_filename, index=False)
    print(f"Excel file created: {excel_filename}")

## Aşağıdaki username ve api-tokenın değiştirilmesi gerekiyor.

def main():
    repositories = [
        "https://pelin.erdogan:d5nVRzKg2Va4AR-rwvBz@git.odeal.com/odeal/devops/internal-nginx-configs.git",
        "https://pelin.erdogan:d5nVRzKg2Va4AR-rwvBz@git.odeal.com/odeal/devops/prod-nginx-configs.git",
        "https://pelin.erdogan:d5nVRzKg2Va4AR-rwvBz@git.odeal.com/odeal/devops/stage-nginx-configs.git"
    ]

    destination_directory = "./cloned_repos"

    # Clone the repositories
    clone_repos(repositories, destination_directory)

    # Process each repository separately
    for repo in repositories:
        repo_name = repo.split('/')[-1].replace('.git', '')
        repo_path = os.path.join(destination_directory, repo_name)
        
        # Extract server names from configuration files in 'sites-enabled' directory
        server_names = extract_server_names(repo_path)

        # Create an Excel file for this repository
        create_excel_for_repo(repo_name, server_names)

if __name__ == "__main__":
    main()
