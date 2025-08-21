# This is installing the pgvector extension for postgres
from postgres:17

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    postgresql-server-dev-all \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /tmp

RUN git clone https://github.com/pgvector/pgvector.git

WORKDIR /tmp/pgvector
RUN make
RUN make install

# Create pgvector extension during db init

RUN mkdir -p /docker-entrypoint-initdb.d
COPY ./create_extension.sql /docker-entrypoint-initdb.d/