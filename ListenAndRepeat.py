import urllib.request
import subprocess

class ListenAndRepeat:
    def __init__(self):
        self.client_id = "ViFn8vsrA4A1Uvgf5DL3"
        self.client_secret = "SUzlLIm_af"
        self.sema=-1
    def play(self,sentence):
        encText = urllib.parse.quote(sentence)
        data = "speaker=mijin&speed=3&text=" + encText;
        url = "https://openapi.naver.com/v1/voice/tts.bin"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", self.client_id)
        request.add_header("X-Naver-Client-Secret", self.client_secret)
        response = urllib.request.urlopen(request, data=data.encode('utf-8'))
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            with open('test1.mp3', 'wb') as f:
                f.write(response_body)
        else:
            print("Error Code:" + rescode)
        #css.speech_syntax(text=sentence, setting="speaker=mijin&speed=0&text=")
        self.tellme()
    def tellme(self):
        self.sema=0
        audio_file = "test1.mp3"
        subprocess.call(["mplayer", '-really-quiet', audio_file])
        self.sema=-1