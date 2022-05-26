import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def setup():
    os.system("python3 -m pip install -U py-cord[speed]")
    os.system("pip install pymongo[srv]")
    os.system('chmod +777 ./ffmpeg')
    os.system('./ffmpeg')

    os.system('pip install beautifulsoup4')
    os.system('pip install spotipy')

    os.system("python3 -m pip install -U py-cord[voice]")
    os.system("python3 -m pip install ffmpeg")
    cls()
    