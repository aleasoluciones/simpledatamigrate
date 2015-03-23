# -*- coding: utf-8 -*-

from expects import *
from doublex import *

import os
from simpledatamigrate import collector as c

with describe('MigrationCollector'):
    with context('when returning migrations'):
        with it('returns older in first place'):
            collector = c.MigrationCollector(os.path.join(os.path.dirname(__file__), 'fixtures/migrations'))

            migrations = collector.migrations()

            expect(migrations).to(contain_exactly('001.py', '002.py', '003.py'))

