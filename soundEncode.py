import numpy as np
import pyaudio
from reedsolo import RSCodec

HANDSHAKE_START_HZ = 8192# select start hz
HANDSHAKE_END_HZ = 8704# select start hz (higher than start hz)

START_HZ = 1024
STEP_HZ = 256
BITS = 4

FEC_BYTES = 4

def sound_generate(stream, freq):
    ######insert your code in function######
    t = np.arange(44100*1.0)
    samples = np.sin(2 * np.pi * freq * t / 44100).astype(np.float32)
    stream.write(samples)
'''
    t = np.arange(44100*0.5)
    samples = [np.sin(2*np.pi*HANDSHAKE_START_HZ*t/44100)]
    for i in range(len(freq)):
        print(freq[i])
        samples.append(np.sin(2*np.pi*freq[i]*t))
    samples.append(np.sin(2*np.pi*HANDSHAKE_END_HZ*t))
    samples = np.array(samples).astype(np.float32)
'''


def divide_by_tone(each_data):
    ######insert your code in function######
    pass


def to_freq(step):
    ######insert your code in function######
    return START_HZ + step * STEP_HZ

def sound_code(fec_payload):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=44100,
                    output = True)

    ######insert your code below######
    data = []
    for byte_data in fec_payload:
        data.append(byte_data >> 4)
        data.append(byte_data & 15)
    freqs = []
    for step in data:
        freqs.append(to_freq(step))
    sound_generate(stream, HANDSHAKE_START_HZ)
    for freq in freqs:
        print(freq)
        sound_generate(stream, freq)
    sound_generate(stream, HANDSHAKE_END_HZ)

def play_sound(msg):
    byte_array = msg.encode()
    rs = RSCodec(FEC_BYTES)
    fec_payload = bytearray(rs.encode(byte_array))
    
    sound_code(fec_payload)

if __name__ == '__main__':
    input_msg = input("Input : ")

    play_sound(input_msg)
