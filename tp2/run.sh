#!/bin/bash

pip install -r requirements.txt

python -m server &
python -m server_b &
