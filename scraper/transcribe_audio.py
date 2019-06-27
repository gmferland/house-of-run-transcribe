import speech_recognition as sr
from os import path
from pydub import AudioSegment

# convert mp3 file to wav                                                       
sound = AudioSegment.from_mp3("./audio/Episode492.mp3")
sound.export("./audio/transcript.wav", format="wav")


# transcribe audio file                                                         
AUDIO_FILE = "./audio/transcript.wav"

def handle_parsed_phrase(recognizer, audio):
    with open('./transcriptions/Episode492.txt', 'a') as f:
        f.write(recognizer.recognize_google(audio) + '\n')

# use the audio file as the audio source                                        
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
      while not source.stream is None:
        audio = r.listen(source, 1)
        handle_parsed_phrase(r, audio)
