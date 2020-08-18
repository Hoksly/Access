from modules.Voice import Cheacker, Listener
from modules.Face import FaceAccess
import os

'''
def take_name_from_camera(image=None):
    if image == None:
        code = 'python3 /root/Github/Detection_Project/Acces/Face_acces/Access.py'
        process = subprocess.Popen(code.split(), stdout=subprocess.PIPE)
        out, err = process.communicate()
        out = out.decode('utf-8')
        name = out.split('\n')[0]

        return name
'''


def take_name_from_camera():
    name = FaceAccess.check()

    return name


def take_name_from_voice(voice_file='', mode=False):
    if voice_file == '':
        try:
            Listener.listen(12, filename='output.wav')
        except:
            print('Error when listen your voice')
            return 'Unknown Person'

        name = Cheacker.check('output.wav')
        os.remove('output.wav')
        return name

    elif voice_file == "None":
        print('None voice file. Recognition now is based only on face')
        return 'Hydra'

    return Cheacker.check(voice_file)


def compare_names(voice_name, face_name):
    if voice_name != 'Unknown Person' and face_name != 'Unknown Person' and voice_name != 'Hydra':
        if voice_name == face_name or voice_name == 'Hydra':
            return True, face_name
        else:
            return False, 'Unknown Person'

    elif voice_name == 'Hydra':
        return True, face_name

    elif voice_name == 'Unknown Person':
        print("Voice recognition was broken. Please try again {0}".format(face_name))
        return False, face_name

    elif face_name == 'Unknown Person':
        print('Face recognition access was broken. Please try again {0}.'.format(voice_name))
        return False, voice_name


def take_voice_from_mic():
    voice_file = None
    return voice_file


def main():
    voice_name = take_name_from_voice('None')  # if you want to recognize your voice from mic, voice_file must be empty
    face_name = take_name_from_camera()

    res, Name = compare_names(voice_name, face_name)

    if res:
        print()
        print('Welcome back ' + Name)
        print()
    else:
        print(Name)


main()
