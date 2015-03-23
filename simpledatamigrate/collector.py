# -*- coding: utf-8 -*-

import os

class MigrationCollector(object):

    def __init__(self, folder):
        self.folder = folder

    def migrations(self):
        return sorted(os.listdir(self.folder + '/'))

