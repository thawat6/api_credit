#!/bin/bash

# kill existing process
ps axf | grep jumpvrp | awk '{print $1}' | xargs kill -9 > /dev/null 2>&1 

#start new one
cd /root/jumpvrp-data-service
source ./bin/activate
cd dataservice

while true; do
python manage.py runserver 0.0.0.0:8000 > service.log 2>&1
done

exit 0
