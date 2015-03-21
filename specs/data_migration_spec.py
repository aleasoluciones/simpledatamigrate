# -*- coding: utf-8 -*-

from expects import *
from doublex_expects import *
from doublex import *

with describe('foo'):
    with before.each:
        pass

    with context('foo1'):
        with it('bar'):
            
            expect(True).to(be(True))