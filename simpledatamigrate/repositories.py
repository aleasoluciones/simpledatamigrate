# -*- coding: utf-8 -*-


class SchemaVersionRepository(object):

    def __init__(self):
        self.state = None

    def actual_schema(self):
        return self.state

    def set_actual_schema(self, version):
        self.state = version


class PostgresSchemaVersionRepository(object):

    TABLE_NAME = 'schemaversion'

    def __init__(self, connection):
        self._connection = connection
        self._connection.autocommit = True
        self._create_table_if_not_exists()

    def actual_schema(self):
        with self._connection.cursor() as cursor:
            cursor.execute('select version from {table_name}'.format(table_name=self.TABLE_NAME))
            schema = cursor.fetchall()
            if len(schema) == 0:
                return None
            return schema[0][0]

    def set_actual_schema(self, version):
        if self.actual_schema() is None:
            self._insert_actual_schema(version)
        else:
            with self._connection.cursor() as cursor:
                cursor.execute('update {table_name} set version=(%s);'.format(table_name=self.TABLE_NAME), (version, ))

    def _insert_actual_schema(self, version):
        with self._connection.cursor() as cursor:
            cursor.execute('insert into {table_name} (version) values (%s);'.format(table_name=self.TABLE_NAME), (version, ))


    def _create_table_if_not_exists(self):
        with self._connection.cursor() as cursor:
            cursor.execute('select exists(select * from information_schema.tables where table_name=%s)', (self.TABLE_NAME,))
            exists = cursor.fetchone()[0]
            if not exists:
                self._create_schema_version_table()

    def _create_schema_version_table(self):
        with self._connection.cursor() as cursor:
            cursor.execute('CREATE TABLE {table_name} (id serial primary key, version text);'.format(table_name=self.TABLE_NAME))

