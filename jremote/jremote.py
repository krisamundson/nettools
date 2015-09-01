#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""JRemote

Fabric tasks for running operational commands and applying
configuration to Juniper JunOS devices.

"""

from __future__ import print_function
from fabric.api import env, roles, run, task
import os
import sys
import yaml


__author__ = "Kris Amundson"
__copyright__ = "Copyright (C) 2015 Puppet Labs, Inc."
__version__ = "0.1"


# Needed for JunOS
env.use_shell = False


def load_junos_hosts():
    """Load hosts from YAML config file in project dir.

    Returns: None
    """
    hosts_loc = '{}/hosts.yaml'.format(os.path.dirname(__file__))
    with open(hosts_loc, 'r') as config_file:
        hosts = yaml.load(config_file)

    env.roledefs = {
        'junos_all': hosts['junos_ex'] + hosts['junos_mx'] + hosts['junos_srx'],
        'junos_ex': hosts['junos_ex'],
        'junos_mx': hosts['junos_mx'],
        'junos_srx': hosts['junos_srx'],
    }

    return None

load_junos_hosts()


##
# Tasks
#
@task
def commit(comment='Commited by fabric.api.'):
    run('configure; commit comment "{}"'.format(comment))


@task
def compare():
    run('configure; show | compare')


@task
def rollback(level='0'):
    """JunOS Rollback Command"""
    run('configure; rollback {}'.format(level))


@task
def configure_commands():
    """Run commands from file."""

    commands = 'configure'

    commands_loc = '{}/commands.txt'.format(os.path.dirname(__file__))
    with open(commands_loc, 'r') as commands_file:
        commands_from_file = commands_file.read().splitlines()

    for cmd in commands_from_file:
        commands = '{}; {}'.format(commands, cmd)

    run(commands)


@task
def show_ntp():
    run('show ntp associations')


@task
def show_system_uptime():
    run('show system uptime')


def main():
    print('Do not run me directly. Use the `fab` tool.')
    sys.exit(1)

if __name__ == "__main__":
    main()