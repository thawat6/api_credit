FROM tiangolo/uwsgi-nginx:python3.8

ENV LISTEN_PORT 8006

EXPOSE 8006

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY ./dataservice/. /app/

RUN chmod a+x /app/prestart.sh
