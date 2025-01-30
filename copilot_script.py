import requests
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("AUTH_TOKEN")
ORG = 'SquareTrade'

# Headers: 
# Accept: application/vnd.github+json
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f'Bearer {TOKEN}',
    "X-GitHub-Api-Version": "2022-11-28",
}

# path parameters:
# org: SquareTrade **REQUIRED**
# team_slug: name of team name
PATH = f'https://api.github.com/orgs/{ORG}/copilot/metrics'

# Query parameters:
# since: usage metrics since this date (YYYY-MM-DD) ** max 28 days
# until: usage metrics until this date (YYYY-MM-DD) should not preceed the since date/ go into future
# page: page number of the results to fetch
# per_page: number of days of metrics to display per page ** max 28 days
params = {
    'since': '2025-01-27',
}

response = requests.get(PATH, headers=headers, verify=False, params=params)

print(response.json())

outfile = './data/metrics.json'
with open(outfile, 'w') as f:
    f.write(response.json())
