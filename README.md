# carms-program-api

A simple API for accessing entries from a CaRMS database.

It uses PostgreSQL for storage, Dagster for pipeline orchestration, and interfaces with SQLAlchemy and FastAPI.

There is also a LangChain powered semantic search.

Currently, the API can filter on province or territory or do a simple semantic search using th econtents of each program description. The primary purpose of this API is to demonstrate familiarity with the stack.

## HOW TO RUN

1) Install git and clone this repo
```
sudo yum install -y git #if not already installed
git clone https://github.com/elvinpoole/carms-program-api.git
cd carms-program-api/
```

2) make a `.env` file with your OPENAI_API_KEY
```
echo "OPENAI_API_KEY=sk-your_api_key_here" >> .env
```

### Local setup

3) Build the image and start containers
```
docker compose up --build -d
```

### AWS setup

3) Run the AWS setup script
```
./setup_aws.sh
```

### Viewing the Results

View the results in a browser at http://<ip>:8000/frontend
and view (and re-run) the pipelines (dagster) at http://<ip>:3000/

where `<ip> is either localhost or the public ip of your AWS machine`

A hosted version is currently running on AWS EC2 and is available on request for demonstration purposes.

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
