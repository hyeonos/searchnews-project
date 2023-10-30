import speech_recognition as sr


# 음성 인식 객체 생성

def SpeechRecognition() :
    print("speech_recognition start")

    recognizer = sr.Recognizer()


    with sr.Microphone() as source :
        print("Say something ... ")
        recognizer.adjust_for_ambient_noise(source)     # 배경 소음 조절?
        audio = recognizer.listen(source)
        print(audio)
        
        
    try :
        words = recognizer.recognize_google(audio, language='ko-KR')
    except Exception as e:
        print("Speech recognition failed. ", e)
    
    print('recognized words : ', words)
    return words