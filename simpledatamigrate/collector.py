import os

class MigrationCollector(object):

    PYTHON_EXTENSION = '.py'

    def __init__(self, folder):
        self.folder = folder

    def migrations(self):
        return [self._with_relative_path(migration) for migration in sorted(os.listdir(self.folder + '/')) if self._is_python_script(migration)]

    def _is_python_script(self, migration):
        return migration.endswith(self.PYTHON_EXTENSION)

    def _with_relative_path(self, migration):
        return os.path.join(os.path.relpath(self.folder), migration)
