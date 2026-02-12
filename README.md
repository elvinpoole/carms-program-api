# carms-program-api

A simple API for accessing entries from a CaRMS database.

It uses PostgreSQL for storage, Dagster for pipeline orchestration, and interfaces with SQLAlchemy and FastAPI.

Currently, the API lists the first N programs currently stored in the database to demonstrate familiarity with the stack. Future plans include expanding functionality, such as search functions and integrating LangChain.

## HOW TO RUN (LOCAL)

### Command line setup

Build the image and start containers
```
docker compose up --build
```

View the results in a browser at http://localhost:8000/programs?limit=5
and view (and re-run) the pipelines (dagster) at http://localhost:3000/

## AWS

This API can also be run on AWS (e.g., EC2) using the docker image. A hosted version is available on request for demonstration purposes.

## STRUCTURE

             ┌──────────────┐
             │  Markdown    │
             │  CSV Files   │
             └──────┬───────┘
                    │
                pipelines/
                 (Dagster)
                    │
             ┌──────▼───────┐
             │ PostgreSQL   │
             │  Structured  │
             │  Tables      │
             └──────┬───────┘
                    │
                   app/
           (FastAPI + SQLAlchemy)
                    │
             ┌──────▼───────┐
             │ API Clients  │
             │ Browser      │
             │ Frontend     │
             └──────────────┘
