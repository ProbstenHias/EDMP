# Enterprise Data Marketplace

The Enterprise Data Marketplace is a platform for data providers to publish their data and for data consumers to discover and access data. The platform is built on top of Amundsen, an open source data catalog.
It uses Apache Airflow to register data assets to Amundsen and updates the metadata on a daily basis.
To visualize the data assets, Amundsen uses Superset, an open source data visualization tool.
The special feature of our platform is that it is designed for any data consumer that does not waste time on converting data formats. Instead of downloading the data, the consumer can choose in which tool they want to use the data and the platform will convert the data to the desired format and provisions the data for immediate use.

## Getting Started

## Pages

| Link Description | URL |
| --- | --- |
| Register you data | localhost:5002 |
| Visualize you data | localhost:8088 |
| Discover you data | localhost:5000 |