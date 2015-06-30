#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2015 Puppet Labs, Inc.
#
# arp_table
#
# The goal with this check script is to care about interfaces with
# descriptions, ignoring descriptions that start with a defined prefix.
# All it takes to monitor an important interface is to give it a description.
# If this interface goes up/down, this script will return CRITICAL and the
# list of ports in this state.
#
# Requirements:
#   * py-junos-eznc module
#   * Enabling the NETCONF protocol on JunOS devices.

__author__ = "Kris Amundson"
__copyright__ = "Copyright (C) 2015 Puppet Labs, Inc."
__version__ = "0.1"

import argparse
from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.op.arp import ArpTable


def main():

    args = process_args()
    arps = get_arp_table(args)

    for x in arps:
        pprint(x.values())


def process_args():
    """
    Process command arguments.
    Return friendly dict of arguments.
    """

    parser = argparse.ArgumentParser(
        description='Check interface states on JunOS device.')
    parser.add_argument('--hostname',
                        help='Device hostname.', required=True, type=str)
    parser.add_argument('--sshconfig',
                        help='Alternate SSH config.', required=False, type=str)
    parser.add_argument('--sshkey',
                        help='Path to SSH private key.',
                        required=False, type=str)
    parser.add_argument('--user',
                        help='SSH login name.', required=False, type=str)

    args = parser.parse_args()

    # Return dict of arguments
    return {'hostname': args.hostname, 'sshconfig': args.sshconfig,
            'sshkey': args.sshkey, 'user': args.user}


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
