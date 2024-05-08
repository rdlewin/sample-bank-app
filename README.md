# Bank API

This server is a simple implementation of a bank's internal transfers system, 
allowing users to create accounts, and transfer funds betweeen them.

## Setup
### Environment Variables

To run the server, you will need a [`.env`](.env) file, which isn't kept on git for security purposes.

To set it, rename or copy [`sample.env`](sample.env) to a file called [`.env`](.env):

Shell command on Linux / MacOS:
```shell
cp ./sample.env ./.env
```

## Running Locally
There are two ways to run the server locally:

### Docker Compose
The easiest way to run this project, including a database, is using [docker-compose](https://docs.docker.com/compose/):

```shell
docker compose up
```

### Local Execution
If you already have a PostgreSQL server up and .env confugred, you can run the server directly:

First, install the server's requirements locally:
```shell
pip install -r requirements.txt
```

Then run one of the following commands to run the server:
```shell
uvicorn src.main:app
```

```shell
fastapi dev src/main.py
```

## API
Once started, regardless of method, the server should be available on http://localhost:8000

You can find the automatically generated Swagger documentation at http://localhost:8000/docs

# Notes
1. This server currently does not implement any security or authentication mechanisms,
   but adding a JWT-based auth system would be quite simple to implement, 
   to stop things such as users sending requests to send funds from another user's account.
2. Due to SQLAlchemy being sensitive to the load order of models, they are for now all defined in [models.py](src/models.py).
   In a production-ready environment, I would refactor it properly, so they would be in separate files under the `/src/models` module.
3. There are multiple API and unit tests that I would like to implement, but decided to cut for time. 
4. Only basic type input validation is currently implemented.
   e.g. validating a user's email, a transaction's amount being a positive number, etc are not currently supported. 