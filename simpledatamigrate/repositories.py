# -*- coding: utf-8 -*-


class SchemaVersionRepository(object):

    def __init__(self):
        self.state = None

    def actual_schema(self):
        return self.state

    def set_actual_schema(self, version):
        self.state = version


class PostgresSchemaVersionRepository(object):

    def __init__(self, connection):
        self._connection = connection
        self._connection.autocommit = True

    def actual_schema(self):
        with self._connection.cursor() as cursor:
            cursor.execute("select version from schemaVersion")
            schema = cursor.fetchall()
            return schema['version']

    def set_actual_schema(self, version):
        with self._connection.cursor() as cursor:
            pass
