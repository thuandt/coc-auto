#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Web control interface for AutoCoC-Tools


import os
import sys
import web
import signal
import virtualbox
import subprocess
from time import sleep

urls = ('/', 'Index')
title = "Web interface for AutoCoC Tools by MrTux"
app = web.application(urls, globals())

coc_status = "/tmp/coc_status"
kill_script = "pkill -f keepalive.py"
keepalive_script = "python /home/mrtux/app/coc-auto/keepalive.py"
webpy_templates = "/home/mrtux/app/coc-auto/templates/"

start_button = web.form.Button('action', html="Start",
                               class_="btn btn-success btn-lg",
                               style="width: 5em;height: 2em;font-size: 70px",
                               id="control_button", value="start")

stop_button = web.form.Button('action', html="Stop",
                              class_="btn btn-danger btn-lg",
                              style="width: 5em;height: 2em;font-size: 70px",
                              id="control_button", value="stop")

f = open(coc_status, 'w')
f.write("offline")
f.close()


class Index:

    def __init__(self):
        if open(coc_status, 'r').readline() == "offline":
            self.control_form = web.form.Form(start_button)
        elif open(coc_status, 'r').readline() == "running":
            self.control_form = web.form.Form(stop_button)
        self.render = web.template.render(webpy_templates)

    def GET(self):
        return self.render.index(title, self.control_form)

    def POST(self):
        data = web.input()
        action = data.action
        if action == "start":
            f = open(coc_status, 'w')
            f.write("running")
            f.close()
            subprocess.Popen(keepalive_script, shell=True)
        elif action == "stop":
            file_status = open(coc_status, 'r').readline()
            if file_status == "running":
                subprocess.Popen(kill_script, shell=True)
                f = open(coc_status, 'w')
                f.write("offline")
                f.close()

        return web.redirect("/")

if __name__ == "__main__":
    app.internalerror = web.debugerror
    app.run()
