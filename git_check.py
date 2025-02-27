import os
import requests
import base64
from dotenv import load_dotenv

def list_github_repositories():
    # Load environment variables from .env file
    load_dotenv()
    
    # Read credentials from environment variables
    github_user = os.getenv("Github_user")
    github_access_token = os.getenv("Github_accessToken")
    
    if not github_user or not github_access_token:
        print("Error: Missing GitHub credentials in .env file.")
        return None
    
    # GitHub API URL for listing user repositories
    url = f"https://api.github.com/users/{github_user}/repos"
    
    # Authentication headers
    headers = {
        "Authorization": f"token {github_access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        repos = response.json()
        print("Your GitHub repositories:")
        repo_names = [repo['name'] for repo in repos]
        for i, repo in enumerate(repo_names, 1):
            print(f"{i}. {repo}")
        print(f"{len(repo_names) + 1}. Create a new repository")
        return repo_names
    else:
        print(f"Error: Unable to fetch repositories (Status Code: {response.status_code})")
        print(response.json())
        return None

def create_github_repository(repo_name):
    load_dotenv()
    github_access_token = os.getenv("Github_accessToken")
    
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {github_access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"name": repo_name, "private": False}
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print(f"Repository '{repo_name}' created successfully.")
        return repo_name
    else:
        print(f"Error: Unable to create repository (Status Code: {response.status_code})")
        print(response.json())
        return None

def upload_file_to_repo(repo_name, file_path):
    load_dotenv()
    github_user = os.getenv("Github_user")
    github_access_token = os.getenv("Github_accessToken")
    
    if not github_user or not github_access_token:
        print("Error: Missing GitHub credentials in .env file.")
        return
    
    url = f"https://api.github.com/repos/{github_user}/{repo_name}/contents/{os.path.basename(file_path)}"
    
    with open(file_path, "rb") as file:
        content = base64.b64encode(file.read()).decode("utf-8")
    
    data = {
        "message": "Adding new file",
        "content": content,
        "branch": "main"
    }
    
    headers = {
        "Authorization": f"token {github_access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
        print(f"File uploaded successfully to {repo_name}.")
    else:
        print(f"Error: Unable to upload file (Status Code: {response.status_code})")
        print(response.json())

if __name__ == "__main__":
    files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f)]
    print("Available files:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")
    print(f"{len(files) + 1}. Enter a custom file path")
    file_choice = int(input("Enter the number of the file you want to upload: ")) - 1
    
    if 0 <= file_choice < len(files):
        selected_file = files[file_choice]
    elif file_choice == len(files):
        selected_file = input("Enter the full path of the file you want to upload: ")
        if not os.path.isfile(selected_file):
            print("Invalid file path.")
            exit()
    else:
        print("Invalid file selection.")
        exit()
    
    repos = list_github_repositories()
    if repos:
        choice = int(input("Enter the number of the repository you want to upload to: ")) - 1
        if 0 <= choice < len(repos):
            upload_file_to_repo(repos[choice], selected_file)
        elif choice == len(repos):
            new_repo_name = input("Enter the name for the new repository: ")
            created_repo = create_github_repository(new_repo_name)
            if created_repo:
                upload_file_to_repo(created_repo, selected_file)
        else:
            print("Invalid repository selection.")
