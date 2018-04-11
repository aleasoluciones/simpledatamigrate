# -*- coding: utf-8 -*-

from expects import *
from doublex_expects import *
from doublex import *

from simpledatamigrate import migrator, collector, repositories as r


NO_SCHEMA = None
VER1 = '001'
VER2 = '002'
VER3 = '003'
VER4 = '004'

with describe('Migrator'):
    with before.each:
        self.collector = Spy(collector.MigrationCollector)
        self.dataschema = r.SchemaVersionRepository()
        self.subprocess = Spy()
        self.logger = Spy()
        self.migration = migrator.Migrator(self.dataschema, self.collector, subprocess_module=self.subprocess, logger=self.logger)

    with context('when no initial data/schema'):
        with it('execute migration from no schema to initial version'):
            when(self.collector).migrations().returns(['migrations/001.py'])
            when(self.subprocess).call(['python', 'migrations/001.py']).returns(0)

            self.migration.migrate()

            expect(self.subprocess.call).to(have_been_called_with(['python', 'migrations/001.py']))

        with it('sets the current version to initial version'):
            when(self.collector).migrations().returns(['migrations/001.py'])
            when(self.subprocess).call(['python', 'migrations/001.py']).returns(0)

            self.migration.migrate()

            expect(self.dataschema.current_schema()).to(equal(VER1))

    with context('errors and logs'):
        with context('when there are no errors'):
            with it('logs a message with the version successfully migrated'):
                when(self.collector).migrations().returns(['migrations/001.py'])
                when(self.subprocess).call(['python', 'migrations/001.py']).returns(0)

                self.migration.migrate()

                expect(self.logger.info).to(have_been_called_with(contain(VER1)))
                expect(self.logger.info).not_to(have_been_called_with(contain('error')))

        with context('when migration fails'):
            with it('raises an error and log the critical log'):
                when(self.collector).migrations().returns(['migrations/001.py'])
                when(self.subprocess).call(['python', 'migrations/001.py']).returns(1)

                expect(lambda: self.migration.migrate()).to(raise_error(migrator.MigrationExecutionError))
                expect(self.logger.critical).to(have_been_called_with(contain('Error', VER1)))

            with it('does not update current version'):
                when(self.collector).migrations().returns(['migrations/001.py'])
                when(self.subprocess).call(['python', 'migrations/001.py']).returns(1)

                expect(lambda: self.migration.migrate()).to(raise_error(migrator.MigrationExecutionError))
                expect(self.dataschema.current_schema()).to(equal(None))

        with context('when several migrations are required and the first one fails'):
            with it('does not continue with the pending migrations'):
                when(self.collector).migrations().returns(['migrations/001.py', 'migrations/002.py'])
                when(self.subprocess).call(['python', 'migrations/001.py']).returns(1)
                when(self.subprocess).call(['python', 'migrations/002.py']).returns(0)

                expect(lambda: self.migration.migrate()).to(raise_error(migrator.MigrationExecutionError))
                expect(self.subprocess.call).to(have_been_called_with(['python', 'migrations/001.py']))
                expect(self.subprocess.call).not_to(have_been_called_with(['python', 'migrations/002.py']))

    with context('when several migrations are required'):
        with it('execute the migrations'):
            when(self.collector).migrations().returns(['migrations/001.py', 'migrations/002.py', 'migrations/003.py'])
            when(self.subprocess).call(['python', 'migrations/001.py']).returns(0)
            when(self.subprocess).call(['python', 'migrations/002.py']).returns(0)
            when(self.subprocess).call(['python', 'migrations/003.py']).returns(0)

            self.migration.migrate()

            expect(self.subprocess.call).to(have_been_called_with(['python', 'migrations/001.py']))
            expect(self.subprocess.call).to(have_been_called_with(['python', 'migrations/002.py']))
            expect(self.subprocess.call).to(have_been_called_with(['python', 'migrations/003.py']))

        with context('when exists a current version'):
            with it('execute the migrations since the latest migrate version'):
                when(self.collector).migrations().returns(['migrations/001.py', 'migrations/002.py', 'migrations/003.py'])
                when(self.subprocess).call(['python', 'migrations/002.py']).returns(0)
                when(self.subprocess).call(['python', 'migrations/003.py']).returns(0)
                self.dataschema.set_schema_version(VER1)

                self.migration.migrate()

                expect(self.subprocess.call).not_to(have_been_called_with(['python', 'migrations/001.py']))
                expect(self.subprocess.call).to(have_been_called_with(['python', 'migrations/002.py']))
                expect(self.subprocess.call).to(have_been_called_with(['python', 'migrations/003.py']))

            with context('when current version is bigger than hightest '):
                with it('does not execute any migration'):
                    when(self.collector).migrations().returns(['migrations/001.py', 'migrations/002.py', 'migrations/003.py'])
                    when(self.subprocess).call(['python', 'migrations/001.py']).returns(0)
                    when(self.subprocess).call(['python', 'migrations/002.py']).returns(0)
                    when(self.subprocess).call(['python', 'migrations/003.py']).returns(0)
                    self.dataschema.set_schema_version(VER4)

                    self.migration.migrate()

                    expect(self.subprocess.call).not_to(have_been_called_with(['python', 'migrations/001.py']))
                    expect(self.subprocess.call).not_to(have_been_called_with(['python', 'migrations/002.py']))
                    expect(self.subprocess.call).not_to(have_been_called_with(['python', 'migrations/003.py']))
