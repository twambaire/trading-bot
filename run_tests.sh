#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run tests with pytest
python -m pytest tests/ -v

