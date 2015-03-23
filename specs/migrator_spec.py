# -*- coding: utf-8 -*-

from expects import *
from doublex_expects import *
from doublex import *

from simpledatamigrate import migrator, collector


NO_SCHEMA = None
VER1 = '001'
VER2 = '002'
VER3 = '003'

with describe('Migrator'):
    with before.each:
        self.collector = Spy(collector.MigrationCollector)
        self.dataschema = Spy()
        self.subprocess = Spy()
        self.logger = Spy()
        self.migration = migrator.Migrator(self.dataschema, self.collector, subprocess_module=self.subprocess, logger=self.logger)

    with context('when no initial data/schema'):
        with it('execute migration from no schema to initial version'):
            when(self.collector).migrations().returns(['migrations/001.py'])
            when(self.dataschema).actual_schema().returns(NO_SCHEMA)

            self.migration.migrate_to(VER1)

            expect(self.subprocess.call).to(have_been_called_with(['python', 'migrations/001.py']))

        with it('sets the actual version to initial version'):
            when(self.collector).migrations().returns(['migrations/001.py'])
            when(self.dataschema).actual_schema().returns(NO_SCHEMA)
            when(self.subprocess).call(['python', 'migrations/001.py']).returns(0)

            self.migration.migrate_to(VER1)

            expect(self.dataschema.set_actual_schema).to(have_been_called_with(VER1))

        with it('logs an message'):
            when(self.collector).migrations().returns(['migrations/001.py'])
            when(self.dataschema).actual_schema().returns(NO_SCHEMA)
            when(self.subprocess).call(['python', 'migrations/001.py']).returns(0)

            self.migration.migrate_to(VER1)

            expect(self.logger.info).to(have_been_called_with(contain(VER1)))
            expect(self.logger.info).not_to(have_been_called_with(contain('error')))

        with context('when migration fails'):
            with it('does not  set the actual version'):
                when(self.collector).migrations().returns(['migrations/001.py'])
                when(self.dataschema).actual_schema().returns(NO_SCHEMA)
                when(self.subprocess).call(['python', 'migrations/001.py']).returns(1)

                self.migration.migrate_to(VER1)

                expect(self.dataschema.set_actual_schema).to_not(have_been_called_with(VER1))

            with it('log an error message'):
                when(self.collector).migrations().returns(['migrations/001.py'])
                when(self.dataschema).actual_schema().returns(NO_SCHEMA)
                when(self.subprocess).call(['python', 'migrations/001.py']).returns(1)

                self.migration.migrate_to(VER1)

                expect(self.logger.error).to(have_been_called_with(contain('Error', VER1)))

    with context('when two or more migrations required'):
        with it('execute the migrations'):
            when(self.collector).migrations().returns(['migrations/001.py', 'migrations/002.py', 'migrations/003.py'])
            when(self.dataschema).actual_schema().returns(VER1)

            self.migration.migrate_to(VER3)

            expect(self.subprocess.call).to(have_been_called_with(['python', 'migrations/002.py']))
            expect(self.subprocess.call).to(have_been_called_with(['python', 'migrations/003.py']))

