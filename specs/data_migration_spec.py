# -*- coding: utf-8 -*-

from expects import *
from doublex_expects import *
from doublex import *

import subprocess
import os.path
import logging


NO_SCHEMA = 'noschema'
VER1 = 'ver1'
VER2 = 'ver2'
VER3 = 'ver3'

class MigrationFileNotFoundError(Exception):
    def __init__(self, dest):
        self.dest = dest


class Migrator(object):
    def __init__(self, dataschema, filesystem=os, subprocess_module=subprocess, logger=logging.getLogger()):
        self.dataschema = dataschema
        self.subprocess_module = subprocess_module
        self.basepath = 'migrations'
        self.logger = logger
        self.filesystem = filesystem

    def extract_versions_from_file(self, file):
        versions, extension = os.path.splitext(file)
        return versions.split('_')

    def migrate_to(self, dest_version):
        try:
            actual_schema_version = self.dataschema.actual_schema()
            files = sorted(self.filesystem.listdir(self.basepath + '/'))
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

with describe('Data migrator'):
    with before.each:
        self.fs = Spy()
        self.dataschema = Spy()
        self.subprocess = Spy()
        self.logger = Spy()
        self.migration = Migrator(self.dataschema, filesystem=self.fs, subprocess_module=self.subprocess, logger=self.logger)

    with context('when no initial data/schema'):
        with it('execute migration from no schema to initial version'):
            when(self.fs).listdir('migrations/').returns(['noschema_ver1.py'])
            when(self.dataschema).actual_schema().returns(NO_SCHEMA)

            self.migration.migrate_to(VER1)

            expect(self.subprocess.call).to(have_been_called_with(['python', 'migrations/%s_%s.py' % (NO_SCHEMA, VER1)]))

        with it('set the actual version to initial version'):
            when(self.fs).listdir('migrations/').returns(['noschema_ver1.py'])
            when(self.dataschema).actual_schema().returns(NO_SCHEMA)
            when(self.subprocess).call(['python', 'migrations/%s_%s.py' % (NO_SCHEMA, VER1)]).returns(0)

            self.migration.migrate_to(VER1)

            expect(self.dataschema.set_actual_schema).to(have_been_called_with(VER1))

        with it('log an message'):
            when(self.fs).listdir('migrations/').returns(['noschema_ver1.py'])
            when(self.dataschema).actual_schema().returns(NO_SCHEMA)
            when(self.subprocess).call(['python', 'migrations/%s_%s.py' % (NO_SCHEMA, VER1)]).returns(0)

            self.migration.migrate_to(VER1)

            expect(self.logger.info).to(have_been_called_with(contain(NO_SCHEMA, VER1)))
            expect(self.logger.info).not_to(have_been_called_with(contain('error')))

        with context('when migration fails'):
            with it('does not  set the actual version'):
                when(self.fs).listdir('migrations/').returns(['noschema_ver1.py'])
                when(self.dataschema).actual_schema().returns(NO_SCHEMA)
                when(self.subprocess).call(['python', 'migrations/%s_%s.py' % (NO_SCHEMA, VER1)]).returns(1)

                self.migration.migrate_to(VER1)

                expect(self.dataschema.set_actual_schema).to_not(have_been_called_with(VER1))

            with it('log an error message'):
                when(self.fs).listdir('migrations/').returns(['noschema_ver1.py'])
                when(self.dataschema).actual_schema().returns(NO_SCHEMA)
                when(self.subprocess).call(['python', 'migrations/%s_%s.py' % (NO_SCHEMA, VER1)]).returns(1)

                self.migration.migrate_to(VER1)

                expect(self.logger.error).to(have_been_called_with(contain('Error', NO_SCHEMA, VER1)))

    with context('when two or more migrations required'):
        with it('execute the migrations'):
            when(self.fs).listdir('migrations/').returns(['ver2_ver3.py', 'ver3_ver4.py', 'ver1_ver2.py'])
            when(self.dataschema).actual_schema().returns(VER1)

            self.migration.migrate_to(VER3)

            expect(self.subprocess.call).to(have_been_called_with(['python', 'migrations/%s_%s.py' % (VER1, VER2)]))
            expect(self.subprocess.call).to(have_been_called_with(['python', 'migrations/%s_%s.py' % (VER2, VER3)]))

        with context('when a migration is missing'):
            with it('does not execute any migration'):
                when(self.fs).listdir('migrations/').returns(['ver2_ver3.py', 'ver3_ver4.py'])
                when(self.dataschema).actual_schema().returns(VER1)

                self.migration.migrate_to(VER3)

                expect(self.subprocess.call).not_to(have_been_called)

            with it('log an error message'):
                when(self.fs).listdir('migrations/').returns(['ver2_ver3.py', 'ver3_ver4.py'])
                when(self.dataschema).actual_schema().returns(VER1)

                self.migration.migrate_to(VER3)

                expect(self.logger.error).to(have_been_called_with(contain('Error', 'migration not found', VER2)))
