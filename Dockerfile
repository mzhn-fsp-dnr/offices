FROM python:3.12-alpine3.20

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ARG APP_PORT
EXPOSE $APP_PORT
CMD chmod +x ./entrypoint.sh && ./entrypoint.sh $APP_PORT