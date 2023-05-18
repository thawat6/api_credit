#!/bin/bash
DIR="dataservice/fixtures"

python3 manage.py loaddata  $DIR/auth.json
python3 manage.py loaddata  $DIR/data_api_v2.json
