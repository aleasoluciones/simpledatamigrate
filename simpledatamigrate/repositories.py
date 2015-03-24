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
            if len(schema) == 0:
                return None
            return schema[0][0]

    def set_actual_schema(self, version):
        if self.actual_schema() is None:
            self.insert_actual_schema(version)
        else:
            with self._connection.cursor() as cursor:
                cursor.execute("update schemaVersion set version=(%s);", (version, ))

    def insert_actual_schema(self, version):
        with self._connection.cursor() as cursor:
            cursor.execute("insert into schemaVersion (version) values (%s);", (version, ))
