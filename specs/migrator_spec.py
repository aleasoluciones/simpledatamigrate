# -*- coding: utf-8 -*-

from expects import *
from doublex_expects import *
from doublex import *

from simpledatamigrate import migrator


NO_SCHEMA = 'noschema'
VER1 = 'ver1'
VER2 = 'ver2'
VER3 = 'ver3'

with describe('Migrator'):
    with before.each:
        self.fs = Spy()
        self.dataschema = Spy()
        self.subprocess = Spy()
        self.logger = Spy()
        self.migration = migrator.Migrator(self.dataschema, filesystem=self.fs, subprocess_module=self.subprocess, logger=self.logger)

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
