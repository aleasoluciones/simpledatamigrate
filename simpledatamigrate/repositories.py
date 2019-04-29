# -*- coding: utf-8 -*-


class SchemaVersionRepository(object):

    def __init__(self):
        self._version = None

    def current_schema(self):
        return self._version

    def set_schema_version(self, version):
        self._version = version


class PostgresSchemaVersionRepository(object):

    TABLE_NAME = 'schemaversion'

    def __init__(self, connection):
        self._connection = connection
        self._connection.autocommit = True
        self._create_table_if_not_exists()

    def current_schema(self):
        with self._connection.cursor() as cursor:
            cursor.execute('SELECT version FROM %s', (self.TABLE_NAME, ))
            schema = cursor.fetchall()
            if len(schema) == 0:
                return None
            return schema[0][0]

    def set_schema_version(self, version):
        if self.current_schema() is None:
            self._insert_current_schema(version)
        else:
            with self._connection.cursor() as cursor:
                cursor.execute('UPDATE %s SET version=(%s);', (self.TABLE_NAME, version, ))

    def _insert_current_schema(self, version):
        with self._connection.cursor() as cursor:
            cursor.execute('INSERT INTO %s (version) VALUES (%s);', (self.TABLE_NAME, version, ))


    def _create_table_if_not_exists(self):
        with self._connection.cursor() as cursor:
            cursor.execute('SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)', (self.TABLE_NAME,))
            exists = cursor.fetchone()[0]
            if not exists:
                self._create_schema_version_table()

    def _create_schema_version_table(self):
        with self._connection.cursor() as cursor:
            cursor.execute('CREATE TABLE %s (id SERIAL PRIMARY KEY, version TEXT);', (self.TABLE_NAME, ))


class PostgresDatabaseRepository(object):

    def __init__(self, connection):
        self._connection = connection
        self._connection.autocommit = True

    def create_test_database(self):
        with self._connection.cursor() as cursor:
            cursor.execute('CREATE DATABASE %s;', (self._connection.db_name, ))

    def remove_test_database(self):
        with self._connection.cursor() as cursor:
            cursor.execute('DROP DATABASE IF EXISTS %s;', (self._connection.db_name, ))
