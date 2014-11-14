#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Clash of Clans Auto Tool for Genymotion (VirtualBox Android VM)
"""

import os
import sys
import virtualbox
import subprocess
import cv2.cv as cv
import tesseract
import PIL.ImageOps as ImageOps
from time import sleep
from PIL import Image

# Genymotion Android VM name
genymotion_vm_name = "COC"

menu_text = """Choose function?
1. Keep Alive
2. Auto Search
3. Quit
"""

vbox = virtualbox.VirtualBox()
genymotion_vm = vbox.find_machine(genymotion_vm_name)
genymotion_session = genymotion_vm.create_session()

def keep_alive():
    while True:
        genymotion_session.console.mouse.put_mouse_event_absolute(360,233,0,0,0)
        genymotion_session.console.mouse.put_mouse_event_absolute(360,233,0,0,1)
        genymotion_session.console.mouse.put_mouse_event_absolute(360,233,0,0,0)
        sleep(90)


def auto_search():
    # click search button
    genymotion_session.console.mouse.put_mouse_event_absolute(660,290,0,0,0)
    genymotion_session.console.mouse.put_mouse_event_absolute(660,290,0,0,1)
    genymotion_session.console.mouse.put_mouse_event_absolute(660,290,0,0,0)
    sleep(10)

    # processing
    subprocess.call("adb shell screencap -p /sdcard/screen.png", shell=True)
    subprocess.call("adb pull /sdcard/screen.png /tmp/screen.png", shell=True)
    im = Image.open("/tmp/screen.png")
    #box = (60, 80, 165, 180)
    #box = (53, 72, 140, 165)
    box = (57, 75, 140, 138)
    loot = im.crop(box).convert('L')
    loot = ImageOps.invert(loot)
    loot.save("/tmp/loot.png", "png")

    api = tesseract.TessBaseAPI()
    api.Init("/home/mrtux/app/bin/", "coc",tesseract.OEM_DEFAULT)
    api.SetVariable("tessedit_char_whitelist", "0123456789")
    api.SetPageSegMode(tesseract.PSM_AUTO)

    image = cv.LoadImage("/tmp/loot.png", cv.CV_LOAD_IMAGE_UNCHANGED)
    tesseract.SetCvImage(image,api)
    text = api.GetUTF8Text()
    conf = api.MeanTextConf()
    total_loot = text.splitlines()

    gold_loot, elixir_loot = total_loot[0:2]
    gold_loot_text_element = gold_loot.split(" ")
    elixir_loot_text_element = elixir_loot.split(" ")

    for i in range(len(gold_loot_text_element)):
        if len(gold_loot_text_element[i]) > 3:
            gold_loot_text_element[i] = gold_loot_text_element[i][1:]

    for i in range(len(elixir_loot_text_element)):
        if len(elixir_loot_text_element[i]) > 3:
            elixir_loot_text_element[i] = elixir_loot_text_element[i][1:]

    gold_expr = gold_loot.find(" ") == 3 and int(gold_loot_text_element[0]) >= 200
    elixir_expr = elixir_loot.find(" ") == 3 and int(elixir_loot_text_element[0]) >= 200

    print gold_loot
    print gold_loot_text_element
    print elixir_loot
    print elixir_loot_text_element

    if gold_expr and elixir_expr:
        subprocess.call("mplayer /home/mrtux/app/bin/gun.mp3", shell=True)
        api.End()
        return True

    return False

if __name__ == "__main__":
    try:
        while True:
            print menu_text
            answer = raw_input("Your choice: ")
            if answer == "1":
                try:
                    keep_alive()
                except:
                    pass
            elif answer == "2":
                try:
                    while auto_search() is False:
                        pass
                except:
                    pass
            elif answer == "3":
                sys.exit(0)
    except:
        sys.exit(1)
