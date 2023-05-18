#! /usr/bin/env sh
set -e

cd /app
python manage.py makemigrations --noinput 

python manage.py migrate --noinput 

./dumpdata.sh --noinput 
./loaddata.sh --noinput 
