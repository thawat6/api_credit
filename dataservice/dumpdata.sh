#!/bin/bash
DIR="dataservice/fixtures"

python manage.py dumpdata --indent=2 --exclude=contenttypes --exclude=auth.Permission auth > $DIR/auth.json
python manage.py dumpdata --indent=2 --natural-foreign data_api > $DIR/data_api.json
