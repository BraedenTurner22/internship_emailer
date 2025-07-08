import requests
import re

def fetch_readme():
    response = requests.get('https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/refs/heads/dev/README.md')

    if response.status_code == 200:
        print("Request to README successful.")
        with open("most_recent_readme.txt", "w") as file:
            file.write(response.text)
    else:
        print("Unable to request data")
