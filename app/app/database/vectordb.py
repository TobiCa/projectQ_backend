import os
from langchain_community.vectorstores.pgvector import PGVector


class VectorDB:
    def __init__(self):
        # Getting environment variables
        host = os.environ.get('PGVECTOR_HOST')
        database = os.environ.get('PGVECTOR_DATABASE')
        user = os.environ.get('PGVECTOR_USER')
        password = os.environ.get('PGVECTOR_PASSWORD')
        sslmode = os.environ.get('PGVECTOR_SSLMODE')
        driver = os.environ.get("PGVECTOR_DRIVER", "psycopg2")
        port = int(os.environ.get("PGVECTOR_PORT", "5432"))

        # Psycopg2 connection string for checking db connection
        self.conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, database, password, sslmode)

        # Create connection string for PGVector
        self.pgvector_conn_string = PGVector.connection_string_from_db_params(
            driver, host, port, database, user, password
        )
