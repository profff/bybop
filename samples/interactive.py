#!/usr/bin/env python3

import sys

import code
import readline
import rlcompleter

sys.path.append('../src')

from Bybop_Discovery import Discovery, DeviceID, get_name
import Bybop_Device

print('Searching for devices')

discovery = Discovery(DeviceID.ALL)

discovery.wait_for_change()

devices = discovery.get_devices()

discovery.stop()

if not devices:
    print('Oops ...')
    sys.exit(1)

device = next(iter(devices.values()))

print('Will connect to ' + get_name(device))

d2c_port = 54321
controller_type = "PC"
controller_name = "bybop shell"

drone = Bybop_Device.create_and_connect(
    device, d2c_port, controller_type, controller_name)

if drone is None:
    print('Unable to connect to a product')
    sys.exit(1)

drone.dump_state()

vars = globals().copy()
vars.update(locals())
readline.set_completer(rlcompleter.Completer(vars).complete)
readline.parse_and_bind("tab: complete")
shell = code.InteractiveConsole(vars)

shell.interact()

drone.stop()
