# -*- coding: utf-8 -*-

from expects import *
from doublex_expects import *
from doublex import *

import subprocess
import os.path
import logging



class Migration(object):
    def __init__(self, dataschema, subprocess_module=subprocess, logger=logging.getLogger()):
        self.dataschema = dataschema
        self.subprocess_module = subprocess_module
        self.basepath = 'migrations'
        self.logger = logger
    
    def migrate_to(self, dest_version):
        actual_schema_version = self.dataschema.actual_schema()
        return_value =self.subprocess_module.call(['python', os.path.join(self.basepath, '%s_%s.py' % (actual_schema_version, dest_version))])
        if return_value == 0:
            self.dataschema.set_actual_schema(dest_version)
            self.logger.info("migration from {} to {} executed".format(actual_schema_version, dest_version))
        else:
            self.logger.info("error executing migration from {} to {}".format(actual_schema_version, dest_version))

NO_SCHEMA = 'no_schema'
VER1 = 'ver1'

with describe('Data migration'):
    with before.each:
        self.dataschema = Spy()
        self.subprocess = Spy()
        self.logger = Spy()
        self.migration = Migration(self.dataschema, subprocess_module=self.subprocess, logger=self.logger)

    with context('when no initial data/schema'):
        with it('execute migration from no schema to initial version'):
            when(self.dataschema).actual_schema().returns(NO_SCHEMA)
            
            self.migration.migrate_to(VER1)
            
            expect(self.subprocess.call).to(have_been_called_with(['python', 'migrations/%s_%s.py' % (NO_SCHEMA, VER1)]))
        
        with it('set the actual version to initial version'):
            when(self.dataschema).actual_schema().returns(NO_SCHEMA)
            when(self.subprocess).call(['python', 'migrations/%s_%s.py' % (NO_SCHEMA, VER1)]).returns(0)
            
            self.migration.migrate_to(VER1)
            
            expect(self.dataschema.set_actual_schema).to(have_been_called_with(VER1))
        
        with it('log an message'):
            when(self.dataschema).actual_schema().returns(NO_SCHEMA)
            when(self.subprocess).call(['python', 'migrations/%s_%s.py' % (NO_SCHEMA, VER1)]).returns(0)
            
            self.migration.migrate_to(VER1)
        
            expect(self.logger.info).to(have_been_called_with(contain(NO_SCHEMA, VER1)))
            expect(self.logger.info).not_to(have_been_called_with(contain('error')))

        with context('when migration fails'):
            with it('does not  set the actual version'):
                when(self.dataschema).actual_schema().returns(NO_SCHEMA)
                when(self.subprocess).call(['python', 'migrations/%s_%s.py' % (NO_SCHEMA, VER1)]).returns(1)    
                
                self.migration.migrate_to(VER1)
            
                expect(self.dataschema.set_actual_schema).to_not(have_been_called_with(VER1))

            with it('log an error message'):
                when(self.dataschema).actual_schema().returns(NO_SCHEMA)
                when(self.subprocess).call(['python', 'migrations/%s_%s.py' % (NO_SCHEMA, VER1)]).returns(1)    
                
                self.migration.migrate_to(VER1)
            
                expect(self.logger.info).to(have_been_called_with(contain('error', NO_SCHEMA, VER1)))
                