import subprocess
import os
from shutil import move
import pyAesCrypt as cryp
from random import choice
import sys

directory = '/home/hoksly/Githab/'  # you must change to your own directory, where is your Access project
crypted_dir = directory + 'Access/Data/Crypted/'
crypted_file = directory + 'Access/Data/files.txt'


def crypt(password, filename, out):
    bufferSize = 64 * 1024
    cryp.encryptFile(filename, out, password, bufferSize)


def decrypt(password, encrypted, out):
    bufferSize = 1024 * 64
    cryp.decryptFile(encrypted, out, password, bufferSize)


def read(filename):
    file = open(filename, 'r')
    data = file.read().split('\n')
    if len(data[0]) > 0:
        pass
    else:
        data = data[1:]
    res = []
    for line in data:
        name = line[0:line.index(',')]
        encrypted = line[line.index(',') + 2:line.index(':')]
        password = line[line.index(':') + 2:]
        res.append([name, encrypted, password])
    return res


def encrypt_from_list(data):
    for line in data:
        decrypt(line[2], line[1], line[0])


class Decoder:
    @staticmethod
    def decode():
        encrypt_from_list(read(crypted_file))


def gen_pass():
    s = ''

    for i in range(16):
        s += choice(
            '1 2 3 4 5 6 7 8 9 0 - = _ + q w e r t y u i o p [ ] { } a s d f g h j k l ; z x c v b n m '
            'Q W E R T Y U I O P A S D F G H J K L Z X C V B N M < > ? ` ! '.split())
    return s


def not_dir(file):
    return True


def create_new_encrypt_file(files, password=gen_pass()):
    """

    :param password: password for new file
    :param file: file to be encrypt
    :return: None
    """

    file1 = open(crypted_file, 'a')
    file2 = open(crypted_file, 'r')
    l = len((file2.read().split('\n')))

    for line in files:
        new_name = crypted_dir + 'encrypted' + str(l) + '.aes'
        crypt(password, line, new_name)
        # os.remove(line)
        file1.write('\n')
        file1.write(line + ', ' + new_name + ': ' + password)
        l += 1


class Coder:
    @staticmethod
    def code():
        directory = os.getcwd()
        files = os.listdir(directory)
        new = []
        for file in files:
            if 'Coder' not in file or 'coder' not in file:
                new.append(directory + '/' + file)

        for file in new:
            if not_dir(file):
                create_new_encrypt_file([file])



def main():
    inp = sys.argv
    if '-C' in inp or '-c' in inp:
        Coder.code()
    elif '-d' in inp or '-D' in inp:
        Decoder.decode()
    else:
        print("For coding files try: -c or -C key. \nFor decoding files try: -d or -D key.")

if __name__ == '__main__':
    main()