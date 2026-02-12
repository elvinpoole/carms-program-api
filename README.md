# carms-program-api

A very simple API to access entries from a CaRMS database

Currently this example simply lists the first N programs in the database

## HOW TO RUN

### Command line setup

Build the image and start containers
```
docker-compose build
docker-compose up
```

View the results in a browser at http://localhost:8000/

## STRUCTURE

             ┌──────────────┐
             │  Markdown    │
             │  CSV Files   │
             └──────┬───────┘
                    │
                pipelines/
                 (pandas)
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
