---
title: "Build a back-end with PostgreSQL, FastAPI, and Docker"
url: https://medium.com/p/7ebfe59e4f06
---

# Build a back-end with PostgreSQL, FastAPI, and Docker

[Original](https://medium.com/p/7ebfe59e4f06)

# Build a back-end with PostgreSQL, FastAPI, and Docker

## A step-by-step guide to develop a map-based application (Part IV)

[![Jacky Kaub](https://miro.medium.com/v2/resize:fill:64:64/1*U3twwZ2ADIoy7ciShy7fmA.jpeg)](/@jacky.kaub?source=post_page---byline--7ebfe59e4f06---------------------------------------)

[Jacky Kaub](/@jacky.kaub?source=post_page---byline--7ebfe59e4f06---------------------------------------)

28 min read

·

Mar 14, 2023

--

4

Listen

Share

More

Press enter or click to view image in full size

![]()

Maps are a powerful tool for visualizing and understanding geographic data but they need specific skills to be designed efficiently.

In this step-by-step guide, we are going to take a deep dive into building a map-based application to show the customers prices of gas stations around them. We will cover the different key steps of a product, from original proof of concept (POC) to the minimum viable product (MVP)

## Articles in the series:

[Part I: The proof-of-concept — Build a minimalist demo](https://towardsdatascience.com/a-step-by-step-guide-to-develop-a-map-based-application-part-i-757766b04f77)

[Part II: How to use React to build web apps (Static Layout)](https://towardsdatascience.com/a-step-by-step-guide-to-develop-a-map-based-application-part-ii-6d3fa7dbd8b9)

[Part III: Add interactivity to your web apps with React](https://towardsdatascience.com/a-step-by-step-guide-to-develop-a-map-based-application-part-iii-ad501c4aa35b)

Part IV: Build a back-end with PostgreSQL, FastAPI, and Docker

### A bit of context around this article

In the previous articles in this series, we built the front end of the gas station finder using **React**, and we considered the back end as a “black box” that was only providing the relevant data.

In this part, we are going to detail step by step how to build the back end using powerful tools such as **PostgreSQL** or **FastAPI**.

You can find the full code of this project in my [Github page](https://github.com/jkaub/station-prices-app-full).

### Why do we need a clean back end?

In the first part of this series, we created some utility functions to obtain data on-the-fly from fuel stations directly from the public provider. While this was sufficient for our proof of concept, we now need a more robust system for several reasons:

* Performances & Latency: Processing the data in real-time, including parsing the XML, formatting, and filtering, is computationally expensive and would be impractical for an application that expects frequent use.
* Reliability: To ensure that our application is not impacted by unexpected changes or downtime of third-party data sources. Relying solely on data from external portals would put our application at risk, as even a simple change to a field name by the provider could generate bugs and downtime on our side while we patch the change. By building our own database, we have greater control over the data, and we can perform necessary updates and maintenance without relying on external parties.
* Customization: With our own database, we can customize the data to meet our technical specs, add other external data sources, build custom views of the data for different use cases, etc…

To address these requirements, we will build our own database and API that can handle data acquisition, processing, and delivery to the front end. This will involve running a PostgreSQL database with **Docker**, using P**ython** and s**qlalchemy** to interact with the database, and making geo-queries using the **PostGIS** extension. We will also explore how to build a simple API using **FastAPI** and **SQLmodel**.

The chart below is a simple schema of the different components of the app:

Press enter or click to view image in full size

![]()

### What this article covers

In this article, we focus on our internal database and the creation of the API. In particular, we will:

* Run a PostgreSQL database using Docker
* Use python and sqlalchemy to interact with the database
* Make geo-queries with PostGIS extension
* Build a simple API using FastAPI and SQLmodel
* Containerizing our Project and running it with **docker-compose**

## Create a local PostgreSQL instance with Docker

Docker is an open-source containerization platform that allows you to run applications in a consistent and isolated environment. Setting up a PostgreSQL server with Docker has several advantages, including being able to install the application in a standardized way without risking conflicts with other configurations on your system.

In our case, we will set up our Postgre server directly inside a container.

I’ll assume here you already have Docker installed on your computer, as the installation method differs from system to system.

### Get the container image

A docker image can be seen as the specification of everything that is needed to build a container dedicated to a particular task. It does nothing on its own, but it is used to build the containers (a dedicated virtual environment) where your application will live. We can create our own custom images using a Dockerfile (we will cover this later) or we can download pre-made images from a wide range of open-source images shared by the community.

In our case, we want an image that will help us to create a container with PostgreSQL running in it, and we can use the [official image](https://hub.docker.com/_/postgres) for that purpose.

We start by downloading the PostgreSQL image on docker. This is done in the Shell:

```
docker pull postgres
```

### Run the Postgre container

Once the image is downloaded in Docker, we can build the container based on it with the following command:

```
docker run -itd -e POSTGRES_USER=jkaub -e POSTGRES_PASSWORD=jkaub -p 5432:5432 -v ~/db:/var/lib/postgresql/data --name station-db postgres
```

Let’s decrypt it.

-itd is a combination of 3 parameters:

* -d means we run the container in detached mode. In this mode, the container will run in the background and we can continue to use our terminal for other stuff.
* -i specifies that our container will run in interactive mode. It will allow us to go inside the container and interact with it
* -t means a pseudo-terminal will be available inside of the container to interact with it, which will bring a more seamless and intuitive interaction with the container

-e generate environmental variables inside the container. In this case, the environmental variables POSTGRES\_USER and POSTGRES\_PASSWORD are also used to generate a new user of our PostgreSQL instance with the given password. Without this, we could still access the PostgreSQL instance with the default user/password (postgre/postgre)

-p is used to map a port from the local machine to the docker container. The default port used for PostgreSQL is 5432. If it was already used in your local machine, you could use this parameter to map the 5432 from the container to another port of your machine.

-v is a very important parameter in our case: it allows us to map a volume from our machine (in our case the folder `~/db` ) to the volume inside of the container where the SQL data are stored by default (`/var/lib/postgresql/data` ). By doing this mapping, we create a persistent volume that will remain even after the container is stopped. Thus, our database will persist even when we stop using the container, and will be available for later uses.

— name is just a flag to name the container, which will be useful to access it later on

We can check that the container is active by using the below command which will display the list of running containers on our machine:

```
docker ps
```

Returning:

```
CONTAINER ID   IMAGE           COMMAND                  CREATED         STATUS        PORTS                    NAMES  
cb0840806636   postgres        "docker-entrypoint.s…"   2 minutes ago   Up 2minutes   0.0.0.0:5432->5432/tcp   station-db
```

## First interactions with PostgreSQL

Our PostgreSQL instance is now running inside our container, we can now interact with it.

### Create the Database

As a starting point, let’s create a first database that will contain the different tables of our project.

To do so, we need to enter our container. Remember that this is possible as we specified the -it parameters when initializing the container. The below command line will do the job:

```
docker exec -it station-db bash
```

The command prompt now should be:

```
root@cb0840806636:/#
```

meaning we are logged with the root user in the container. We can connect to PostgreSQL using the user (-U)/password (-d) as follow:

```
psql -U jkaub -d jkaub
```

Once in the PostgreSQL instance, we can interact with it using SQL queries, and in particular, create a new database to host our future tables.

```
CREATE DATABASE stations;
```

We can verify that the database has been created by running

```
\l
```

which will show the different databases in the system. Among some default databases created at the initialization of the instance, we can find the one we just created:

```
jkaub=# \l  
                                             List of databases  
   Name    | Owner | Encoding |  Collate   |   Ctype    | ICU Locale | Locale Provider | Access privileges   
-----------+-------+----------+------------+------------+------------+-----------------+-------------------  
 stations  | jkaub | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            |
```

Now that we have set up our PostgreSQL instance, we could interact with our database by manually writing SQL queries in **psql** to create tables and import data from .csv files. While this approach is suitable for one-time use, it can become cumbersome and error-prone in the long run if we need to frequently update our tables.

Therefore, to facilitate automation, we will use a Python framework to interact with the database and its tables. This will allow us to easily create, update, and query our database using code, making the process more efficient and less error-prone.

### Open a session with sqlalchemy

SQLalchemy is an open-source SQL toolkit and Object Relational Mapper (ORM) for Python developers. It proposes a set of high-level functions to interact with databases rather than writing SQL queries.

It is particularly convenient as it will allow us to define the structure of our tables using Python classes (also named “models” here) and work with object-oriented paradigms. Our python ORM, **sqlalchemy** will be particularly useful in the next part when we build the backend API.

Let’s start by installing the libraries needed for the project. On top of sqlalchemy, we will also use **psycopg2** which is a PostgreSQL adapter for python and can be used as a connector by sqlalchemy.

```
pip install psycopg2 sqlalchemy
```

We can now effectively create a session to our database directly in Python:

```
from sqlalchemy import create_engine  
  
engine = create_engine('postgresql://jkaub:jkaub@localhost/stations')  
  
# test the connection by executing a simple query  
with engine.connect() as conn:  
    result = conn.execute('SELECT 1')  
    print(result.fetchone())
```

Explaining step by step this script:

```
engine = create_engine('postgresql://jkaub:jkaub@localhost/stations')
```

The create\_engine method is used to hold the connection to the database. We need to specify here a database URL that includes all the information required to connect to our database.

* The first part of that URL postgresql**://** is there to specify that we are using a PostgreSQL connection and that what will follow will be the specs of a connection for that type of database. If you are using a different database such as SQLite, you will have a different base and different specs.
* jkaub:jkaubis the login information to connect to our database.
* localhostis the server on which we run the database. A server IP could also be used to connect to remote servers, or, as we will see later in the case of a cluster of containers, we could also use a container name in certain cases.
* /stations is used to specify the database we want to connect to. In our case, we connect to the one we just created, “stations”.

```
# test the connection by executing a simple query  
with engine.connect() as conn:  
    result = conn.execute('SELECT 1')  
    print(result.fetchone())
```

This part of the code is just used for now to test that the connection worked well. Our database has no table to query yet, so we are just running a dummy query. It should return (1,), which means the connexion succeeded.

## Building the API with FastAPI

Now that we have set up our PostgreSQL database in a Docker container and accessed it using the SQLAlchemy engine, it’s time to develop the API for interacting with the database.

There are several benefits of using an API here:

* It offers reusability and platform/language agnosticism, allowing multiple services to use the same API endpoint.
* It separates the database logic from the application logic, making it easier to modify one without affecting the other as long as the inputs/outputs are respected.
* It adds a layer of security as you can control who has access to the database with an authorization system.
* Finally, an API is scalable and can run on multiple servers, making it flexible for managing the workload. By creating a well-defined set of URLs, we will be able to retrieve, modify, insert, or delete data from our database via the API.

### About FastAPI

[FastAPI](https://fastapi.tiangolo.com/) is a modern python framework particularly efficient in building lightweight API developed by [Sebastián Ramírez](https://github.com/tiangolo).

It is particularly efficient when combined with **sqlalchemy** and [**pydantic**](https://docs.pydantic.dev/), a python library used for data validation (for example it can control that a date is actually a date, that a number is a number, etc…). Used together, it allows us to handle and query effectively tables directly via the framework.

Even better, [Sebastián Ramírez](https://github.com/tiangolo) designed also another library, [**sqlmodel**](https://sqlmodel.tiangolo.com/) that combines both pydantic and sqlalchemy to remove some of the redundancies and simplify even more the architecture of the APIs.

If you have yet to become familiar with FastAPI, I recommend you to have a look at [this tutorial](https://fastapi.tiangolo.com/tutorial/) first, which is really well done.

Before starting the project, we will need to install multiple libraries.

```
pip install uvicorn  
pip install fastapi  
pip install sqlmodel  
pip install geoalchemy2
```

* **uvicorn** is the tool that will run the API server and is well-suited to work in tandem with FastAPI
* **fastapi** is the core engine of the API, that we will use to create the different endpoints
* **sqlmodel** combines the sqlalchemy ORM with the power of type verification of pydantic
* **geolochemy2** is an extension of sqlalchemy used to perform geoqueries

### Initialize the models

Let’s create a new repository for our API Project, starting with the definition of our models with **sqlmodel**. A “model” is nothing more than a python class that represents a table in SQL.

```
api/  
  |-- app/  
    |-- __init__.py  
    |-- models.py
```

Our project will have 3 tables and will follow the initial design we built in [part I](https://towardsdatascience.com/a-step-by-step-guide-to-develop-a-map-based-application-part-i-757766b04f77).

* One table containing the information related to cities (postal codes, locations)
* One table containing information about the gas prices
* One table containing information about the stations

Combining those tables with joins and geofilters will help us build the final output requested by the front-end side.

Let’s have a look at the first table, the Cities table:

```
from sqlmodel import Field, SQLModel  
from datetime import datetime  
from typing import Optional  
  
class Cities(SQLModel, table=True):  
    id: Optional[int] = Field(default=None, primary_key=True)  
    postal_code: str  
    name: str  
    lat: float  
    lon: float
```

The class “Cities” inherit from the class SQLModel, combining both sqlalchemy**’s** ORM features and pydantic’s typing control.

The parameter table=True indicates to automatically create the corresponding table if it does not exist yet in the database, matching columns names and columns typing.

Each attribute of the class will define each column with its type. In particular, “id” will be our primary key. Using Optional will indicate sqlalchemy to automatically generate ids by incrementation if we don’t provide one.

We also provide the models for the two other tables:

```
from datetime import datetime  
  
...  
  
class GasPrices(SQLModel, table=True):  
    id: Optional[int] = Field(default=None, primary_key=True)  
    station_id: str  
    oil_id: str  
    nom: str  
    valeur: float  
    maj: datetime = Field(default_factory=datetime.utcnow)  
  
  
class Stations(SQLModel, table=True):  
    station_id: str = Field(primary_key=True)  
    latitude: float  
    longitude: float  
    cp: str  
    city: str  
    adress: str
```

Note that in the case of the table Stations, we are using station\_id as the primary key, and unlike GasPrices, the field will be mandatory. If the field is empty when sent to the table, it will generate an error message.

### Initialize the engine

In another dedicated file to keep the project structured, we are going to initiate the engine. We call that file services.py.

```
api/  
  |-- app/  
    |-- __init__.py  
    |-- models.py  
    |-- services.py
```

The connection to the DB is done in the same way as the one presented before.

```
from sqlmodel import SQLModel, create_engine  
import models  
  
DATABASE_URL = 'postgresql://jkaub:jkaub@localhost/stations'  
  
engine = create_engine(DATABASE_URL)  
  
def create_db_and_tables():  
    SQLModel.metadata.create_all(engine)
```

Note the function create\_db\_and\_tables(): this function will be called during the initialization of the API, will look-up the models defined in models.py, and will create them directly inside the SQL database if they don’t already exist.

### Hands-on the API

We can now start the development of the main component in which we are going to put the endpoints (= the URL that will allow us to interact with the database).

```
api/  
  |-- app/  
    |-- __init__.py  
    |-- main.py  
    |-- models.py  
    |-- services.py
```

The first thing we want to do is configure FastAPI when it starts up and deal with API authorizations.

```
from fastapi.middleware.cors import CORSMiddleware  
from fastapi import FastAPI, HTTPException  
from models import Cities, Stations, GasPrices  
from services import engine, create_db_and_tables  
  
#We create an instance of FastAPI  
app = FastAPI()  
  
#We define authorizations for middleware components  
app.add_middleware(  
    CORSMiddleware,  
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)  
  
#We use a callback to trigger the creation of the table if they don't exist yet  
#When the API is starting  
@app.on_event("startup")  
def on_startup():  
    create_db_and_tables()
```

An important point to note: by default, our front does not have the access to make API calls, and if you forget to configure the middleware part, you will expose yourself to errors on the front-end side. You could decide to allow all origins by using:

```
allow_origins=["*"],
```

but this is not something I recommend for safety reasons, as you would basically open your API to the world once it is online. Our front end is currently running locally at localhost:3000, so this is the domain we will allow.

At that point, we can already launch the API, by using the following command line:

```
uvicorn main:app --reload
```

The — reload simply means that each time we will save a modification in the API while it is running, it will reload to include those changes.

Once started, you can see some logs displayed in the shell, in particular:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

indicates that the API server is running on localhost (equivalent to the IP 127.0.0.1), port 8000.

As explained earlier, starting the API will also trigger the creation of empty tables in the DB (if they don’t already exist). So from the moment you have initiated your API for the first time, the models you create with table=True will have a dedicated table in the database.

We can check this easily from within the PostgresSQL container in psql. Once connected as the main user, we first connect to the database station:

```
\c stations
```

We can now check that our tables have been well created:

```
\dt
```

Which will return:

```
            List of relations  
 Schema |      Name       | Type  | Owner   
--------+-----------------+-------+-------  
 public | cities          | table | jkaub  
 public | gasprices       | table | jkaub  
 public | stations        | table | jkaub
```

We can also verify that the columns match our models by running a description query in psql, for example, for cities:

```
\d cities
```

```
   Column    |       Type        | Collation | Nullable |              Default    
               
-------------+-------------------+-----------+----------+-----------------------  
-------------  
 id          | integer           |           | not null | nextval('cities_id_seq  
'::regclass)  
 postal_code | character varying |           | not null |   
 name        | character varying |           | not null |   
 lat         | double precision  |           | not null |   
 lon         | double precision  |           | not null |   
Indexes:  
    "cities_pkey" PRIMARY KEY, btree (id)
```

### Building our first request — Adding rows to Cities with a POST request

The Cities table will be filled only one time and is used to match postal codes with lat/lon of cities, which will be particularly helpful later to query around those locations using a postal code.

As of now, the data are stored in a .csv and we want to design a POST call that will be used to update the table adding one row at a time if it is not yet in the database. The API calls are put inside the main.py file.

```
from sqlmodel import Session  
  
...  
  
@app.post("/add-city/")  
def add_city(city: Cities):  
    with Session(engine) as session:  
        session.add(city)  
        session.commit()  
        session.refresh(city)  
        return city
```

Let’s have a look at this piece of code line by line:

```
@app.post("/add-city/")
```

Each API endpoint is defined using a decorator. We are defining here two things: the type of request (get, post, put, delete…) and the URL endpoint associated (/add-city/).

In this particular case, we will be able to do a POST request at http://127.0.0.1:8000/add-city/

```
def add_city(city: Cities):
```

We pass in the function the different parameters to be used in the query. In our case, the post request will look for an instance of Cities, which will be passed via a JSON in our request. This JSON will contain the values for each column of the Cities Table for the new row we want to add.

```
with Session(engine) as session:
```

To connect to the database we open a Session. Each query needs its own session. Using this methodology will be particularly useful in case something unexpected happens inside the session: all changes made between the initialization of the session and the commit() will be rolled back in case of a problem.

```
  session.add(city)  
  session.commit()  
  session.refresh(city)
```

Here, the object is added to the database and then commit. From the moment it is committed the operations cannot be rolled back. The refresh is used to update the “city” object with any modification operated by the DB. In our case, for example, an incremental “id” is automatically added.

```
return city
```

We conclude the request by sending the object city in the form of a JSON.

We can now try the request in python (this need to be done with the API running, of course):

```
import requests  
  
url='http://127.0.0.1:8000/add-city/'  
  
json = {  
    'postal_code': '01400',  
    'name':"L'Abergement-Clémenciat",  
    'lat':46.1517,  
    'lon':4.9306  
}  
  
req = requests.post(url, json=json)
```

Note that the keys of the JSON we are sending in the request match the name of the columns of the table we want to update. The parameter “id” is optional, it will be automatically added to the operation and we don’t need to bother about it.

This should trigger in the API shell the following line:

```
INFO:     127.0.0.1:33960 - "POST /add-gas-price/ HTTP/1.1" 200 OK
```

Meaning the request was successful. We can then verify that the line has been well-added. Going back to psql in our docker, we can try the following query:

```
SELECT * FROM cities LIMIT 1;
```

which will display:

```
 id | postal_code |          name           |   lat   |  lon     
----+-------------+-------------------------+---------+--------  
  1 | 01400       | L'Abergement-Clémenciat | 46.1517 | 4.9306
```

demonstrating that the row has been effectively added by the API in our DB.

On top of that, we don’t want a postal code to be added twice. To do so, we are going to query the Cities table, filter the table based on the postal code we are trying to send, and return an HTML error in case we find a row with that postal code, which will result in avoiding postal\_code duplicates.

```
from fastapi import FastAPI, HTTPException  
  
...  
  
@app.post("/add-city/")  
async def add_city(city: Cities):  
    with Session(engine) as session:  
  
        #New code block  
        exist = session.query(Cities).filter(  
            Cities.postal_code == city.postal_code).first()  
        if exist:  
            raise HTTPException(  
                status_code=400, detail="Postal code already exists")  
        #New code block  
  
        session.add(city)  
        session.commit()  
        session.refresh(city)  
        return city
```

In this new block of code we are performing our first database query using sqlalchemy ORM: instead of writing classical SQL (“SELECT FROM”) we are using a set of functions to query directly our database.

```
exist = session.query(Cities).filter(  
            Cities.postal_code == city.postal_code).first()
```

* .query is equivalent to SELECT … FROM …, in our case, we select everything from the table cities
* .filter is equivalent to the WHERE statement. In particular, we want to match entries that are equal to the postal code of the object we are sending (represented by the variable city)
* .first() is self-explanatory and is equivalent to LIMIT 1.
* if no row is found, exist will be None and the exception will not be raised, so we will add the object to the database. If a row matches with the postal code, the API request will return an error with status\_code 400 and the post request will be interrupted without the element being added.

If we try now to send the exact same request as before, we will see the API returning an error message:

```
INFO:     127.0.0.1:49076 - "POST /add-city/ HTTP/1.1" 400 Bad Request
```

And the row has not been added to the table.

From that point, we can simply loop through our .csv and add all the cities one by one to populate the table cities.

### Adding rows to the Gasprices and Stations tables with a POST request

We will pass very quickly on the construction of these API calls as they are very similar to the previous one.

```
@app.post("/add-station/")  
async def add_station(station: Stations):  
    with Session(engine) as session:  
        exist = session.query(Stations).filter(  
            Stations.station_id == station.station_id).first()  
        if exist:  
            raise HTTPException(  
                status_code=400, detail="Station already exists")  
  
       
        session.add(station)  
        session.commit()  
        session.refresh(station)  
  
        return station  
  
@app.post("/add-gas-price/")  
async def add_station(gasPrice: GasPrices):  
    with Session(engine) as session:  
        exist = session.query(GasPrices). \  
            filter(GasPrices.oil_id == gasPrice.oil_id). \  
            filter(GasPrices.maj == gasPrice.maj). \  
            first()  
        if exist:  
            raise HTTPException(  
                status_code=400, detail="Entry already exists")  
  
        session.add(gasPrice)  
        session.commit()  
        session.refresh(gasPrice)  
        return gasPrice
```

The only interesting thing to notice here is that we are using a double filter query to make sure that we add a row only if there was a new update for the oil\_id. This way, we ensure that future updates will not create duplicates if a price has not moved from one day to another, saving some space in the DB.

To retrieve the gas prices and ingest them, we are simply recycling our parsing code from [Part I](https://towardsdatascience.com/a-step-by-step-guide-to-develop-a-map-based-application-part-i-757766b04f77), get the corresponding dataset and loop through it making a POST call for each entry.

The script below is executed outside of the API scope to upload data to the DB:

```
import request  
from data_parsing import get_data  
  
BASE_API_URL = 'http://127.0.0.1:8000'  
  
#get_data is the function designed in part I to pull the xml from the opendata  
#source and convert them in Dataframes  
stations, gas = get_data()  
  
#Pushing stations data  
to_push = stations[['latitude','longitude','cp','adress','city','station_id']].to_dict('records')  
  
url=f'{BASE_API_URL}/add-station/'  
for elmt in to_push:  
    req = requests.post(url, json=elmt)  
  
#Pushing gasprices data  
to_push = gas.to_dict('records')  
  
url=f'{BASE_API_URL}/add-gas-price/'  
for elmt in to_push:  
    req = requests.post(url, json=elmt)
```

*Note: I chose here for simplicity to push the data row by row. We could have also designed the endpoint to push the data by batches and send a list of JSON.*

## Building the GET query used in the front-end

At this point, our database is fully filled and the script above could be eventually used to update it with more recent data, and we can start building the GET request used in the front end to query the prices of a specific fuel for the stations around a particular city.

I decided to dedicate a full section to this particular query, due to its complexity (we are going to use all the tables defined so far, make joins and geofilters) but also because we need to operate some changes at this point to integrate spatial features to our database, installing add-ons and modifying some models. While this could have been done directly from the start, it is common in real projects to operate modifications and I think it is interesting to show you how we can do it here smoothly.

### Installing PostGIS

PostGIS is an extension to PostgreSQL that will allow us to build geo-queries, which implies a spatial component. For example in our case, we would be able to select all rows from stations in a 30km radius from a point of interest.

Now we don’t want to install directly PostGIS in our running container, because this installation will be “lost” every time we need to pop a new container, which is based on an image in which only PostgreSQL is installed.

Instead, we are going to simply change the image we are using to build the container and replace it with one containing both PostgreSQL and PostGIS. We will provide the same persistent storage where our DB is currently located, so the new container will also have access to it.

To build the container with the PostGIS extension, we first pull the latest PostGIS image from docker, then we kill and remove the current PostgreSQL container, and build the new one with the new image.

```
docker pull postgis  
docker kill stations  
docker rm stations  
docker run -itd -e POSTGRES_USER=jkaub -e POSTGRES_PASSWORD=jkaub -p 5432:5432 -v ~/db:/var/lib/postgresql/data --name station-db postgis/postgis:latest
```

We can then access the container as we were doing previously, but we are now using a version of PostgreSQL including PostGIS.

We now need to add the extension to our existing database. We first reconnect to the DB:

```
docker exec -it station-db bash
```

```
psql -U jkaub -d jkaub
```

```
\c stations
```

Then we include in it the PostGIS extension:

```
CREATE EXTENSION postgis;
```

### Modifying our Stations model

Now that we have PostGIS up and running in our database, we need to modify our Stations table to be able to perform a geo-query. More precisely, we need to add a “geometry” field that is understood and converted to an actual location on Earth.

There are multiple ways of building maps or indicating a location on Earth, each way with its own projections and referenced coordinate system. To make sure one system can speak to another, we need to make sure they speak the same language which can include making conversion of units (the same way we could convert meters to feet, or kilograms to pounds).

For coordinates, we are using something called a “Geodetic Parameter Dataset” (EPSG). Latitudes and Longitudes (EPSG 4326) are expressed as angles and it is not possible to directly convert this to distances (Euclidean Geometry, including distance calculation, cannot be applied on the surface of a sphere directly as it is, because, by nature, this is not a euclidean surface..). Instead, they need to be projected to a plan representation, which is handled nicely in PostGIS as long as we are aware of it and apply the appropriate conversions.

As a starting point, we need to add a new field in our Stations database which can be interpreted as a “geometrical” coordinate. From within our database:

```
ALTER TABLE stations ADD COLUMN geom geometry(Point, 4326);
```

This line will modify our stations' table with a new field “geom” which is a PostGIS geomtry of type “point”, expressed using EPSG 4326 (the EPSG of latitude/longitude system). The field is for now empty for all the rows, but we can fill it very easily still in SQL to update the current table (which is not empty at this point).

```
UPDATE stations SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326);
```

The above SQL query will SET the geom column for each row of the Stations table with a Point made from the longitudes/latitudes. Note that we are using here two PostGIS functions, ST\_MakePoint and ST\_SetSRID to help us define the geometry in SQL.

We can check how this new geometry is stored in the DB

```
SELECT * FROM stations LIMIT 1;
```

```
 station_id | latitude | longitude |  cp   | city  |        adress         |                              geom                          
------------+----------+-----------+-------+-------+-----------------------+----------------------------------------------------  
 26110004   |    44.36 |     5.127 | 26110 | NYONS | 31 Avenue de Venterol | 0101000020E6100000355EBA490C821440AE47E17A142E4640
```

You can see here that the geometry is encoded in a string which is the Well-Known Binary (WKB) format, which is efficient to store geometries. I’ll not expand on this, but don’t be surprised if you see this in your datasets, you might need to decode this to a more readable format if needed.

Now, we also need to also update the Stations class in our model.py file to include this new field, and for this, we are using the type “Geometry” from **geoalchemy**.

```
from typing import Any  
from geoalchemy2.types import Geometry  
  
class Stations(SQLModel, table=True):  
    station_id: str = Field(primary_key=True)  
    latitude: float  
    longitude: float  
    cp: str  
    city: str  
    adress: str  
    geom: Optional[Any] = Field(sa_column=Column(Geometry('GEOMETRY')))
```

Last modification to make: we want the geometry to be automatically calculated in the POST call (in main.py) using the latitude and longitude parameters:

```
from geoalchemy2.elements import WKTElement  
  
@app.post("/add-station/")  
async def add_station(station: Stations):  
    with Session(engine) as session:  
        exist = session.query(Stations).filter(  
            Stations.station_id == station.station_id).first()  
        if exist:  
            raise HTTPException(  
                status_code=400, detail="Station already exists")  
  
        #New code block  
        point = f"POINT({station.longitude} {station.latitude})"  
        station.geom = WKTElement(point, srid=4326)  
        #New code block  
  
        session.add(station)  
        session.commit()  
        session.refresh(station)  
  
        #This is only done to return a clean dictionnar with a proper json format  
        to_return = {}  
        to_return["station_id"] = station.station_id  
        to_return["latitude"] = station.latitude  
        to_return["longitude"] = station.longitude  
        to_return["cp"] = station.cp  
        to_return['city'] = station.city  
        to_return["adress"] = station.adress  
  
        return to_return
```

Here we are creating a point via a string using another format named WKTElement, which is a way to encode geometry using human-readable strings. Our string is then converted to geometry via the **geolalchemy** function WKTElement, which implicitly converts it into the WKB format to be encoded in the database.

Note that “geom” is not JSON serializable, so we need to modify it or remove it before sending back the station object via the API.

### Build the final GET query

The goal of the GET query is to retrieve all the stations within a 30km radius from a city identified via its postal code and show the fuel latest price of a certain type (also used in the query) of all the stations queried with a bunch of prettified stuff like a normalized address or a google map link.

```
{    
  "lat": 49.1414,  
  "lon": 2.5087,  
  "city": "Orry-la-Ville",  
  "station_infos": [  
    {  
      "address": "Zi Route de Crouy 60530 Neuilly-en-Thelle",  
      "price_per_L": 1.58,  
      "price_tank": 95,  
      "delta_average": 25.1,  
      "better_average": 1,  
      "google_map_link": "https://www.google.com/maps/search/?api=1&query=Zi+Route+de+Crouy+60530+Neuilly-en-Thelle",  
      "distance": 19.140224654602328,  
      "latitude": 49.229,  
      "longitude": 2.282  
    }, ...  
  ]  
}
```

We are going to do this in two steps:

* First building an efficient SQL query to perform the joins and filtering operations
* Modify the output of the query using python functions before sending the results via the API

Unlike other queries where the parameters were passed as a JSON in the body of the request, we will use here another convention, in which the query parameters are passed directly in the URL, see the example below:

```
http://localhost:8000/stations/?oil_type=SP98&postal_code=60560
```

In FastAPI, this is done very naturally by simply adding inputs to the function used to build the endpoint:

```
@app.get("/stations/")  
async def get_prices(oil_type: str, postal_code: str):  
  with Session(engine) as session:  
    ...
```

The first thing we want to retrieve now is the latitude and longitude of the city associated with a postal code. If no city is associated with the postal code, the API should return an error code stating that no postal code was found.

```
city = session.query(Cities).filter(  
         Cities.postal_code == postal_code  
       ).first()  
if not city:  
    raise HTTPException(  
        status_code=404, detail="Postal Code not found")
```

Next, we are going to build a series of subqueries. Each subquery will not be evaluated until the final query is fully executed. It will help us keep a readable code and optimize the query as sqlalchemy ORM dynamically optimize the query based on those subqueries.

The first subquery we want to make is to select all the stations from the Stations table that are within a 30km radius of the city already queried.

```
stations = session.query(  
    Stations.station_id, Stations.adress,  Stations.cp, Stations.city,  
    Stations.latitude, Stations.longitude,  
).filter(  
    ST_Distance(  
        Stations.geom.ST_GeogFromWKB(),  
        WKTElement(f"POINT({city.lon} {city.lat})",  
                   srid=4326).ST_GeogFromWKB()  
    ) < 30000).subquery()
```

Numerous interesting things to note here.

* We select only a few columns in session.query( … ) and we are not keeping the geom column which is done only for filtering purposes. In standard SQL, it would have been made doing “SELECT station\_id, adress, cp, city, latitude, longitude FROM stations”.
* We are using **ST\_Distance**, an in-built function of geoalchemy used to compute the distance between two geographies (another geoalchemy type).
* ST\_Distance could work also with geometries, but the output would become an angular distance (remember that lat/lon are expressed in angles), which is not what we want.
* To convert geometries to geographies, we simply use another inbuilt function, ST\_GeoFromWKB, which will automatically project our geometry in their reference system to a point on Earth.

Next, we filter the Gasprices table based on the desired oil\_type (SP95, Gazole, etc..)

```
  price_wanted_gas = session.query(GasPrices).filter(  
      GasPrices.nom == oil_type  
  ).subquery()
```

We also need to filter the Gasprices table based on the latest prices available in the dataset. This is not an easy task because all updates are not done at the same time for all the prices. We are going to build the subquery in two steps.

First, we perform an aggregation by taking the station\_id and the last update date from the price\_wanted\_gas sub-table.

```
last_price = session.query(  
    price_wanted_gas.c.station_id,  
    func.max(price_wanted_gas.c.maj).label("max_maj")  
    ).group_by(price_wanted_gas.c.station_id) \  
     .subquery()
```

This information is then used to help us filter price\_wanted\_gas via a join where only the rows with the latest update prices are kept. The “and\_” method allows us to use multiple conditions in our join operation.

```
last_price_full = session.query(price_wanted_gas).join(  
    last_price,  
    and_(  
        price_wanted_gas.c.station_id == last_price.c.station_id,  
        price_wanted_gas.c.maj == last_price.c.max_maj  
    )  
).subquery()
```

Finally, we operate a final join between the last\_price\_full subtable (containing all the latest prices of a given fuel) and the stations subtable (including all the stations within a 30km radius) and retrieve all the results.

```
stations_with_price = session.query(stations, last_price_full).join(  
    last_price_full,  
    stations.c.station_id == last_price_full.c.station_id  
).all()
```

Arrived at that point, we retrieved a filtered list of relevant stations merged with the relevant information from the GasPrices table (ie: prices) and we just need to post-process the output to fit the requirements of the front. As the table has been already cleaned and filtered at that point, this final postprocessing step can be done in raw Python without impacting too much the performances.

I will only elaborate a little on that final post-processing step as it is not in the core of the article but fill free to check the [GitHub](https://github.com/jkaub/station-prices-app-full) repository for more information.

```
prices = [float(e["valeur"]) for e in stations_with_price]  
avg_price = float(np.median(prices))  
  
output = {  
    "lat": city.lat,  
    "lon": city.lon,  
    "city": pretify_address(city.name),  
    "station_infos": sorted([extend_dict(x, avg_price, city.lat, city.lon) for x in stations_with_price], key=lambda x: -(x['delta_average']))  
}  
  
return output
```

We can now test and verify that the query is returning the relevant output. We could use a request in Python to check, but FastAPI also provides in-built documentation for all your endpoint in which you can test your API, available at <http://localhost:8000/docs>

Press enter or click to view image in full size

![]()

## Containerizing the application

Now that we have an API up and running, we will finish this article by packaging our application in containers.

This is how our project will be organized:

```
stations-project/  
  |-- db/  
  |-- api/  
    |-- app/  
    |-- requirements.txt  
    |-- Dockerfile  
  |-- update_scripts/  
  |-- front/  
  |-- docker-compose.yml
```

We are going to use the Dockerfile in api/ to containerize the API, and use docker-compose to manage simultaneously the API and the database.

The folder db/ is the volume the PostgreSQL container uses to persist the database.

### Packaging our API

To package our API we will simply build a docker image that will replicate the environment and dependencies required to run our API. This docker image will contain everything necessary to run our API, including the code, runtime, system tools, libraries, and configurations.

To do so, we need to write a Dockerfile which will contain the series of instructions to set up a FastAPI environment. Writing a Dockerfile is relatively easy when you understood the principle: it is like configuring a new machine from the beginning. In our case:

* We need to install the relevant version of python
* Setup the working directory
* Copy the relevant files in our working directory (including the requirements.txt which is mandatory to pip install all the libraries needed for the project
* Installing the libraries with pip install
* Expose FastAPI port
* Run the command that initializes the API (uvicorn main:app — reload)

Translated in Docker language, this becomes:

```
FROM python:3.9  
  
WORKDIR /code  
  
COPY ./requirements.txt /code/requirements.txt  
  
COPY ./app /code/app  
  
RUN pip install --no-cache-dir -r requirements.txt  
  
EXPOSE 80  
  
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

We also need to take care of the requirement.txt file in which we precise all the libraries used and their versions.

```
fastapi==0.94.0  
GeoAlchemy2==0.13.1  
numpy==1.24.2  
SQLAlchemy==1.4.41  
sqlmodel==0.0.8  
uvicorn==0.20.0  
psycopg2==2.9.5
```

With these updates made, we can now build the image of our container (from within the folder with the Dockerfile):

```
docker build -t fast-api-stations .
```

### Using docker-compose

**docker-compose** is a tool for defining and running multi-container Docker applications. In our case, we want to run both our SQL container as well as the FastAPI container. I will assume you have already docker-compose installed on your computer. If this is not the case, please follow [those instructions](https://docs.docker.com/compose/install/).

In order to use docker-compose, we simply need to configure a `docker-compose.yml` file in the root directory of our project, which defines the services that make up our application and their respective configurations.

The `docker-compose.yml` file uses YAML syntax to define a set of services, each representing a container that will be run as part of the global application. Each service can specify its image, build context, environment variables, persistent volumes, ports, etc…

This is how looks our docker-compose.yml:

```
version: "3"  
  
services:  
  fastapi:  
    image: fast-api-stations  
    ports:  
      - "8000:80"  
  
  stationdb:  
    image: postgis/postgis  
    environment:  
      POSTGRES_USER: jkaub  
      POSTGRES_PASSWORD: jkaub  
      POSTGRES_DB: stations  
    volumes:  
      - ./db:/var/lib/postgresql/data
```

As you can see, we are defining two services:

* one for the API, named now FastAPI, which is built on the Docker image fast-api-station that we created in the previous sub-section. For this service, we are exposing port 80 from the container to our local port 8000.
* one for the DB, running on the PostGIS image. We are specifying the same environmental variable as we were doing before and the same volume to persist in the database.

### One last small modification

We used to connect to the SQL engine using the local IP. As we are now running the API and PostgreSQL in two different environments, we need to switch the way we connect to the database.

docker-compose manage on its own network between the different containers and make it easy for us to connect from one service to another. In order to connect to the SQL service from the API service, we can specify the name of the service to which we want to connect in the engine creation:

```
DATABASE_URL = 'postgresql://jkaub:jkaub@stationdb/stations'
```

### Running the back-end

Now that we have configured everything, we can just run our back-end application by doing:

```
docker-compose up
```

And the API will be available via port 8000

```
http://localhost:8000/docs
```

## Conclusion

In this article, we have been working on the back end of our GasFinder Application.

We decided to store all the relevant data of the Application in our own storage solution to avoid all problems that could have been related to relying on a third-party connection.

We leveraged Docker and PostgreSQL+PostGIS to build a database allowing us to perform efficient geo-queries and used the Python framework FastAPI + SQLModel to build an efficient API that can be used to interact with the database and serve data to the frontend developed in the previous articles.

As of now, we have a Prototype based on “production standard” tools (React, PostgreSQL, FastAPI… ) that can run 100% locally. In the final part of this series, we will have a look at how to make the application live and automatically update our SQL tables to always provide the latest information available.