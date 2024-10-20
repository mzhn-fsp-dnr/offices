FROM python:3.12-alpine3.20

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ARG APP_PORT
EXPOSE $APP_PORT
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.12.1/wait wait
CMD chmod +x ./wait && ./wait \
    chmod +x ./entrypoint.sh && ./entrypoint.sh $APP_PORT