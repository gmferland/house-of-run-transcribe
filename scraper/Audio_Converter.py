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

        # create a directory to store the audio chunks.
        try:
            os.mkdir('audio_chunks')
        except(FileExistsError):
            pass

        # move into the directory to
        # store the audio files.
        os.chdir('audio_chunks')

        # create a speech recognition object
        recognizer = sr.Recognizer()

        i = 0
        # create the file that we will write the text to
        with open(self.outputFileName, 'w') as outFile:
            # process each chunk
            for chunk in chunks:
                # the name of the newly created chunk
                filename = 'chunk' + str(i) + '.wav'
                print('Processing ' + filename)
                self._process_chunk(chunk, filename)
                text = self._listen_to_audio(filename, recognizer)
                outFile.write(text + '. ')
                i += 1

        os.chdir('..')
        print('Finished transcribing ' + self.inputFileName)

    def _split_into_chunks(self, wavFileName, silence_min_duration):
        # open the audio file stored in
        # the local system as a wav file.
        song = AudioSegment.from_wav(wavFileName)

        # split track where silence is 0.5 seconds
        # or more and get chunks
        chunks = split_on_silence(song,
            # must be silent for at least 0.5 seconds
            # or 500 ms. adjust this value based on user
            # requirement. if the speaker stays silent for
            # longer, increase this value. else, decrease it.
            min_silence_len = silence_min_duration,

            # consider it silent if quieter than -16 dBFS
            # adjust this per requirement
            silence_thresh = -16
        )

        return chunks

    def _process_chunk(self, chunk, wavFileName):
        # Create 0.5 seconds silence chunk
        chunk_silent = AudioSegment.silent(duration = 10)
        # add 0.5 sec silence to beginning and
        # end of audio chunk. This is done so that
        # it doesn't seem abruptly sliced.
        audio_chunk = chunk_silent + chunk + chunk_silent
        # export audio chunk and save it in
        # the current directory.
        print('saving' + wavFileName)
        # specify the bitrate to be 192 k
        audio_chunk.export(wavFileName, bitrate ='192k', format ='wav')

    def _listen_to_audio(self, inputFilePath, recognizer):
        print('Listening to audio...')
        # recognize the chunk
        with sr.AudioFile(inputFilePath) as source:
            try:
                recognizer.adjust_for_ambient_noise(source)
                audio_listened = recognizer.record(source)
                # try converting it to text
                text = recognizer.recognize_google(audio_listened)
                return text
            except sr.UnknownValueError:
                print('Could not recognize word, continuing...')
            except sr.RequestError:
                print('Could not request results. check your internet connection')
