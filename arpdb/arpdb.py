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
from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.op.arp import ArpTable
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# default database file
DBFILE = 'data.db'


def main():

    args = process_args()

    if args['initdb']:
        initdb()

#    arps = get_arp_table(args)
#
#    for x in arps:
#        pprint(x.values())


def process_args():
    """
    Process command arguments.
    Return friendly dict of arguments.
    """

    parser = argparse.ArgumentParser(
        description='Gather ARP tables from routers and store them in a db.')
    parser.add_argument('--hostname',
                        help='Device hostname.', required=False, type=str)
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


def initdb():
    """
    Initialize sqlite3 database.
    """

    Base = declarative_base()

    class Arps(Base):
        __tablename__ = 'arps'
        id = Column(Integer, primary_key=True)
        # ISO Timestamp: 2015-06-29 23:59:59
        timestamp = Column(String(19), nullable=False)
        # L3 Interface: vlan.33 or xe-1/1/1
        interface = Column(String(20), nullable=False)
        # IPv4 Address: 192.158.234.234
        inet = Column(String(15), nullable=False)
        # MAC Address: 54:e0:32:0e:8d:7d
        mac = Column(String(17), nullable=False)

    # If open succeeds, exit with error.
    try:
        open(DBFILE, 'r')
        print('Error: Can not initialize, {} exists'.format(DBFILE))
        exit(1)
    except IOError:
        engine = create_engine('sqlite:///' + DBFILE)
        Base.metadata.create_all(engine)


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
