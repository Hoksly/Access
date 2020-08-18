import time
import cv2
import face_recognition as fr
import numpy as np
import os


def get_names_and_encodes_from_file():
    # folder = os.getcwd()
    folder = '/root/Github/Access/Data'
    try:
        with open(folder + '/Persons.txt', 'a') as t:
            t.close()
    except:
        with open(folder + '/Persons.txt', 'w') as t:
            t.close()

    file = open(folder + '/Persons.txt', 'r')
    names_and_enc = file.read().split('\n')[1:]

    if True:
        d = {}

        for line in names_and_enc:
            enc = np.array(list(map(float, line[line.index(':') + 2:].split())))
            name = line[0:line.index(':')]
            d.update({name: enc})
        return d
    # else:
    #   return {}


def get_encodes_from_dict(dic):
    return list(dic.values())


def compare(targets_encode, known_encodes_and_names):
    """

    :param known_encodes_and_names: dict
    :type targets_encode: list
    """
    enc = get_encodes_from_dict(known_encodes_and_names)

    for target_encode in targets_encode:
        res = fr.compare_faces(enc, target_encode)
        if True in res:
            n = res.index(True)
            name = list(known_encodes_and_names.keys())[n]
            return name
        else:
            return 'Unknown Person'


'''
def main():
    known_encodes_and_names = get_names_and_encodes_from_file()

    cap = cv2.VideoCapture(0)

    name = ''

    enc = list(known_encodes_and_names.values())

    while True:

        ret, frame = cap.read()
        f_l = fr.face_locations(frame)
        counter = 0

        if len(f_l) > 0:
            new_enc = fr.face_encodings(frame, f_l)

            try:
                a = fr.compare_faces(enc, new_enc)
            except:
                a = [False]

            if True not in a:

                new_name = compare(new_enc, known_encodes_and_names)
                enc = new_enc
                if name != new_name:
                    name = new_name
                    if name != "Unknown Person":
                        return name
                    else:
                        if counter > 1:
                            return 'Unknown Person'
                        else:
                            counter += 1
                else:
                    continue

        if time.process_time() > 10:
            break

    cap.release()
    cv2.destroyAllWindows()
'''


class FaceAccess:
    @staticmethod
    def check():

        known_encodes_and_names = get_names_and_encodes_from_file()

        cap = cv2.VideoCapture(0)

        name = ''

        enc = list(known_encodes_and_names.values())

        while True:

            ret, frame = cap.read()
            f_l = fr.face_locations(frame)
            counter = 0

            if len(f_l) > 0:
                new_enc = fr.face_encodings(frame, f_l)

                try:
                    a = fr.compare_faces(enc, new_enc)
                except:
                    a = [False]

                if True not in a:


                    new_name = compare(new_enc, known_encodes_and_names)
                    enc = new_enc
                    if name != new_name:
                        name = new_name
                        if name != "Unknown Person":
                            return name
                        else:
                            if counter > 1:
                                return 'Unknown Person'
                            else:
                                counter += 1
                    else:
                        continue

            # if time.process_time() > 10:
            #   break

        cap.release()
        cv2.destroyAllWindows()


class FaceAdder:
    @staticmethod
    def AddPersonFromCamera():

        cap = cv2.VideoCapture(0)
        # folder = os.getcwd()
        folder = "/root/Github/Access/Data"
        try:
            with open(folder + '/Persons.txt', 'a') as t:
                t.close()
        except:
            with open(folder + '/Persons.txt', 'w') as t:
                t.close()

        file = open(folder + '/Persons.txt', 'a')

        while True:
            ret, frame = cap.read()
            f_l = fr.face_locations(frame)

            if len(f_l) == 1:
                enc = fr.face_encodings(frame, f_l)[0]

                if True:  # if not check():
                    time.sleep(0.8)
                    name = input("Your Name:") + ": "

                    encode = ''
                    for i in enc:
                        encode += str(i) + ' '

                    file.write('\n')
                    file.write(name + encode)
                    break

            elif len(f_l) == 2:
                print("Must be only one person in camera view")
                time.sleep(1)

        file.close()
        print("Done")


