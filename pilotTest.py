from konlpy.tag import Komoran 
from konlpy.tag import Kkma
from konlpy.tag import Twitter
twit = Twitter()
kom = Komoran()
kkma = Kkma()
teststr="법무부가 우선 경제민주화법 개정 추진을 추진한다."
print(kkma.pos(teststr))
print(kom.pos(teststr))
print(twit.pos(teststr))
