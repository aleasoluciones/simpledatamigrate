# -*- coding: utf-8 -*-

from expects import *
from doublex import *

from simpledatamigrate import repositories as r

with describe('SchemaVersion repository'):
    with before.each:
        self.data_schema = r.SchemaVersionRepository()

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
