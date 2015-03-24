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
        self._create_table_if_not_exists()

    def actual_schema(self):
        with self._connection.cursor() as cursor:
            cursor.execute("select version from schemaVersion")
            schema = cursor.fetchall()
            if len(schema) == 0:
                return None
            return schema[0][0]

    def set_actual_schema(self, version):
        if self.actual_schema() is None:
            self._insert_actual_schema(version)
        else:
            with self._connection.cursor() as cursor:
                cursor.execute("update schemaVersion set version=(%s);", (version, ))

    def _insert_actual_schema(self, version):
        with self._connection.cursor() as cursor:
            cursor.execute("insert into schemaVersion (version) values (%s);", (version, ))


    def _create_table_if_not_exists(self):
        with self._connection.cursor() as cursor:
            cursor.execute("select * from information_schema.tables where table_name=%s", ('schemaVersion',))
            if not bool(cursor.rowcount):
                self._create_schema_version_table()

    def _create_schema_version_table(self):
        with self._connection.cursor() as cursor:
            cursor.execute("CREATE TABLE schemaVersion (id serial primary key, version text);")

