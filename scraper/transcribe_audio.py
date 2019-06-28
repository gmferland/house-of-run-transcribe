import speech_recognition as sr
from os import path
from pydub import AudioSegment
import argparse

parser = argparse.ArgumentParser(description='Transcribe an mp3 file to text!')

parser.add_argument('--inputFile', type=str, nargs=1, required=True,
    help='The path to the mp3 file you wish to transcribe')
parser.add_argument('--outputFile', type=str, nargs=1, required=True,
    help='The path to the text file that will be output')
parser.add_argument('--chunkSize', type=int, nargs=1, required=False,
    default=30, help='Duration in seconds of one cycle of transcription')

args = parser.parse_args()
inputFile = args.inputFile
outputFile = args.outputFile
# transcribe the file in shorter pieces
record_duration = args.chunkSize

# convert mp3 file to wav                                                       
sound = AudioSegment.from_mp3(inputFile)
sound.export("./audio/transcript.wav", format="wav")

# transcribe audio file                                                         
AUDIO_FILE = "./audio/transcript.wav"

def parse_google(recognizer, audio):
    with open(outputFile, 'a') as f:
        f.write(recognizer.recognize_google(audio) + '\n')

# use the audio file as the audio source                                        
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    while not source.stream is None:
        try:
            audio = r.record(source, record_duration)
            parse_google(r, audio)
        except sr.UnknownValueError:
            print('Could not recognize word, continuing...')
