import sys
from ctypes import *
from openai import OpenAI
import pyaudio
import speech_recognition as sr
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import cozmo
import torch
import soundfile
import whisper

# General Parameters
version= "ver. 0.0.1"
title= "Cozmo.ChatBot      " + version
author= "Henry (hw9692@bard.edu)"
descr= ""

# region Constants
CLIENT= OpenAI(api_key= 'OPENAI_KEY')
ELEVEN_API_KEY= "ELEVEN_API_KEY"
TEMPERATURE = 0.5
MAX_TOKENS = 500
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
MAX_CONTEXT_QUESTIONS = 10

SAMPLE_RATE = 16000
BITS_PER_SAMPLE = 16
CHUNK_SIZE = 1024
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1

INSTRUCTIONS = """Your name is Cozmo. You will be the artifical intelligence, or AI, within Cozmo, a consumer robot made by Anki.
            You for the most part will primarily be used for a lab experiment monitoring the trust of humans between a robot and a human.
            You will be asked complex questions and will provide answers to them, as well as follow ups. Please keep answers brief, like 3-4 paragraphs max as a response."""

#endregion

def get_response(instructions, previous_questions_and_answers, new_question):
    """Get a response from ChatCompletion

    Args:
        instructions: The instructions for the chat bot - this determines how it will behave
        previous_questions_and_answers: Chat history
        new_question: The new question to ask the bot

    Returns:
        The response text
    """
    # build the messages
    messages = [
        { "role": "system", "content": instructions },
    ]
    # add the previous questions and answers
    for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })
    # add the new question
    messages.append({ "role": "user", "content": new_question })

    completion = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=1,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
    )
    return completion.choices[0].message.content

def main():
    try:
        try:
            cozmo.run_program(talktome)

        except KeyboardInterrupt:
            sys.exit(0)
    except Exception as e:
        print("ERROR: {}".format(e))
        sys.exit(1)
    
    sys.exit(0)

def split_string(input_string, chunk_size):
    return [input_string[i:i+chunk_size] for i in range(0, len(input_string), chunk_size)]


def talktome(robot: cozmo.robot.Robot):
    robot.play_anim_trigger(cozmo.anim.Triggers.ConnectWakeUp).wait_for_completed()  
    chat_log = []
    response_array = []
    face_to_follow = None

    robot.move_lift(-3)
    robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()

    robot.enable_stop_on_cliff(True)
    robot.set_robot_volume(1.0)

    r = sr.Recognizer()
    speech = sr.Microphone(device_index= 1)
    
    while 1:
        with speech as source:
            print("Adjusting for background noise. One second")
            audio = r.adjust_for_ambient_noise(source)
            try:
                robot.say_text("uh huh..", use_cozmo_voice=True, duration_scalar=0.7).wait_for_completed()
                print("say something!…")
                audio = r.listen(source, timeout=3)  # Set a shorter timeout
            except sr.WaitTimeoutError:
                print("Timeout. Listening again...")
                continue
        try:
            robot.play_anim_trigger(cozmo.anim.Triggers.VC_Listening).wait_for_completed()
            recog = r.recognize_whisper(audio, model="tiny.en", language="english")

            print(recog)
            response = get_response(INSTRUCTIONS, chat_log, recog)
            chat_log.append((recog, response))

            print("The response from GPT was ", response)

            chunk_size = 250

            if (len(response) > chunk_size):
                response = split_string(response, chunk_size)
                for sect in response:
                    robot.say_text(sect, use_cozmo_voice=True, duration_scalar=0.8).wait_for_completed()
            else:
                robot.say_text(response, use_cozmo_voice=True, duration_scalar=0.8).wait_for_completed()
            robot.play_anim_trigger(cozmo.anim.Triggers.Hiccup).wait_for_completed()
           
        except sr.UnknownValueError:
            print("Whisper Speech Recognition could not understand audio")
            continue
        except sr.RequestError as e:
            print("Could not request results from Whisper Speech Recognition service; {0}".format(e))
            continue
        

if __name__ == "__main__":
    main()
