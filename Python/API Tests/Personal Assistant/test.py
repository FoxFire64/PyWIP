# to bring text to speech capability to your Windows computer
# install SAPI5Speech (XP and Vista should have it already)
# http://www.nolad.com/vt/redist/SAPI5SpeechInstaller.msi
#
# Windows XP has Sam, SAPI5Voice adds Mary and Mike
# http://www.nolad.com/vt/redist/SAPI5VoiceInstaller.msi
#
# the Python for Windows extensions should be installed
# for COM to work eg.  pywin32-210.win32-py2.5.exe
# from http://sourceforge.net/projects/pywin32/
#
# tested with Python25 on a Windows XP machine by vegaseat
import win32com.client
voices = {
    'Sam': 'Microsoft Sam',
    'Mary': 'Microsoft Mary',
    'Mike': 'Microsoft Mike'
}
# choose voice from the voices dictionary
voice = 'Sam'
# range 0(low) - 100(loud)
volume = 100
# range -10(slow) - 10(fast)
rate = -1
# some text to speak
text = """It is said, that if you line up all the cars in the world end to end, someone would be stupid enough and 
try to pass them. """
# initialize COM components of MS Speech API
# COM is Microsoft's Component Object Model
# (COM is also used by Peter Parente's pyTTS)
speak = win32com.client.Dispatch('Sapi.SpVoice')
# assign a voice
speak.Voice = speak.GetVoices("Name=Microsoft David").Item(0)
speak.Rate = rate
speak.Volume = volume
# now speak out the text
speak.Speak(text)