"""
File: version_check.py
Author: Jake Leyhr
GitHub: https://github.com/jakeleyhr/EZgenesynteny/
Date: March 2024
Description: automatically check package version is up to date
"""
# Import dependencies
import importlib.metadata
import requests
from packaging import version

# Check for package updates
def check_for_updates():
    latest_version = None  # Initialize latest_version
    try:
        response = requests.get(f'https://pypi.org/pypi/ezgenesynteny/json')
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        latest_version = data['info']['version']
    except requests.RequestException as e:
        print(f'Error occurred while fetching latest package version: {e}')
        return  # Exit the function if an error occurs

    try:
        current_version = importlib.metadata.version('ezgenesynteny')
        if latest_version and version.parse(latest_version) > version.parse(current_version):
            print(f"Update available: {latest_version}. You are using {current_version}. Run 'pip install ezgenesynteny --upgrade' to get the latest version.")
    except importlib.metadata.PackageNotFoundError:
        pass  # Package is not installed, so version check is not possible

if __name__ == '__main__':
    check_for_updates()
