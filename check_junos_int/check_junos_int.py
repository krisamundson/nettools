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
from jnpr.junos.op.phyport import *
import pprint
import re

def main():

    args = process_args()
    interfaces = get_interfaces(args) 
    down_interface = check_interfaces(interfaces)

    if down_interface:    
        # Critical output header
        print('CRITICAL:')
        print('Interface\tAdmin\tLink\tDescription')

        errout = ''
        for each in down_interface:
            errout = errout + each[0] + '\t' + each[1] + '\t' + each[2] + '\t' + each[3] + '\n'
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

    parser = argparse.ArgumentParser(description='Check interface states on JunOS device.')
    parser.add_argument('--configfile', help='Alternate SSH user config.', required=False, type=str)
    parser.add_argument('--hostname', help='Device hostname.', required=True, type=str)
    parser.add_argument('--user', help='SSH login name.', required=False, type=str)

    args = parser.parse_args()

    # Return dict of arguments
    return { 'user': args.user, 'hostname': args.hostname, 'configfile': args.configfile }

def get_interfaces(args):
    """
    Connect to device over NETCONF protocol and obtain list of interfaces.
    This uses jnpr.junos.op.phyport.PhyPortTable
    """

    dev = Device(host=args['hostname'])

    try:
        dev.open()
    except:
        print('Unexpected error with NETCONF connection.  Try `ssh ' + args['hostname'] + '`')
        exit(3)

    interfaces = PhyPortTable(dev).get()
    dev.close()

    return interfaces

def check_interfaces(interfaces):
    """
    Iterate over interfaces
        - If Admin state is "up" and Operational Link is "down"
        - Description is not None 
        - Descriptions that do not match the ignore regex
        - Return an array of what is left
    """

    # Ignore interface descriptions that match this regex
    # Currently: Ignore descriptions that start with an underscore
    ignore_interface = re.compile(r'^_.*$')

    down_interface = []

    for interface in interfaces:
        if interface.admin == 'up' and interface.oper == 'down': 
            if interface.description == None or ignore_interface.match(interface.description):
                continue
            else:
                down_interface.append([interface.key,interface.admin,interface.oper,interface.description])

    return down_interface
    
if __name__ == "__main__":
    main()
