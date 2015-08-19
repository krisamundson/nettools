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


env.hosts = [
    'pdx-oob.ops.puppetlabs.net',
    'pix-jj09c-r1.ops.puppetlabs.net'
    ]
env.use_shell = False

def commit(comment='Commited by fabric.api.'):
    run('commit comment "{}"'.format(comment))


def compare():
    run('configure; show | compare')


def configure_ntp():
    configure_cmds = [
        'delete system ntp',
        'set system ntp boot-server 10.32.22.9',
        'set system ntp server 10.32.22.9 version 4',
        'set system ntp server 10.0.22.10 version 4',
        'set system ntp server 10.32.44.11 version 4',
        'set system ntp server 10.0.22.11 version 4',
        ]

    commands = 'configure'

    for configure_cmd in configure_cmds:
        commands = '{}; {}'.format(commands, configure_cmd)

    run(commands)

def hosts_from_yaml():

def rollback(level='0'):
    run('configure; rollback {}'.format(level))


def main():
    """Begins enrollment."""
    tasks.execute(configure_ntp)
    disconnect_all()


if __name__ == "__main__":
    main()