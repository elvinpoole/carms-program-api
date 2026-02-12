#!/bin/bash

# ingest data first
python pipelines/ingest_data.py

# then start FastAPI
uvicorn app.main:app --host 0.0.0.0 --port 8000