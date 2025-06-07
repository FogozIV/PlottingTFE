#!/bin/bash
echo "Freezing requirements.txt..."
source .venv/bin/activate
pip freeze > requirements.txt
git add requirements.txt