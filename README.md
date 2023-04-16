# Enterprise Data Marketplace

The Enterprise Data Marketplace is a platform for data providers to publish their data and for data consumers to discover and access data. The platform is built on top of Amundsen, an open source data catalog.
It uses Apache Airflow to register data assets to Amundsen and updates the metadata on a daily basis.
To visualize the data assets, Amundsen uses Superset, an open source data visualization tool.
The special feature of our platform is that it is designed for any data consumer that does not waste time on converting data formats. Instead of downloading the data, the consumer can choose in which tool they want to use the data and the platform will convert the data to the desired format and provisions the data for immediate use.

## Getting Started

### Setup

1. Clone the repository
```bash
git clone --recursive <link-to-repo>
```
2. Install Docker and Docker Compose
3. Create the .env files in the root directory of the repository. Here are some example .env files:

    * In ./transformer/.env

    ```bash
    ADMIN_PG_USER=postgres
    ADMIN_PG_PASSWORD=postgres
    ADMIN_PG_HOST=172.17.0.1
    ADMIN_PG_PORT=5432
    ADMIN_MYSQL_USER=root
    ADMIN_MYSQL_PASSWORD=root
    ADMIN_MYSQL_HOST=172.17.0.1
    ADMIN_MYSQL_PORT=3306
    ADMIN_MONGO_USER=root
    ADMIN_MONGO_PASSWORD=root
    ADMIN_MONGO_HOST=172.17.0.1
    ADMIN_MONGO_PORT=27017
    SENDER_MAIL_ADRESS=test@mail.com
    SENDER_MAIL_PASSWORD=emailpassword
    SENDER_MAIL_HOST=smtp.mail.com
    SENDER_MAIL_PORT=587
    SUPERSET_PORT=8088
    SUPERSET_USER=admin
    SUPERSET_PASSWORD=admin
    SUPERSET_URL=http://172.17.0.1:8088
    ```

    * In ./registration_services/.env

    ```bash
    MYSQL_USER = 'root'
    MYSQL_PW = 'root'
    MYSQL_ROOT_PW = 'root'
    MONGODB_USER = 'root'
    MONGODB_PW = 'root'
    ```

    * In ./registration-backend/.env

    ```bash
    SUP_BASE_URL=http://172.17.0.1:8088/api/v1
    SUP_USERNAME=admin
    SUP_PASSWORD=admin
    ```


### Installation

The full platform needs more than 32GB of RAM. To try out the platform we reccomand to start only the services you want to try out.
To run the start the different services with the folloing commands:

#### Amundsen

```bash
cd amundsen
docker-compose -f docker-amundsen-local.yml up
```

#### Airflow

```bash
cd airflow
docker-compose up
```

#### Superset

```bash
cd superset
docker-compose -f docker-compose-non-dev.yml up
```

#### Registration service

```bash
docker-compose -f docker-registration.yml up
```

#### Data bying service

```bash
docker-compose -f docker-buying.yml up
```

#### Sample data to sell

```bash
    cd postgres-chinook
    docker-compose up
```

#### Sample provisioning tools

```bash
    cd transformation_services
    docker-compose up
```

To test registration start Superset, Airflow, Amundsen and the registration service (Sample data to sell). Then go to localhost:5005 and register the sample data.

To test data buying start Superset, Amundsen and the data buying service (Sample data to sell, Sample provisioning tools). Then go to localhost:5000 and discover the sample data. After that you can buy the data and use it in Superset.

### Pages

| Link Description | URL |
| --- | --- |
| Register you data | localhost:5005 |
| Visualize you data | localhost:8088 |
| Discover you data | localhost:5000 |
| Airflow | localhost:8080 |
