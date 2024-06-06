"""
PCH Daily Data Collector

1) Source daily feed data from PCH
2) Obtain data and extract meaningful paths
3) Export paths in CSV format equivalent to other extracted sources
"""

# Import libraries
import gzip
import re
import io
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Input Vars
YEAR = str(sys.argv[1]) # YYYY
MONTH = str(sys.argv[2]) # MM
DAY = str(sys.argv[3]) # DD

print("Collecting data for", YEAR, MONTH, DAY)

class PCHdaily():
    """
    PCHdaily: Get PCH Daily routing overview files.
    """
    def __init__(self):
        pass

    @staticmethod
    def get_router_index_by_ver(IPver, year, month):
        """
        Get Router Index (by IP version)
        Collect a list of routers with available data on the specified month/year combination.
        Return a list of routers.
        """
        index_url = "https://www.pch.net/resources/Routing_Data/" + IPver + "_daily_snapshots/" + year + "/" + month + "/"
        
        # Get router index page
        index = requests.get(index_url)
        page = BeautifulSoup(index.text, 'html.parser')

        # Get a list of available routers, and format data into list
        router_list = page.find_all(attrs={"data-sort-value": True})
        routers = []
        for router in router_list:
            try:
                data = router.a.strong.string
                if data != None:
                    routers.append(data)
            except:
                pass

        # Return router names as array
        return routers

    @staticmethod
    def get_router_index(year, month):
        """
        Get Router Index (both IPv4 and IPv6)
        """
        ipv4 = PCHdaily.get_router_index_by_ver("IPv4", year, month)
        ipv6 = PCHdaily.get_router_index_by_ver("IPv6", year, month)
        return ipv4, ipv6

    @staticmethod
    def get_router_dump_url(IPver, router, year, month, day):
        # routecollector-IPVER_bgp_routes.YYYY.MM.DD.gz
        file_url = "https://www.pch.net/resources/Routing_Data/" + IPver + "_daily_snapshots/" + year + "/" + month + "/" + router + "/" + router + "-" + IPver.lower() + "_bgp_routes." + year + "." + month + "." + day + ".gz"
        
        return file_url

    @staticmethod
    def get_router_urls(IPver, routers, year, month, day):
        urls = []
        for router in routers:
            urls.append(PCHdaily.get_router_dump_url(IPver, router, year, month, day))
        return urls

def extract_path(data):
    paths = re.findall("\s[0-9]+\s+[0-9]+\s([0-9\s]*)\si", data)
    return paths

def get_daily_path_data(url):
    print("Requesting", url)
    req = requests.get(url) # Get file from URL

    if req.status_code == 200:
        fileasgz = req.content  # Get file to store
        fileinmem = io.BytesIO(fileasgz) # Store file in memory

        with gzip.GzipFile(fileobj = fileinmem) as f: # Decompress
            data = f.read().decode('UTF-8') # Convert raw bytes

        return extract_path(data) # Extract relevant data
    
    else:
        return []

print("Getting router index...")
ipv4, ipv6 = PCHdaily.get_router_index(YEAR, MONTH)

print("Getting IPv4 and IPv6 archive urls")
ipv4_router_urls = PCHdaily.get_router_urls("IPv4", ipv4, YEAR, MONTH, DAY)
ipv6_router_urls = PCHdaily.get_router_urls("IPv6", ipv6, YEAR, MONTH, DAY)
router_urls = ipv4_router_urls + ipv6_router_urls

print("Starting download and extraction loop")
# Loop and store
paths = []
for router in router_urls:
    paths += get_daily_path_data(router)

print("Creating dataframe for export")
export = pd.DataFrame(paths, columns=['as_path'])
filename = YEAR + "-" + MONTH + "-" + DAY + "-pch-daily.csv"

print("Exporting data as CSV")
export.to_csv(filename)

print("Completed")
