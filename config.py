import os

postgresql = {
                'host': os.environ.get('POSTGRES_HOST'),
                'user': os.environ.get('POSTGRES_USER'),
                'password': os.environ.get('POSTGRES_PASSWORD'),
                'db': os.environ.get('POSTGRES_DB')
            }

postgresqlConfig = "postgresql+psycopg2://{}:{}@{}/{}".format(postgresql['user'], postgresql['password'], postgresql['host'], postgresql['db'])
