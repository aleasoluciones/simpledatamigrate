#!/usr/bin/env python

from simpledatamigrate import factory

def main():
    factory.create_postgres_migrator().migrate()

if __name__ == '__main__':
    main()
