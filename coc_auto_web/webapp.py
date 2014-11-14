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

urls = ('/','Index')
title = "Web interface for AutoCoC Tools by MrTux"
app = web.application(urls, globals())

f = open("/tmp/coc_status", 'w')
f.write("offline")
f.close()

ngrok_prog = subprocess.Popen("/home/mrtux/app/bin/ngrok start coc", shell=True)

class Index:

    def __init__(self):
        if open("/tmp/coc_status", 'r').readline() == "offline":
            self.control_form_button = web.form.Button('action', html="Start", \
                                                       class_="btn btn-success btn-lg", \
                                                       style="width: 5em;height: 2em;font-size: 70px", \
                                                       id="control_button", value="start")
        elif open("/tmp/coc_status", 'r').readline() == "running":
            self.control_form_button = web.form.Button('action', html="Stop", \
                                                       class_="btn btn-danger btn-lg", \
                                                       style="width: 5em;height: 2em;font-size: 70px", \
                                                       id="control_button", value="stop")


        self.control_form = web.form.Form(self.control_form_button)
        self.render = web.template.render('templates/')

    def GET(self):
        return self.render.index(title, self.control_form)

    def POST(self):
        data = web.input()
        action = data.action
        if action == "start":
            f= open("/tmp/coc_status", 'w')
            f.write("running")
            f.close()
            prog = subprocess.Popen("python /home/mrtux/app/coc-auto/keepalive.py", shell=True)
        elif action == "stop":
            file_status = open("/tmp/coc_status", 'r').readline()
            if file_status == "running":
                prog = subprocess.Popen("pkill -f keepalive.py", shell=True)
                f= open("/tmp/coc_status", 'w')
                f.write("offline")
                f.close()

        return web.redirect("/")

if __name__ == "__main__":
    app.internalerror = web.debugerror
    app.run()
