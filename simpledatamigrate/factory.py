#!/usr/bin/env python

import os
import psycopg2 as pg
from simpledatamigrate import repositories as r, collector as c, migrator as m

def create_postgres_migrator():
    connection = pg.connect(
        host=os.getenv('INVENTORY_DB_PORT_5432_TCP_ADDR', 'localhost'),
        port=os.getenv('INVENTORY_DB_PORT_5432_TCP_PORT', '5432'),
        database=os.getenv('INVENTORY_DB_ENV_DBNAME', 'default'),
        user=os.getenv('INVENTORY_DB_ENV_DBUSER', 'postgres'),
        password=os.getenv('INVENTORY_DB_ENV_POSTGRES_PASSWORD', '12345')
    )

    schema_version_repo = r.PostgresSchemaVersionRepository(connection)
    migrations_folder = os.getenv('MIGRATIONS_FOLDER', 'migrations')
    collector = c.MigrationCollector(migrations_folder)

    return m.Migrator(schema_version_repo, collector)

