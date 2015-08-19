#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""JRemote

See README.md

"""

from __future__ import print_function
from fabric import tasks
from fabric.api import run
from fabric.api import env
from fabric.network import disconnect_all
import os

__author__ = "Kris Amundson"
__copyright__ = "Copyright (C) 2015 Puppet Labs, Inc."
__version__ = "0.1"


env.hosts = [ 'pdx-oob.ops.puppetlabs.net']

def uptime():
    run('show uptime')

def main():
    """Begins enrollment."""
    uptime()
    disconnect_all

if __name__ == "__main__":
    main()