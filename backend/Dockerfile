FROM python:3.8.0-alpine3.10

WORKDIR /usr/src/market

RUN apk add --no-cache gcc musl-dev linux-headers
COPY . .
RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

CMD [ "python", "main.py" ]
