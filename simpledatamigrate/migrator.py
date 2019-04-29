# -*- coding: utf-8 -*-

import os
import subprocess
import logging

class MigrationExecutionError(Exception):
    def __init__(self, dest):
        self.dest = dest


class DatabaseManipulationError(Exception):
    pass


class Migrator(object):
    def __init__(self, dataschema, collector, subprocess_module=subprocess, logger=logging.getLogger()):
        self.dataschema = dataschema
        self.subprocess_module = subprocess_module
        self.logger = logger
        self.collector = collector

    def extract_version_from_file(self, file_):
        versions, extension = os.path.splitext(os.path.basename(file_))
        return versions

    def migrate(self):
        try:
            current_schema_version = self.dataschema.current_schema()
            migrations = self.collector.migrations()
            migrations_to_execute = self._select_migrations(migrations, current_schema_version)
            for migration in migrations_to_execute:
                self._execute_migration(migration)
        except MigrationExecutionError as exc:
            self.logger.critical("Error executing migration {}".format(exc.dest))
            raise

    def _select_migrations(self, migrations, current_version):
        return migrations[self._index_for_version(migrations, current_version): None]

    def _index_for_version(self, migrations, version):
        if version is None:
            return 0

        for index, migration in enumerate(migrations):
            if version in migration:
                return index + 1
        return len(migrations)

    def _execute_migration(self, migration):
        return_value = self.subprocess_module.call(['python', migration])
        target = self.extract_version_from_file(migration)

        if return_value == 0:
            self.dataschema.set_schema_version(target)
            self.logger.info("Migration {} successfully executed".format(target))
        else:
            raise MigrationExecutionError(target)


class TestMigrator(object):
    def __init__(self, database, migrator, logger=logging.getLogger()):
        self.database = database
        self.migrator = migrator
        self.logger = logger

    def test_migrate(self):
        self._execute_database_manipulation_command(self.database.remove_test_database)
        self._execute_database_manipulation_command(self.database.create_test_database)
        self.migrator.migrate()
        self._execute_database_manipulation_command(self.database.remove_test_database)

    def _execute_database_manipulation_command(self, command):
        try:
            command()
        except Exception as exc:
            message = "Error executing database manipulation {}".format(exc)
            self.logger.critical(message)
            raise DatabaseManipulationError(message)
