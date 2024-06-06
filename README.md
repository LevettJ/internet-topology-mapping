<a name="readme-top"></a>

<!-- PROJECT DETAILS -->
<div align="center">

  <h1 align="center">Internet Topology Mapping</h1>

  <p align="center">
    A <a href="https://systronlab.github.io"><strong>SYSTRON Lab</strong></a> project
    <br />
    from the <a href="https://www.cs.york.ac.uk/"><strong>Department of Computer Science</strong></a> at the University of York
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#dependencies-overview">Dependencies Overview</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#bgp-data-collection">BGP Data Collection</a></li>
        <li><a href="#adjacency-inferencing">Adjacency Inferencing</a></li>
        <li><a href="#registry-data">Registry Data</a></li>
        <li><a href="#topology-graph">Topology Graph</a></li>
      </ul>
    </li>
    <li><a href="#publications">Publications</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Heightened interest from nation states to perform content censorship make it evermore critical to identify the impact of censorship efforts on the Internet. We undertake a study of Internet architecture, capturing the state of Internet topology with greater completeness than existing state-of-the-art.

There are a small number of nation states that do not follow this trend, for which we provide an analysis and explanation, demonstrating a relationship between geographical factors in addition to geopolitics. In summary, our work provides a deeper understanding of how these censorship measures impact the overall functioning and dynamics of the Internet.

> This previous version of our code, which forms the foundation of our current approach, does not include the complete codebase used in our analysis, which targets specific HPC architecture. We intend to release a platform-agnostic version (which includes RIPE Atlas measurements) shortly.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Dependencies Overview

* [BGPKIT](https://github.com/bgpkit), an open-source BGP data toolkit. We use the `pybgpkit` bindings for BGPKit.
* [Requests](https://requests.readthedocs.io/en/latest/), an HTTP library for Python.
* [NetworkX](https://networkx.org/documentation/stable/reference/index.html), a network analysis library.
* [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/), a data extractor from scraped web files.
* [Pandas](https://pandas.pydata.org/docs/) and [NumPy](https://numpy.org/doc/).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

You can quickly create a copy of this project locally to perform your own analysis. Depending on the specified timeframes and the quantity of data, running from this codebase is relatively memory-intensive. In using Pandas, we have done little to optimise the memory requirements of our approach.

### BGP Data Collection

We collect BGP table data from [RIPE Routing Information Service (RIS)](https://www.ripe.net/analyse/internet-measurements/routing-information-service-ris/), [RouteViews](https://www.routeviews.org/routeviews/) and [Packet Clearing House (PCH)](https://www.pch.net/). This provides a snapshot of the routing table from a variety of geographic locations. Some data from these sources may be duplicated: either because the routes they see are the same, or because in some cases the route collectors may be situated in the same or nearby physical locations.

1. Run `bgp_collector_ris_rv.py` with a supplied timestamp (`TS_START` and `TS_END`) range to collect BGP data from the RIPE RIS and RouteViews collectors for the specified time range. In the code supplied, we use RIB tables rather than UPDATE files, which mean only the retained (router-determined locally optimal) paths. To increase the dataset, using UPDATE files to observe routes outside of those retained can give better visibility.
2. Run `bgp_collector_pch.py` with a supplied date (`YEAR`, `MONTH`, `DAY`) to collect BGP data from a given day. If observing a multi-day period, this script can be run multiple times with a different date supplied. This script uses Regex rather than a pandas converter to extract path information from the text-based files, so non-`as_path` information is ignored.

### Adjacency Inferencing

1. Run `bgp_adjacency_creator.py` with an input file listing all of the generated CSV files from (1) and (2), as well as an output destination for an `adjacencies.csv` file. This will contain a long list of non-duplicated adjacencies based on neighbours in the listed `as_path`, which enables us to observe multiple adjacencies for one AS, as well as ignoring prepending.

### Registry Data

The code supplied in this version only provides country-code and node colouring capability, and relies on a pre-provided file names `countries.csv`, which is expected to contain columns for `country_code` (ISO 2-letter), `country_name` (common name), `avg_long` (country average longitude), `avg_lat` (country average latitude), and `colour`.

With this data, we can then query RIPEstat for registered ASN resources:

1. Run `ripe_stat.py` providing the lookup date, `countries.csv` file and an output destination for `resource_data.csv`.

### Topology Graph

With the collected data, this script creates a GRAPHML and GEXF format graph for analysis in a tool like [Gephi](https://gephi.org/).

1. Run `bgp_topology_graph.py` with the `adjacencies.csv`, end timestamp (this allows for time-based analysis in Gephi), `resource_data.csv`, an output GEXF location and output GRAPHML location.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- PUBLICATIONS -->
## Publications

- [(Preprint) Unveiling Internet Censorship: Analysing the Impact of Nation States’ Content Control Efforts on Internet Architecture and Routing Patterns](https://systronlab.github.io/publications/2024-unveiling-internet-censorship)
- [(Abstract) From Internet to Emulator: A Virtual Testbed for Internet Routing Protocols](https://systronlab.github.io/publications/2024-from-internet-to-emulator)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

**Josh Levett**: [@Levett_Josh](https://twitter.com/Levett_Josh) / joshua.levett (at) york.ac.uk


<p align="right">(<a href="#readme-top">back to top</a>)</p>