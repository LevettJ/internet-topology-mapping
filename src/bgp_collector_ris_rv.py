"""
BGP Collector and Parser

1) Source BGP feeds from RIPE RIS via the BGPKIT Broker
2) Supplement discovered collectors with PCH feeds for the same time period
3) Parse discovered files in to .csv format
"""

# IMPORTS
import bgpkit
import pandas as pd
import sys

# Input Timestamps
TS_START = str(sys.argv[1]) # TS_START, e.g. "2023-06-01T00:00:00"
TS_END = str(sys.argv[2]) # TS_END, e.g. "2023-06-10T23:59:59"

# GET DATA FROM BROKERS
broker = bgpkit.Broker()

collectors = broker.query(ts_start=TS_START, ts_end=TS_END, data_type="rib")

# GET DATA FROM EACH COLLECTOR
for collector in collectors:
    try:
        print("Getting data from", collector.collector_id, "starting at", collector.ts_start, "of datatype", collector.data_type)

        # Create dataframe
        records = pd.DataFrame()

        # Retrieve data
        data = bgpkit.Parser(url=collector.url).parse_all()
        records = pd.concat([records, pd.DataFrame(data)], ignore_index=True)

        # Convert to datetime
        records['timestamp'] = pd.to_datetime(records['timestamp'],unit='s').sort_values()

        records.reset_index()

        # Filename format: 2023-04-30T23:45:00_update_route-views4.csv
        filename = str(collector.ts_start) + "_" + str(collector.data_type) + "_" + str(collector.collector_id) + ".csv"
        records.to_csv(filename)
        del records

    except Exception as ex:
        print("Failed:", str(ex), "from", collector.collector_id)

