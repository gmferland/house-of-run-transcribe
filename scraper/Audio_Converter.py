import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

class Audio_Converter:
    def __init__(self, inputFileName, outputFileName, silence_min_duration):
        # input file must be in wav format
        self.inputFileName = inputFileName
        self.outputFileName = outputFileName
        self.silence_min_duration = silence_min_duration

    # a function that splits the audio file into chunks 
    # and applies speech recognition 
    def transcribe(self): 
        chunks = self._split_into_chunks(self.inputFileName, self.silence_min_duration)
        indexOfExt = self.outputFileName.find('.')
        outputDirName = 'audio/' + self.outputFileName[:indexOfExt]
        # create a directory to store the audio chunks.
        try:
            os.makedirs(outputDirName)
        except(FileExistsError):
            pass

        # move into the directory to
        # store the audio files.
        os.chdir(outputDirName)

        # create a speech recognition object
        recognizer = sr.Recognizer()

        # create the file that we will write the text to
        with open(self.outputFileName, 'w') as outFile:
            i = 0
            # store chunks as files in directory
            for chunk in chunks:
                # the name of the newly created chunk
                filename = 'chunk' + str(i) + '.wav'
                print('Processing ' + filename)
                self._save_chunk(chunk, filename)
                text = self._listen_to_audio(filename, recognizer)
                if text is not None:
                    # sometimes we can't recognize anything from the audio
                    outFile.write(self._create_phrase(text))
                i += 1

        os.chdir('..')
        print('Finished transcribing ' + self.inputFileName)

    def _split_into_chunks(self, wavFileName, silence_min_duration):
        # open the audio file stored in
        # the local system as a wav file.
        song = AudioSegment.from_wav(wavFileName)

        song = song[:120000]

        chunks = split_on_silence(song,
            # must be silent for at least silence_min_duration.
            # adjust this value based on user requirement.
            # if the speaker stays silent for longer,
            # increase this value. else, decrease it.
            min_silence_len = silence_min_duration,

            # consider it silent if quieter than this threshold
            silence_thresh = -36
        )
        print('Successfully split audio into ' + str(len(chunks)) + ' chunks')

        return chunks

    def _save_chunk(self, chunk, wavFileName):
        # export audio chunk and save it in
        # the current directory.
        print('saving ' + wavFileName)
        # specify the bitrate to be 192 k
        chunk.export(wavFileName, bitrate ='192k', format ='wav')

    def _listen_to_audio(self, inputFilePath, recognizer):
        print('Listening to audio...')
        # recognize the chunk
        with sr.AudioFile(inputFilePath) as source:
            try:
                audio_listened = recognizer.record(source)
                # try converting it to text
                text = recognizer.recognize_google(audio_listened)
                return text
            except sr.UnknownValueError:
                print('Could not recognize word, continuing...')
            except sr.RequestError:
                print('Could not request results. check your internet connection')

    def _create_phrase(self, text):
        text = str(text)
        # capitalize the first word and end with a period
        return text[0].upper() + text[1:] + '. '
