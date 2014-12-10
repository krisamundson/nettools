#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2014 Puppet Labs, Inc.

##
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
#

__author__ = "Kris Amundson"
__copyright__ = "Copyright (C) 2014 Puppet Labs, Inc."
__version__ = "0.1"

import argparse
from jnpr.junos import Device
from jnpr.junos.op.phyport import *
import pprint
import re

def main():

    # Process arguments
    args = process_args()

    # Ignore interface descriptions that match this regex
    # Currently: Ignore descriptions that start with an underscore
    ignore_interface = re.compile(r'^_.*$')

    # Connect to device, get port table, close device
    interfaces = get_interfaces(args) 

    # Iterate over interfaces
    #  - If Admin state is "up" and Operational Link is "down"
    #  - Description is not None 
    #  - Descriptions that do not match the ignore regex
    #  - Build an array of these interfaces
    down_interfaces = []
    for interface in interfaces.items():
        if interface[1][4][1] == 'up' and interface[1][0][1] == 'up': 
            if interface[1][2][1] == None or ignore_interface.match(interface[1][2][1]):
                continue
            else:
                down_interfaces.append(interface[0])

    print down_interfaces

def process_args():
    parser = argparse.ArgumentParser(description='Check interface states on JunOS device.')
    parser.add_argument('--configfile', help='Alternate SSH user config.', required=False, type=str)
    parser.add_argument('--hostname', help='Device FQDN hostname.', required=True, type=str)
    parser.add_argument('--user', help='SSH login name.', required=False, type=str)

    args = parser.parse_args()

    # Return dict of arguments
    return { 'user': args.user, 'hostname': args.hostname, 'configfile': args.configfile }

def get_interfaces(args):
    dev = Device(host=args['hostname'])

    try:
        dev.open()
    except:
        print('Unexpected error with NETCONF connection.  Try `ssh ' + args['hostname'] + '`')
        exit(3)

    interfaces = PhyPortTable(dev).get()
    dev.close()

    return interfaces
    
if __name__ == "__main__":
    main()
