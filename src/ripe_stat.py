"""
RIPE Stat: Metadata Collector
"""

import json
import requests
import pandas as pd
import sys

# INPUTS
DATE = str(sys.argv[1]) # Date to lookup (YYYY-MM-DD), e.g. 2023-06-01
COUNTRY_LIST = str(sys.argv[2]) # countries.csv (primary code/name/lat/long source)
OUTPUT = str(sys.argv[3]) # Output as .csv

# Load country data
country_data = pd.read_csv(
    COUNTRY_LIST,
    names=['country_code', 'country_name', 'avg_long', 'avg_lat', 'colour'],
    keep_default_na=False,
    skiprows=1
    )

def get_country_data(country_code):
    """
    Get all resources registered in a country, from the country code.
    """
    HEADERS = {'content-type': 'application/json'}
    PARAMS = {'resource': country_code, 'time': DATE}
    url = 'https://stat.ripe.net/data/country-resource-list/data.json'

    # Get Data
    resources = requests.get(url, headers=HEADERS, params=PARAMS).content

    return json.loads(resources)['data']['resources']['asn'], json.loads(resources)['data']['resources']['ipv4'], json.loads(resources)['data']['resources']['ipv6']

# Initialise countries
countries = {}
for index, country in enumerate(country_data['country_code'].tolist()): # Use country code only
    countries[country] = [country_data['country_name'][index], country_data['avg_long'][index], country_data['avg_lat'][index], country_data['colour'][index]]

for country in countries:
    print("Getting data for", country)
    asn, ipv4, ipv6 = get_country_data(country)
    countries[country].append(asn)

resource_data = pd.DataFrame(countries)
resource_data = resource_data.transpose()

resource_data.to_csv(OUTPUT)

