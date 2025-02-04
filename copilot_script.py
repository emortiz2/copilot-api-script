import requests
import os
import json
from dotenv import load_dotenv
from datetime import date, timedelta

load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")

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
ORG = 'SquareTrade'
# TEAM_SLUG = '/team/Copilot-test'
TEAM_SLUG = ''
PATH = f'https://api.github.com/orgs/{ORG}{TEAM_SLUG}/copilot/metrics'

# Query parameters:
# since: usage metrics since this date (YYYY-MM-DD) ** max 28 days
# until: usage metrics until this date (YYYY-MM-DD) should not preceed the since date/ go into future
# page: page number of the results to fetch
# per_page: number of days of metrics to display per page ** max 28 days
DATE = date.today() - timedelta(days=1)
params = {
    # 'since': DATE,
}
try:
    response = requests.get(PATH, headers=headers, params=params)
except requests.exceptions.RequestException as e:
    print('Error: ', e)
    exit()


if(response.status_code != 200):
    print('Error: ', response.json())
    exit()

if(response.status_code == 200):
    print('Success. Status code: ', response.status_code)

data = response.json()
outfile = './data/1-31.json'
with open(outfile, 'w') as f:
    json.dump(response.json(), f)

