# -*- coding: utf-8 -*-

import os
import subprocess
import logging

class MigrationFileNotFoundError(Exception):
    def __init__(self, dest):
        self.dest = dest


class Migrator(object):
    def __init__(self, dataschema, collector, subprocess_module=subprocess, logger=logging.getLogger()):
        self.dataschema = dataschema
        self.subprocess_module = subprocess_module
        self.basepath = 'migrations'
        self.logger = logger
        self.collector = collector

    def extract_versions_from_file(self, file):
        versions, extension = os.path.splitext(file)
        return versions.split('_')

    def migrate_to(self, dest_version):
        try:
            actual_schema_version = self.dataschema.actual_schema()
            files = self.collector.migrations()
            migrations_to_execute = self._select_migrations(files, actual_schema_version, dest_version)

            for migration in migrations_to_execute:
                self._execute_migration(migration)
        except MigrationFileNotFoundError as exc:
            self.logger.error("Error migration not found to migrate to {}".format(exc.dest))

    def _find_file_with_destination(self, dest, files):
        for f in reversed(files):
            initial_version, destination_version = self.extract_versions_from_file(f)
            if destination_version == dest:
                return f
        raise MigrationFileNotFoundError(dest)

    def _execute_migration(self, migration):
            return_value = self.subprocess_module.call(['python', os.path.join(self.basepath, migration)])
            ini, dest = self.extract_versions_from_file(migration)

            if return_value == 0:
                self.dataschema.set_actual_schema(dest)
                self.logger.info("Migration {} to {} executed".format(ini, dest))
            else:
                self.logger.error("Error executing migration from {} to {}".format(ini, dest))

    def _select_migrations(self, files, actual_version, dest_version):
        migrations_to_execute = []
        version = dest_version
        while True:
            file_to_execute = self._find_file_with_destination(dest_version, files)
            ini_ver, dest_version = self.extract_versions_from_file(file_to_execute)
            migrations_to_execute.append(file_to_execute)
            if ini_ver == actual_version:
                break
            else:
                dest_version = ini_ver

        return reversed(migrations_to_execute)

