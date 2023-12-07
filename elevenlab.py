
 from elevenlabs import generate, play, stream, save
        audio = generate(
            text= response,
            api_key= ELEVEN_API_KEY,
            voice= "Clyde",
            model= "eleven_turbo_v2",
            stream= True
        )

        stream(audio)

def record_audio(filename, duration= 3):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=AUDIO_FORMAT, channels=CHANNELS,
                        rate=SAMPLE_RATE, input=True,
                        frames_per_buffer=CHUNK_SIZE)

    print("Recording...")

    frames = []

    for _ in range(0, int(SAMPLE_RATE / CHUNK_SIZE * duration)):
        data = stream.read(CHUNK_SIZE)
        frames.append(data)

    print("Finished recording")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(AUDIO_FORMAT))
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b''.join(frames))

def transcribe_audio(filename):
    
    with open(filename, "rb") as audio_file:
        transcript = CLIENT.audio.transcriptions.create(
            model= "whisper-1", 
            file= audio_file,
            response_format="text")
        return transcript
    
        #temp = tempfile.mktemp('.wav')
    #record_audio(temp)
    #transcription = transcribe_audio(temp)
    #print("Transcription:", transcription)