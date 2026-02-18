#!/bin/bash
set -e

# Activate virtual environment
source /home/airflow/.venv/bin/activate

# Start Airflow 
airflow standalone 

