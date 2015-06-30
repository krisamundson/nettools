#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2015 Puppet Labs, Inc.
#
# arpdb
#
# Gather the arp tables from L3 devices, timestamp them and store them in an
# sqlite3 db.
#
# Requirements:
#   * sqlalchemy module
#   * py-junos-eznc module
#   * Enabling the NETCONF protocol on JunOS devices.

__author__ = "Kris Amundson"
__copyright__ = "Copyright (C) 2015 Puppet Labs, Inc."
__version__ = "0.1"

import argparse
import datetime
from jnpr.junos import Device
from jnpr.junos.op.arp import ArpTable
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
        interface = peewee.CharField()
        inet = peewee.CharField()
        mac = peewee.CharField()

        class Meta:
            database = db

    if args['initdb']:
        db.create_tables([Arp])

    # Using NETCONF, obtain the arp table.
    arps = get_arp_table(args)

    for arp_entry in arps:
        Arp.create(hostname=args['hostname'],
                   interface=arp_entry.values()[0],
                   inet=arp_entry.values()[1],
                   mac=arp_entry.values()[2])

    db.close()

def process_args():
    """
    Process command arguments.
    Return friendly dict of arguments.
    """

    parser = argparse.ArgumentParser(
        description='Gather ARP tables from routers and store them in a db.')
    parser.add_argument('--hostname',
                        help='Device hostname.', required=True, type=str)
    parser.add_argument('--sshconfig',
                        help='Alternate SSH config.', required=False, type=str)
    parser.add_argument('--sshkey',
                        help='Path to SSH private key.',
                        required=False, type=str)
    parser.add_argument('--user',
                        help='SSH login name.', required=False, type=str)
    parser.add_argument('--initdb',
                        help='Initialize sqlite3 db.', required=False,
                        action='store_true')

    args = parser.parse_args()

    # Return dict of arguments
    return {'hostname': args.hostname, 'sshconfig': args.sshconfig,
            'sshkey': args.sshkey, 'user': args.user, 'initdb': args.initdb}


def get_arp_table(args):
    """
    Connect to device over NETCONF protocol and obtain arp table.
    This uses jnpr.junos.op.arp.ArpTable
    """

    dev = Device(host=args['hostname'], user=args['user'],
                 ssh_private_key_file=args['sshkey'],
                 ssh_config=args['sshconfig'])

    try:
        dev.open()
    except:
        print('Unexpected error with NETCONF connection.  Try `ssh ' +
              args['hostname'] + '`')
        exit(3)

    arps = ArpTable(dev).get()
    dev.close()

    return arps


if __name__ == "__main__":
    main()
