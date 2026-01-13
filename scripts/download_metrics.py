"""
Download DORA metrics artifacts from GitHub Actions workflows
"""
import os
import json
import requests
from datetime import datetime, timedelta

def download_metrics():
    """Download metrics artifacts from GitHub Actions"""
    
    # Get environment variables
    github_token = os.environ.get('GITHUB_TOKEN')
    github_repository = os.environ.get('GITHUB_REPOSITORY', 'owner/repo')
    
    if not github_token:
        print("Error: GITHUB_TOKEN not set")
        return
    
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Create metrics directory
    os.makedirs('metrics/raw', exist_ok=True)
    
    # Get workflow runs from the last 90 days
    since_date = (datetime.now() - timedelta(days=90)).isoformat()
    
    # Fetch artifacts
    url = f'https://api.github.com/repos/{github_repository}/actions/artifacts'
    params = {
        'per_page': 100,
        'page': 1
    }
    
    all_artifacts = []
    
    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error fetching artifacts: {response.status_code}")
            break
        
        data = response.json()
        artifacts = data.get('artifacts', [])
        
        if not artifacts:
            break
        
        # Filter DORA metrics artifacts
        dora_artifacts = [
            a for a in artifacts 
            if 'dora-metrics' in a['name']
        ]
        
        all_artifacts.extend(dora_artifacts)
        
        # Check if there are more pages
        if len(artifacts) < 100:
            break
        
        params['page'] += 1
    
    print(f"Found {len(all_artifacts)} DORA metrics artifacts")
    
    # Download each artifact
    for artifact in all_artifacts:
        artifact_name = artifact['name']
        artifact_url = artifact['archive_download_url']
        
        print(f"Downloading {artifact_name}...")
        
        response = requests.get(artifact_url, headers=headers)
        
        if response.status_code == 200:
            filename = f"metrics/raw/{artifact_name}.zip"
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            # Unzip the artifact
            import zipfile
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                zip_ref.extractall(f'metrics/raw/{artifact_name}')
            
            # Remove zip file
            os.remove(filename)
        else:
            print(f"Error downloading {artifact_name}: {response.status_code}")
    
    print("Metrics download complete")

if __name__ == '__main__':
    download_metrics()
