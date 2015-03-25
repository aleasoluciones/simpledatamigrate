#!/usr/bin/env python

from simpledatamigrate import factory
import argparse

def main():

    args = _parse_arguments()
    migrator = factory.create_postgres_migrator()

    migrator.migrate_to(args.version)

def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='store', required=True, help="set current schema version")
    return parser.parse_args()

if __name__ == '__main__':
    main()
