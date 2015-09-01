#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""JRemote

Fabric tasks for running operational commands and applying
configuration to Juniper JunOS devices.

"""

from __future__ import print_function
from fabric.api import env, run, task
import os
import sys
import yaml


__author__ = "Kris Amundson"
__copyright__ = "Copyright (C) 2015 Puppet Labs, Inc."
__version__ = "0.1"


def junos_load_hosts():
    """Load hosts from YAML config file in project dir.

    Returns: None
    """
    hosts_loc = '{}/hosts.yaml'.format(os.path.dirname(__file__))
    with open(hosts_loc, 'r') as config_file:
        hosts = yaml.load(config_file)

    env.roledefs = {
        'junos_all': hosts['ex'] + hosts['mx'] + hosts['srx'],
        'junos_ex': hosts['ex'],
        'junos_mx': hosts['mx'],
        'junos_srx': hosts['srx'],
    }

    return None


junos_load_hosts()


def junos_common():
    """JunOS-specific for fabric.

    Return: None
    """
    env.use_shell = False
    return None


##
# Tasks
#
@task
def junos_commit(comment='Commited by fabric.api.'):
    junos_common()
    run('configure; commit comment "{}"'.format(comment))


@task
def junos_compare():
    junos_common()
    run('configure; show | compare')


@task
def junos_rollback(level='0'):
    junos_common()
    """JunOS Rollback Command"""
    run('configure; rollback {}'.format(level))


@task
def junos_configure_commands():
    junos_common()
    """Run commands from file."""

    commands = 'configure'

    commands_loc = '{}/commands.txt'.format(os.path.dirname(__file__))
    with open(commands_loc, 'r') as commands_file:
        commands_from_file = commands_file.read().splitlines()

    for cmd in commands_from_file:
        commands = '{}; {}'.format(commands, cmd)

    run(commands)


@task
def junos_show_ntp_associations():
    junos_common()
    run('show ntp associations')


@task
def junos_show_system_uptime():
    run('show system uptime')


def main():
    print('Do not run me directly. Use the `fab` tool.')
    sys.exit(1)

if __name__ == "__main__":
    main()