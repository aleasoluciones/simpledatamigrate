#!/usr/bin/env python

from simpledatamigrate import factory

def main():
    factory.create_test_postgres_migrator().test_migrate()

if __name__ == '__main__':
    main()
