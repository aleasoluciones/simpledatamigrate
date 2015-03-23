# -*- coding: utf-8 -*-

import os

class MigrationCollector(object):

    def __init__(self, folder):
        self.folder = folder

    def migrations(self):
        return [self._with_relative_path(migration) for migration in sorted(os.listdir(self.folder + '/'))]

    def _with_relative_path(self, migration):
        return os.path.join(os.path.relpath(self.folder), migration)


