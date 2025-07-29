#!/bin/bash
cd "Travel Planner agent/Travel-Planner-AI"
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}