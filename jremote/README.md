# jremote.py

## Description

Manage our Juniper devices.

## Requirements

  * SSH and sudo access to the devices in config.yaml
  * python modules: `pip install fabric`

## hosts.yaml

Hosts are classified in hosts.yaml:

  * **ex**: List of Juniper EX switches.
  * **mx**: List of Juniper MX routers.
  * **srx**: List of Juniper SRX firewalls.

## configure_commands.txt

Commands to run on the remote system in configuration mode,
one command per line.

Typically the last command will be `commit confirmed 5` to
commit changes with a 5 minute auto-rollback.

## Usage

  * [todo]
