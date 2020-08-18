from modules.Voice import Adder, Listener
from modules.Face import FaceAdder
import os


def main():
    mode = ''
    while mode != 'F' or mode != 'V' or mode != 'f' or mode != 'v':
        mode = input('For adding face print F, for voice print V.'
                     'For exit print X')

        if mode == 'x' or mode == 'X':
            return None

    if mode == 'f' or mode == 'F':
        FaceAdder.AddPersonFromCamera()
    else:
        mode2 = input('Listen from mic, or file? y / n')
        if mode2 == 'y' or mode2 == 'Y':
            Listener.listen(10, filename= 'output.wav')
            Adder.add_audio('output.wav')
            os.remove('output.wav')
        else:
            inp = input('Full name of file(with all directories): ')
            Adder.add_audio(inp)
