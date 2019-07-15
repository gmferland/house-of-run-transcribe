from pydub import AudioSegment
import argparse
import re
from Audio_Converter import Audio_Converter

parser = argparse.ArgumentParser(description='Transcribe an mp3 file to text!')

parser.add_argument('inputFile', type=str, help='The path to the mp3 file you wish to transcribe')
parser.add_argument('outputFile', type=str, help='The path to the text file that will be output')
parser.add_argument('--pauseDuration', type=int, required=False,
    default=1000, help='Duration in milliseconds to wait before breaking a phrase')
parser.add_argument('--silenceThreshold', type=int, required=False,
    default=-16, help='The level of sound considered to be silent')
parser.add_argument('--deleteInputFile', type=bool, nargs='?', required=False,
    const=True, default=False, help='Whether to delete the initial mp3 file once it has been fully transcribed')

args = parser.parse_args()
inputFile = args.inputFile
outputFile = args.outputFile
pause_duration = args.pauseDuration
silence_threshold = args.silenceThreshold

# convert mp3 file to wav                                                       
sound = AudioSegment.from_mp3(inputFile)
AUDIO_FILE = inputFile.replace('.mp3', '.wav')
sound.export(AUDIO_FILE, format="wav")

converter = Audio_Converter(AUDIO_FILE, outputFile, pause_duration, silence_threshold)
converter.transcribe()
