#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2015 Puppet Labs, Inc.
#
# check_dns
#
# Provided a list of real DNS server IPs, and anycast IPs, check each of them
# and return status.argparse
#
# Requirements:
#   * dnspython

__author__ = "Kris Amundson"
__copyright__ = "Copyright (C) 2015 Puppet Labs, Inc."
__version__ = "0.1"


import argparse
import socket

import dns.resolver


def main():

    # ... given a unicast and anycast IP...
    # ... and running on a DNS server (print hostname) ...
    # ... output traceroute distance to each IP ...
    # ... check DNS query to those IPs ...
    # ... alert if traceroute is greater than X or lookup fails ...

    args = process_args()

    # DEBUG
    print(args)

#    if down_interfaces:
#        # Critical output header
#        print('CRITICAL:')
#        print('Interface\tAdmin\tLink\tDescription')
#
#        errout = ''
#        for each in down_interfaces:
#            errout = errout + each[0] + '\t' + each[1] + '\t' + each[2] + \
#                '\t' + each[3] + '\n'
#        print(errout)
#
#        exit(2)
#
#    else:
#        print('OK: Interfaces are up.')
#        exit(0)


def process_args():
    """
    Process command arguments.
    Return friendly dict of arguments.
    """

    parser = argparse.ArgumentParser(
        description='Check DNS on anycast and unicast IPs.')
    parser.add_argument('--anycast',
                        help='Anycast IP.', required=True, type=str)
    parser.add_argument('--unicast',
                        help='Unicast IP.', required=True, type=str)
    parser.add_argument('-6', '--ipv6', help='IPv6', required=False,
                        action='store_true')

    args = parser.parse_args()

    # Return dict of arguments
    return {'anycast_ip': args.anycast, 'unicast_ip': args.unicast,
            'inet6': args.ipv6}


def check_ip(address):
    try:
        socket.inet_aton(address)
        ip = True
    except socket.error:
        ip = False

    return ip


if __name__ == "__main__":
    main()
