#!/bin/bash

# ingest data first
dagster dev -f pipelines/dagster_defs.py

# then start FastAPI
uvicorn app.main:app --host 0.0.0.0 --port 8000