#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2014 Puppet Labs, Inc.
#
# check_junos_int
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
__copyright__ = "Copyright (C) 2014 Puppet Labs, Inc."
__version__ = "0.1"

import argparse
from jnpr.junos import Device
from jnpr.junos.op.phyport import PhyPortTable


def main():

    args = process_args()
    interfaces = get_interfaces(args)
    down_interfaces = check_interfaces(interfaces)

    if down_interfaces:
        # Critical output header
        print('CRITICAL:')
        print('Interface\tAdmin\tLink\tDescription')

        errout = ''
        for each in down_interfaces:
            errout = errout + each[0] + '\t' + each[1] + '\t' + each[2] + \
                '\t' + each[3] + '\n'
        print(errout)

        exit(2)

    else:
        print('OK: Interfaces are up.')
        exit(0)


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


def get_interfaces(args):
    """
    Connect to device over NETCONF protocol and obtain list of interfaces.
    This uses jnpr.junos.op.phyport.PhyPortTable
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

    interfaces = PhyPortTable(dev).get()
    dev.close()

    return interfaces


def check_interfaces(interfaces):
    """
    Iterate over interfaces
        - If Admin state is "up" and Operational Link is "down"
        - Description is not None
        - Descriptions that do not start with '_' (underscore)
        - Return an array of what is left
    """

    down_interfaces = []

    for interface in interfaces:
        if interface.admin == 'up' and interface.oper == 'down':
            if interface.description is None or \
                    interface.description.startswith('_'):
                continue
            else:
                down_interfaces.append([interface.key, interface.admin,
                                        interface.oper, interface.description])

    return down_interfaces


if __name__ == "__main__":
    main()
