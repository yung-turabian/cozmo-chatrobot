import asyncio
import time
from threading import Timer

import cozmo
from cozmo.util import distance_mm, speed_mmps, degrees
from termcolor import colored, cprint

class VoiceCommands():

    def __init__(self, robot, log=False):
        self.robot = robot
        self.lang_data = None
        self.log = log
    
    def check_charger(self, robot:cozmo.robot.Robot, distance=150, speed=100):
        if robot.is_on_charger:
            if self.log:
                print("I am on the charger. Driving off the charger...")
            robot.drive_off_charger_contacts().wait_for_completed()
            robot.drive_straight(distance_mm(distance), speed_mmps(speed)).wait_for_completed()
            robot.move_lift(-8)
        