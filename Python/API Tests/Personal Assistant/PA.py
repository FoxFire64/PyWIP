"""
    Don't mind me, just overdoing it with the APIs and trying
    to make a personal assistant. So far it speaks (still 
    need to learn how to speed it up), it searches well,
    and can do basic computations. I'm considering adding in
    some default readouts to run the first time the computer is
    restarted after 8:00AM daily.
    
    Maybe I'll have a readout for tasks, calendar events, and
    the weather. Then it'll always be listening (wassup, Big Brother)
    
    I should probably include some real documentation....soon
    
"""
import wolframalpha, wikipedia
import win32com.client as wincl

speak = wincl.Dispatch("SAPI.SpVoice")
speak.Speak('Hello sir, what can I do for you?')

query = input("Q: ")

try:
    app_id = "75TTPT-6J63VH47ET"
    client = wolframalpha.Client(app_id)
    res = client.query(query)
    answer = next(res.results).text
    print(answer)
except:
    try:
        speak.Speak(wikipedia.summary(query, sentences=2))
    except wikipedia.exceptions.DisambiguationError as dis_err:
        speak.Speak("Looks like there's more than one option for this query, pick one from the menu")
        for option in dis_err.options:
            print(option)
        spec_res = str(input("Specific Query: "))
        speak.Speak(wikipedia.summary(spec_res, sentences=2))

