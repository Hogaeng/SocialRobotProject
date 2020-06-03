# 한국과학기술연구원 소셜로봇 프로젝트 코드
해당 내용은 프로젝트 전체가 아닌 일부를 나타냅니다.    
관련 프로젝트를 진행하기 위한 파일럿 테스트에서 작성한 코드를 서술합니다.

## ListenAndRepeat.py
네이버의 openapi를 이용해 텍스트를 오디오 파일로 만들고, 재생하는 객체 ListenAndRepeat가 정의됨.
* play(sentence) : sentence의 문장 네이버 openapi를 이용해 분석 후 오디오 파일로 만드는 함수.
* tellme() : play 함수에서 만들어진 오디오 파일을 재생하는 함수.

## transcribe_streaming_mic.py
GoogleSpeech를 이용해 마이크의 음성데이터를 텍스트로 만드는 기능을 멀티스레드로 진행하는 역할.     
Google Cloud Speech API 샘플 코드를 사용.
## pilotTest.py
KoNLPy의 komoran, kkma, twitter 태그를 이용해 품사를 나누는 코드.
각 태그마다 품사가 다르다.

## pilotTest2.py
gensim으로 word2vec 모델을 불러 테스트를 진행하는 코드.    
모델은 용량이 너무 커 gitignore로 업로드에 제외시켰음.    
숫자가 1에 가까울수록 상관관계가 높다.
* similarity(w1, w2) : 두 단어의 상관관계가 얼마나 차이나는지 수치로 나타냄.
* most_similar(w1) : 해당 단어와 가장 유사한 단어와 그 단어와의 상관관계를 수치로 나타냄.
