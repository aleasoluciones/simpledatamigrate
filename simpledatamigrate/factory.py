#!/usr/bin/env python

import os
import psycopg2 as pg
from simpledatamigrate import repositories as r, collector as c, migrator as m

def create_postgres_migrator():
    connection = pg.connect(
        host=os.getenv('COMPONENT_DB_HOST_ADDR'),
        port=os.getenv('COMPONENT_DB_TCP_PORT'),
        database=os.getenv('COMPONENT_DB_NAME'),
        user=os.getenv('COMPONENT_DB_USER'),
        password=os.getenv('COMPONENT_DB_PASSWORD')
    )

    schema_version_repo = r.PostgresSchemaVersionRepository(connection)
    migrations_folder = os.environ['MIGRATIONS_FOLDER']
    collector = c.MigrationCollector(migrations_folder)

    return m.Migrator(schema_version_repo, collector)

