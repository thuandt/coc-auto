#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" AutoClick for VirtualBox (Genymotion VMs)
"""

import os
import sys
import virtualbox
from time import sleep

genymotion_vm_name = "Google Nexus 7"


def main():
    vbox = virtualbox.VirtualBox()
    genymotion_vm = vbox.find_machine(genymotion_vm_name)
    genymotion_session = genymotion_vm.create_session()

    while True:
        genymotion_session.console.mouse.put_mouse_event_absolute(360,223,0,0,1)
        genymotion_session.console.mouse.put_mouse_event_absolute(360,223,0,0,0)
        sleep(60)


if __name__ == "__main__":
    try:
        main()
    except:
        sys.exit(1)
