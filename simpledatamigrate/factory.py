#!/usr/bin/env python

import os
import psycopg2 as pg
from simpledatamigrate import repositories, collector, migrator


def create_postgres_migrator():
    connection = pg.connect(
        host=os.getenv('COMPONENT_DB_HOST_ADDR'),
        port=os.getenv('COMPONENT_DB_TCP_PORT'),
        database=os.getenv('COMPONENT_DB_NAME'),
        user=os.getenv('COMPONENT_DB_USER'),
        password=os.getenv('COMPONENT_DB_PASSWORD')
    )

    schema_version_repository = repositories.PostgresSchemaVersionRepository(connection)
    migrations_folder = os.environ['MIGRATIONS_FOLDER']
    migration_collector = collector.MigrationCollector(migrations_folder)

    return migrator.Migrator(schema_version_repository, migration_collector)


def create_test_postgres_migrator():
    migration_test_db = 'migration_test_db'

    connection = pg.connect(
        host=os.getenv('COMPONENT_DB_HOST_ADDR'),
        port=os.getenv('COMPONENT_DB_TCP_PORT'),
        database=migration_test_db,
        user=os.getenv('COMPONENT_DB_USER'),
        password=os.getenv('COMPONENT_DB_PASSWORD')
    )

    database_repository = repositories.PostgresDatabaseRepository(connection)
    migrator = create_postgres_migrator()

    return migrator.TestMigrator(database_repository, migrator)
