# -*- coding: utf-8 -*-

from expects import *
from doublex import *

from simpledatamigrate import repositories as r

with describe('SchemaVersion repository'):
    with context('when query schema version'):
        with context('initial version case'):
            with it('returns none as initial schema version'):
                data_schema = r.SchemaVersionRepository()

                version = data_schema.actual_schema()

                expect(version).to(be_none)
        with _context('there is a version'):
            with it('returns the current schema version'):
                data_schema = r.SchemaVersionRepository()
                version = data_schema.actual_schema()
                expect(version).to(equal(42))

    with context('when change schema version'):
        with it('returns new state'):
               ver = '001'
               data_schema = r.SchemaVersionRepository()
               data_schema.set_actual_schema(ver)
               version = data_schema.actual_schema()
               expect(version).to(be(ver))
