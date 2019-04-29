# -*- coding: utf-8 -*-

from expects import expect, be_none, be

from simpledatamigrate import repositories

with describe('SchemaVersion repository'):
    with before.each:
        self.data_schema = repositories.SchemaVersionRepository()

    with context('when query schema version'):
        with context('initial version case'):
            with it('returns none as initial schema version'):
                version = self.data_schema.current_schema()

                expect(version).to(be_none)

    with context('when change schema version'):
        with it('returns new state'):
               version = '001'
               self.data_schema.set_schema_version(version)

               current_version = self.data_schema.current_schema()

               expect(current_version).to(be(version))
