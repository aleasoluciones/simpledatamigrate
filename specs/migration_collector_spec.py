# -*- coding: utf-8 -*-

from expects import *
from doublex import *

import os
from simpledatamigrate import collector as c

with describe('MigrationCollector'):
    with context('when returning migrations'):
        with it('returns python files with older in first place'):
            relative_path = os.path.relpath(os.path.join(os.path.dirname(__file__), 'fixtures/migrations'))
            collector = c.MigrationCollector(relative_path)

            migrations = collector.migrations()

            expect(migrations).to(contain_exactly(
                '{}/001.py'.format(relative_path),
                '{}/002.py'.format(relative_path),
                '{}/003.py'.format(relative_path)
            ))

        with it('returns migrations with relative path'):
            relative_path = os.path.relpath(os.path.join(os.path.dirname(__file__), 'fixtures/migrations'))
            collector = c.MigrationCollector(relative_path)

            migrations = collector.migrations()

            expect(migrations[0]).to(contain(relative_path))
            expect(migrations[1]).to(contain(relative_path))
            expect(migrations[2]).to(contain(relative_path))
