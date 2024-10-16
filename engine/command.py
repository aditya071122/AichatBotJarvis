import pyttsx3
import speech_recognition as sr
import eel
import time

def speak(text):
    text=str(text)
    engine=pyttsx3.init('sapi5')
    voices=engine.getProperty('voices')
    engine.setProperty('voice',voices[0].id)
    engine.setProperty('rate',174)
    eel.DisplayMessage(text)  # type: ignore
    engine.say(text)
    eel.receiverText(text) # type: ignore
    engine.runAndWait()
    
    
def takecommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening..")
        eel.DisplayMessage("Listening..") # type: ignore
        r.pause_threshold=1
        r.adjust_for_ambient_noise(source)
        
        audio=r.listen(source,10,6)
        
    try:
        print("Recognizing..")
        eel.DisplayMessage("Recognizing..") # type: ignore
        query=r.recognize_google(audio,language='en-in')  # type: ignore
        print(f"user said:{query}")
        time.sleep(2)
    except Exception as e:
        return ""
    return query.lower()

@eel.expose
def allCommands(message=1):
    if message==1:
        query=takecommand()
        print(query)
        eel.senderText(query) # type: ignore
    else:
        query=message
        eel.senderText(query) # type: ignore
        
    try:
        
        if "open" in query: # type: ignore
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query: # type: ignore
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "send message" in query or "phone call" in query or "video call" in query: # type: ignore
            from engine.features import findContact, whatsApp
            contact_no, name = findContact(query)
            if(contact_no != 0):
                speak("Which mode you want to use whatsapp or mobile")
                preferance = takecommand()
                print(preferance)

                if "mobile" in preferance:
                    if "send message" in query or "send sms" in query:  # type: ignore
                        speak("what message to send")
                        message = takecommand()
                    elif "whatsapp" in preferance:
                        message = ""
                    if "send message" in query: # type: ignore
                        message = 'message'
                        speak("what message to send")
                        query = takecommand()
                                        
                    elif "phone call" in query: # type: ignore
                        message = 'call'
                    else:
                        message = 'video call'
                elif "whatsapp" in preferance:
                    message = ""
                    if "send message" in query: # type: ignore
                        message = 'message'
                        speak("what message to send")
                        query = takecommand()
                                        
                    elif "phone call" in query: # type: ignore
                        message = 'call'
                    else:
                        message = 'video call'
                                        
                    whatsApp(contact_no, query, message, name)
        else:
            from engine.features import chatBot
            chatBot(query)
            # print("not run") 
            
    except:
        print("error")  
            
    
    
    eel.ShowHood() # type: ignore
        
    

