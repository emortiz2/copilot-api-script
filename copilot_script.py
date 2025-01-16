import requests
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("AUTH_TOKEN")

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": TOKEN,
    "X-GitHub-Api-Version": "2022-11-28",
}

response = requests.get('https://api.github.com/orgs/SquareTrade/copilot/metrics', headers=headers)

print(response.json())

outfile = './data/metrics.json'
with open(outfile, 'w') as f:
    f.write(response.text)
