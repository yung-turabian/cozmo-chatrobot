#region IMPORTS
import sys
import os
import asyncio
import operator
import glob
import json
import pkg_resources

import cozmo

from termcolor import colored, cprint
from pynput.keyboard import Key, Listener
import speech_recognition as sr

import voice_commands
#endregion

#region VARS
version = "0.0.1"
title = "Cozmo (The R-Lab Assistant) - Version " + version
author = " - HW & YK"
log = False
wait_for_shift = True
lang = "en"
lang_data = None
commands_activate = ["cozmo", "robot", "cosmo", "cosimo", "cosma", "kosmos"]
vc = None
languages = []
#endregion


def main():
    parese_args()
    clearScreen = os.system('cls' if os.name == 'nt' else 'clear')
    cprint(title, "green", attrs=['bold'], end='')
    cprint(author, "cyan")
    cozmo.robot.Robot.drive_off_charger_on_connect = False
    


    try:
        cozmo.run_program(run)
        #cozmo.run_program(run, use_viewer=True, force_viewer_on_top=True)
    except SystemExit as e:
        print('exception = "%s"' % e)
        #ONLY FOR TESTING PURPOSES
        cprint('\nGoing on without Cozmo: for testing purposes only!', 'red')
        run(None)

def run(robot: cozmo.robot.Robot):

    global vc

    vc = voice_commands.VoiceCommands(robot,log)

    def on_press(key):
        print('{0} pressed'.format(key))
        if key == Key.shift_l or key == Key.shift_r:
            listen(robot)
    
    def on_release(key):
        print('{0} release'.format(key))
        if key == Key.shift_l or key == Key.shift_r:
            pass

    if robot:
        vc.check_charger(robot)
        robot.play_anim("anim_cozmosays_getout_short_01")
    
    try:
        loadjsons()
        set_data()
        printSupportedCommands()
        prompt()

        if wait_for_shift:
            with Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()
        else:
            while 1:
                listen(robot)

    except KeyboardInterrupt:
        print("")
        cprint("Exit requested by user", "yellow")


def loadjsons():

def listen(robot: cozmo.robot.Robot):

    cprint("wait...")


    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.pause_threshold = 0.8
        recognizer.dynamic_energy_threshold = False
        recognizer.adjust_for_ambient_noise(source)
        recognized = None

'''
ALLOWS THE PASSAGE OF ARGS: -V -W -L

-V : print version and exit
-N : enable deprecated continuos listening mode
-L : enable verbose logging
'''
def parese_args():
    global wait_for_shift, log
    if "--version" in sys.argv or "-V" in sys.argv:
        print(version)
        sys.exit()
    if "--no-wait" in sys.argv or "-W" in sys.argv:
        wait_for_shift = False
    if "--log" in sys.argv or "-L" in sys.argv:
        log = True

    if log:
        print ('Arguments list:', str(sys.argv[1:]))

def prompt(id = 1):
    d = 1

def checkBattery(robot: cozmo.robot.Robot):
    if (robot.battery_voltage <= 3.5):
        color = "red"
    else:
        color = "yellow"
    cprint("BATTERY LEVEL(RED=LOW): %f" % robot.battery_voltage + "v", color)

def flash_backpack(robot: cozmo.robot.Robot, flag):
    robot.set_all_backpack_lights(cozmo.lights.green_light.flash() if flag else cozmo.lights.off_light)









'''
ENTRY POINT
'''
if __name__ == "__main__":
    main()