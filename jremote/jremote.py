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
import sys
import yaml

__author__ = "Kris Amundson"
__copyright__ = "Copyright (C) 2015 Puppet Labs, Inc."
__version__ = "0.1"


# Needed for JunOS
env.use_shell = False


def commit(comment='Commited by fabric.api.'):
    run('configure; commit comment "{}"'.format(comment))


def compare():
    run('configure; show | compare')


def hosts_from_yaml():
    pass


def rollback(level='0'):
    """JunOS Rollback Command"""
    run('configure; rollback {}'.format(level))


def configure_commands():
    """Run commands from file."""

    commands = 'configure'

    commands_loc = '{}/commands.txt'.format(os.path.dirname(__file__))
    with open(commands_loc, 'r') as commands_file:
        commands_from_file = commands_file.read().splitlines()

    for cmd in commands_from_file:
        commands = '{}; {}'.format(commands, cmd)

    run(commands)


def show_ntp():
    run('show ntp associations')

def main():
    """[todo]"""

    hosts_loc = '{}/hosts.yaml'.format(os.path.dirname(__file__))
    with open(hosts_loc, 'r') as config_file:
        hosts = yaml.load(config_file)

    env.hosts = hosts['srx'] + hosts['switches'] + hosts['routers']

    tasks.execute(show_ntp)
    disconnect_all()


if __name__ == "__main__":
    main()