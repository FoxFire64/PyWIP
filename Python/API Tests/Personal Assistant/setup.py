from cx_Freeze import setup, Executable

base = None

executables = [Executable("PyPIR.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {
        'packages': packages,
    },
}

setup(
    name="PyPIR",
    options=options,
    version="0.8.1",
    description='Python Personal Inquiry Resolver',
    executables=executables, requires=['wolframalpha', 'wikipedia', 'pyowm', 'twilio', 'SpeechRecognition', 'cx_Freeze',
                                       'pyttsx3']
)
