import openai
import asyncio
import azure.cognitiveservices.speech as spechsdk
import speech_recognition as sr

openai.api_key = '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'


chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)