#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2015 Puppet Labs, Inc.
#
# searcharp
#
# Search ARP entries in sqlite3 db.
#
# Requirements:
#   * peewee module

__author__ = "Kris Amundson"
__copyright__ = "Copyright (C) 2015 Puppet Labs, Inc."
__version__ = "0.1"

import argparse
import datetime

import peewee

# default database file
DB = 'data.db'


def main():

    args = process_args()

    # Define and open sqlite3 database
    db = peewee.SqliteDatabase(DB)
    db.connect()

    class Arp(peewee.Model):
        """
        Data model for the Arp database.
        """
        timestamp = peewee.DateTimeField(default=datetime.datetime.now)
        hostname = peewee.CharField()
        inet = peewee.CharField()
        mac = peewee.CharField()
        interface = peewee.CharField()

        class Meta:
            database = db

    if args['inet']:
        query = Arp.select().where(Arp.inet == args['inet'])
    elif args['mac']:
        query = Arp.select().where(Arp.mac == args['mac'])

    for item in query:
        print('{}, {}, {}, {}, {}'.format(item.timestamp, item.hostname,
                                          item.inet, item.mac, item.interface))

    db.close()


def process_args():
    """
    Process command arguments.
    Return friendly dict of arguments.
    """

    parser = argparse.ArgumentParser(
        description='Search ARP tables from historical db.')
    parser.add_argument('--inet',
                        help='IPv4 Address.', required=False, type=str)
    parser.add_argument('--mac',
                        help='MAC Address.', required=False, type=str)

    args = parser.parse_args()

    # Return dict of arguments
    return {'inet': args.inet, 'mac': args.mac}


if __name__ == "__main__":
    main()
