# Backend_task_02

## Deutsch

Die Aufgabe setzt sich aus drei Teilaufgaben zusammen, die alle bearbeitet werden müssen. Ziel ist die Erstellung einer einfachen Rest-API zur Verwaltung von Straßennetzen. Zur Aufgabenbearbeitung befinden sich hierzu beigefügt drei Beispiel-Straßennetze (Knoten-Kanten-Modelle) im GeoJSON-Format.

### Aufgabe 1

Die ersten beiden Straßennetze sollen über einen Endpunkt hochgeladen und in einer PostgreSQL Datenbank gespeichert werden können. Da die Straßennetze im Wesentlichen aus Geometrien bestehen, ist die Nutzung einer Geo-Erweiterung wie PostGIS zu empfehlen, um die Daten effizient speichern zu können. Da die Straßennetze zu unterschiedlichen Kunden gehören, müssen Sie über ein entsprechendes Attribut verfügen, um eine einfache Autorisierung zu ermöglichen.

### Aufgabe 2

Das dritte Straßennetz stellt eine aktualisierte Version des zweiten Netzes dar. Über einen weiteren Endpunkt soll es möglich sein, ein Update durchzuführen, indem die aktualisierte Version des Netzes hochgeladen wird. Bei einem Update sollen die ursprünglichen Kanten nicht gelöscht werden, sondern nur als nicht aktuell gekennzeichnet werden.

### Aufgabe 3

Die Kanten der Straßennetze sollen über einen weiteren Endpunkt im GeoJSON Format abgerufen werden können. Der Endpunkt soll nur die Kanten des angegebenen Netzes eines jeweils authentifizierten Kunden zurückgeben. Über einen Parameter soll zudem angegeben werden können, welchem Zeitpunkt das Netz entsprechen soll. D.h. Netz 2 soll in seinem Zustand vor und nach Update abgerufen werden können.

### Vorgaben

1. Als API-Framework soll Flask oder FastAPI zu verwenden, während die Datenbank mittels Postgres zu realisieren ist.
2. Eine README.md soll die Anwendung sowie die Herangehensweise an die Aufgabenstellung dokumentieren.
3. Die Lösung muss zwingend containerisiert und mittels Docker-Compose einfach ausführbar sein.

## English

The task is made up of three subtasks, all of which must be completed. The aim is to create a simple Rest API for managing road networks. Three example road networks (node-edge models) in GeoJSON format are attached for processing the task.

### Task 1

The first two road networks should be uploaded via an endpoint and stored in a PostgreSQL database. Since the road networks essentially consist of geometries, the use of a geo-extension such as PostGIS is recommended in order to store the data efficiently. As the road networks belong to different customers, they must have a corresponding attribute to enable simple authorization.

### Task 2

The third road network is an updated version of the second network. It should be possible to perform an update via another endpoint by uploading the updated version of the network. During an update, the original edges should not be deleted, but only marked as not up-to-date.

### Task 3

The edges of the road networks should be retrievable via an additional endpoint in GeoJSON format. The endpoint should only return the edges of the specified network of an authenticated customer. It should also be possible to use a parameter to specify which point in time the network should correspond to, i.e. network 2 should be able to be retrieved in its state before and after the update.

### Specifications

1. The API framework to be used should be Flask or FastAPI, while the database is to be realized using Postgres.
2. A README.md should document the application and the approach to the task.
3. The solution must be containerized and readily executable using Docker-Compose.

# Solution
## Set-up dev environment
- Create venv in root dir: `python -m venv ./venv`
- Activate venv. Depends on OS: Linux: `source ./venv/bin/activate`
- Install dependencies:  `pip install -r requirements.txt`
- Set-up pre-commit hooks: `pre-commit install`

## Start application
- In the root folder run: `docker-compose up -d`
- This will start a python container running a flask application and a postgres container with installed PostGIS extension.

## Application architecture
The following picture shows the architecture of the application. The user sends a HTTP request to the flask application, which is listening on port 5000, via e.g. curl/Browser/Postman.
This application uses the ORM-mapper SQLAlchemy and GeoAlchemy2 to interact with the Postgres database for creating and modifying objects.

```mermaid
graph TD
    Client[Curl / Browser / API Client]
    Client -->|HTTP Request| FlaskApp[Flask Application]
    FlaskApp --> SQLAlchemy[SQLAlchemy/GeoAlchemy2]
    SQLAlchemy --> Postgres[(PostgreSQL Database)]
 ```
The following ER diagram shows the used entities:
The RoadNetwork is identified by an ID and a version number. Moreover, the use to whom this network belongs is stored as string.
The road has the GPS coordinates as LineString and the properties as JSON.
Via the composite foreign key constraint, many roads are associated to one RoadNetwork (**one-to-many association**).
```mermaid
erDiagram
    ROAD_NETWORKS {
        int id PK
        int version PK
        string owner
    }

    ROADS {
        int id PK
        int road_network_id FK
        int road_network_version FK
        Geometry line_geometry
        JSON properties
    }

    ROAD_NETWORKS ||--o{ ROADS : contains
    ROADS }o--|| ROAD_NETWORKS : belongs_to
```

## API
The API provides the following endpoints.

### POST localhost:5000/

#### Request
- **Method:** `POST`
- **URL:** `localhost:5000/`
- **Auth Required:** Yes (Bearer Token)

#### Description
Creates a new RoadNetwork belonging to the authenticated User.

#### Body Parameters
| Name   | Type | Required | Description                                                     |
|--------|------|----------|-----------------------------------------------------------------|
| `file` | File | Yes      | A geoJSON file based on this the RoadNetwork should be created. |

### GET localhost:5000/{id}

#### Description
Retrieve the RoadNetwork with this ID and the specified version.

#### Request
- **Method:** `GET`
- **URL:** `localhost:5000/{id}`
- **Auth Required:** Yes (Bearer Token)

#### Path Parameters
| Name      | Type   | Required | Description                                |
|-----------|--------|----------|--------------------------------------------|
| `id`      | int    | Yes      | The unique identifier of the road network. |

#### Query Parameters
| Name      | Type | Required | Description                                        |
|-----------|------|----------|----------------------------------------------------|
| `version` | int  | No       | The version of interest. If not given, use latest. |

### PUT localhost:5000/{id}

#### Request
- **Method:** `PUT`
- **URL:** `localhost:5000/{id}`
- **Auth Required:** Yes (Bearer Token)

#### Path Parameters
| Name      | Type   | Required | Description                                                        |
|-----------|--------|----------|--------------------------------------------------------------------|
| `id`      | int    | Yes      | The unique identifier of the road network which should be updated. |

#### Body Parameters
| Name   | Type | Required | Description                                                    |
|--------|------|----------|----------------------------------------------------------------|
| `file` | File | Yes      | The GeoJSON file containing the new edges for the RoadNetwork. |

## API Usage
- Create a Bearer token at [JWT.io](http://jwt.io) (Choose sub, name and iat as u want and **secret=42**)
- Copy token to use via Postman / curl

### Postman
Copy the URLs and add the token as Bearer token to the request in the Authorization tab. Add the mention query/body parameters to the requests.

### CURL
If you prefer using the curl command via shell:

``
curl -X POST "http://localhost:5000/" \
     -H "Authorization: Bearer YOUR_BEARER_TOKEN" \
     -H "Content-Type: application/json" \
     -F "file=@/road_network_aying_1.0.geojson
``
