
try:
    import cozmo
    import sys
    import os

except ImportError:
    sys.exit(sys.exit("Some packages are required. Do `pip3 install cozmo` to install."))
    

# https://github.com/c64-dev/Cozmo.AI/blob/master/main.py
# https://github.com/rizal72/Cozmo-Voice-Commands
# https://data.bit-bots.de/cozmo_sdk_doc/cozmosdk.anki.com/docs/generated/cozmo.faces.html
# https://www.cybrosys.com/blog/how-to-create-a-voice-chatbot-using-openai-s-api

# GENERAL PARAMS
version = "ver. 0.0.1"
title = "Cozmo.Lab.Assistant      " + version
author = "By Henry Wandover (hw9692@bard.edu)"
descr = ""

# INITIALIZE SYSTEM
def initCozmo():
