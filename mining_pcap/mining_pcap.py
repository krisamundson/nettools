#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2015 Puppet Labs, Inc.
#
# mining_pcap
#
# Functions for mining PCAP files.
#
# Requirements:
#   * scapy module
#   * dnspython(dns) module

__author__ = "Kris Amundson"
__copyright__ = "Copyright (C) 2015 Puppet Labs, Inc."
__version__ = "0.1"

from scapy.all import rdpcap
from dns import resolver, reversename

pkts = rdpcap("dns.pcap")

src_hosts = []
for pkt in pkts:
    src_hosts.append(pkt.sprintf("%IP.src%"))

# remove corrupt last entry
src_hosts.pop()

# sort and uniq
hosts = sorted(set(src_hosts))

# convert to hostnames
for host in hosts:
    host_ptr = reversename.from_address(host)

    try:
        answers = resolver.query(host_ptr, 'PTR')
        for rdata in answers:
            print rdata
    except:
        continue
