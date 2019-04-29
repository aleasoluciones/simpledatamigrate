# -*- coding: utf-8 -*-

from expects import expect, equal, contain, raise_error
from doublex_expects import have_been_called, have_been_called_with
from doublex import Spy, when

from simpledatamigrate import migrator, repositories


with describe('Test Migrator'):
    with before.each:
        self.database = Spy(repositories.PostgresDatabaseRepository)
        self.migrator = Spy(migrator.Migrator)
        self.logger = Spy()
        self.test_migration = migrator.TestMigrator(self.database, self.migrator, logger=self.logger)

    with context('Feature: migrating on a testing environment'):
        with it('removes test database if exists before migration is performed'):
            self.test_migration.test_migrate()

            expect(self.database.remove_test_database).to(have_been_called)

        with it('creates test database before migration is performed'):
            self.test_migration.test_migrate()

            expect(self.database.create_test_database).to(have_been_called)

        with it('executes the migrations on test database'):
            self.test_migration.test_migrate()

            expect(self.migrator.migrate).to(have_been_called)

        with it('removes test database if exists after migration is performed'):
            self.test_migration.test_migrate()

            expect(self.database.remove_test_database).to(have_been_called.twice)

        with context('errors and logs'):
            with context('when removing test database fails'):
                with it('raises an error'):
                    when(self.database).remove_test_database().raises(Exception)

                    expect(lambda: self.test_migration.test_migrate()).to(raise_error(migrator.DatabaseManipulationError))
                    expect(self.logger.critical).to(have_been_called_with(contain('Error executing database manipulation')))


            with context('when creating test database fails'):
                with it('raises an error'):
                    when(self.database).create_test_database().raises(Exception)

                    expect(lambda: self.test_migration.test_migrate()).to(raise_error(migrator.DatabaseManipulationError))
                    expect(self.logger.critical).to(have_been_called_with(contain('Error executing database manipulation')))
