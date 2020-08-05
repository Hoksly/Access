import librosa as lr
import numpy as np
import sys
from pydub import AudioSegment
import wave
import pyaudio

SR = 1600
LENGHT = 16
OVERLAP = 8
FFT = 1024
directory = '/root/Github/Acces/Access/Data'


def confidece(x, y):
    return np.sum((x - y) ** 2)


def filter_audio(audio):
    apower = lr.amplitude_to_db(np.abs(lr.stft(audio, n_fft=2048)), ref=np.max)
    apsums = []
    for i in apower:
        apsums.append(np.sum(i, axis=0) ** 2)
    apsums = np.array(apsums)
    apsums -= np.min(apsums)
    apsums /= np.max(apsums)
    apsums = np.convolve(apsums, np.ones((9,)), 'same')
    apsums -= np.min(apsums)
    apsums /= np.max(apsums)

    apsums = np.array(apsums > 0.35, dtype=bool)
    apsums = np.repeat(apsums, np.ceil(len(audio) / len(apsums)))[:len(audio)]

    return audio[apsums]


def process_audio(aname):
    audio, _ = lr.load(aname)

    afs = lr.feature.mfcc(audio,
                          sr=SR,
                          n_mfcc=34,
                          n_fft=2048)

    affs = np.sum(afs[2:], axis=-1)

    affs = affs / np.max(np.abs(affs))

    return affs


def download_audios(file_name):
    file = open(file_name, 'r')
    s = file.read()
    files = list(s.split('\n'))
    out = {}
    for file in files:
        name = file[:file.index(':')]
        enc = list(map(float, file[file.index(':') + 1:].split()))
        out.update({name: np.array(enc)})
    return out


def check(name):
    if '.wav' in name:
        return name
    elif '.mp3' in name:
        AudioSegment.from_mp3(name).export(name[:-4] + '.wav', format='wav')
        name = name[:-4] + '.wav'
        return name
    else:
        return None


def unload_voices(voices_set: dict, file_name: str):
    """
    :param file_name: name of output file
    :param voices_set: dict with names and voice encodes
    :return: None
    """
    file = open(file_name, 'a')
    names = list(voices_set.keys())
    voices = list(voices_set.values())

    for i in range(len(voices_set)):
        name = names[i]
        voice = voices[i]
        out = name + ': '

        for el in voice:
            out += (str(el) + ' ')

        file.write('\n')
        file.write(out)


class Cheacker:
    """
    def __init__(self, voices_file_name = directory + 'voices.txt'):
        self.names_and_voices = download_audios(voices_file_name)
    """

    @staticmethod
    def check(new_voice, names_and_voices_file=directory + 'voices.txt'):
        names_and_voices = download_audios(names_and_voices_file)
        unknown_audio = filter_audio(process_audio(new_voice))

        res = []
        voices = list(names_and_voices.values())
        names = list(names_and_voices.keys())
        del names_and_voices

        for v in voices:
            while len(v) < len(unknown_audio):
                v = np.append(v, 0.)

            while len(v) > len(unknown_audio):
                unknown_audio = np.append(unknown_audio, 0.)

            res.append(confidece(v, unknown_audio))

        r, ind = min(res), res.index(min(res))

        if r > 0.05:
            return "Unknown Person"
        else:
            return names[ind]


class Adder:
    """

    def __init__(self, voices_file_name = directory + 'voices.txt'):
        self.file_name = voices_file_name
    """

    @staticmethod
    def add_audio(audio_file, file_name = directory + 'voices.txt'):
        new_audio = check(audio_file)

        audio = filter_audio(process_audio(new_audio))

        try:
            file = open(file_name, 'a')
        except:
            file = open(file_name, 'w')

        if '/' in new_audio:
            name = new_audio.split('/')[-1]
            name = name[:name.index('.wav')]
        else:
            name = new_audio[:new_audio.index('.wav')]

        unload_voices({name: audio}, file_name)


class Listener:
    @staticmethod
    def listen(seconds, filename = 'output.wav'):
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 2
        fs = 44100  # Record at 44100 samples per second

        f

        p = pyaudio.PyAudio()  # Create an interface to PortAudio

        print('Recording')

        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []  # Initialize array to store frames

        # Store data in chunks for 3 seconds
        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()

        print('Finished recording')

        # Save the recorded data as a WAV file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()