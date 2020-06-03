#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the streaming API.

NOTE: This module requires the additional dependency `pyaudio`. To install
using pip:

    pip install pyaudio

Example usage:
    python transcribe_streaming_mic.py
"""

# [START import_libraries]
from __future__ import division

import re
import sys
from urllib.request import urlopen
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
import queue
import ContextAnalysis
import time
from ListenAndRepeat import *
from konlpy.tag import Komoran

# Audio recording parameters
RATE = 44100
CHUNK = int(RATE / 10)  # 100ms
lod=0

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk
        self.host = "161.122.208.9:8080"
        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True
        self.Soundhoststr = 'http://' + self.host + '/audio.wav'
        self.Soundstream = urlopen(self.Soundhoststr)
    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True,
            stream_callback=self._fill_buffer,
        )
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        #Continuously collect data from the audio stream, into the buffer.
        global lod
        #print(lod)
        if lod<0:
            if self._buff.full():
                self._buff.get(block=False)
            self.Soundstream.read(8192)
        else:
            self._buff.put(self.Soundstream.read(8192))
        #self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)
# [END audio_stream]
kor=Komoran()
ca=ContextAnalysis.ContextAnalysis(kor)
d = ListenAndRepeat()
num_chars_printed = 0

def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    #print("razarus")
    timetor=True
    global lod
    startt = time.time()

    for response in responses:#when you talk, then start at first
        if not response.results:
            print('or is you?')
            continue
        if lod<0:
            continue
        if timetor:
            endt = time.time()
            t = endt - startt
            print(t)
            if t > 5:
                timetor = False
        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            print('is you?')
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' #* (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()
            print('not me?')

            num_chars_printed = len(transcript)

        else:
            print(transcript)
            #print(type(transcript + overwrite_chars))
            #pos = lex.pos(transcript + overwrite_chars)
            #print("Model :" + str(pos))
            #for i in range(0,len(pos)):
                #print(pos[i][0],model.most_similar(pos[i][0]))
            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            #r.makeAct_dict('sad',transcript)
            #r.Robot_nextSpeak(transcript)
            user_index=ca.anaysisUserStrLevel(transcript)
            ca.predictLevel(ca.prevLevel,user_index)
            ca.wbUtil.printall()
            print('history',ca.history)
            str=ca.makeSentence()
            print(str)
            lod=-1
            lod = d.play(str)#it stopped when playing
            #r.printAll(True)
            #Naver TTS
            #NaverCSS.speech_syntax(text="잘 알겠습니다.",setting="speaker=mijin&speed=0&text=")
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..','streaming')
                break

            num_chars_printed = 0


def main():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = 'ko-KR'  # a BCP-47 language tag

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)
    # Character analysis
    model_path = 'data/wiki_dmpv_1000_no_taginfo_word2vec_format.bin'
    #model = w.KeyedVectors.load_word2vec_format(model_path,binary=True, unicode_errors='ignore')

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        listen_print_loop(responses)


if __name__ == '__main__':
    main()
