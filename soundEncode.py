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
    #하나의 주파수를 얼마나 오래 출력할지 결정하는 변수
    t = np.arange(44100*1.0)
    #freq에 비례하는 주파수를 가지는 사인 함수를 만들어서 float 배열로 만든 후 소리 출력
    samples = np.sin(2 * np.pi * freq * t / 44100).astype(np.float32)

    stream.write(samples)


def divide_by_tone(each_data):
    ######insert your code in function######
    pass


def to_freq(step):
    ######insert your code in function######
    #주파수 변환 공식에 맞게 시작 주파수에 STEP 주파수와 4비트 데이터를 곱한 값을 력더하여 반환
    return START_HZ + step * STEP_HZ

def sound_code(fec_payload):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=44100,
                    output = True)

    ######insert your code below######
    #fec_payload의 데이터 하나하나를 4비트씩 분할하여 주파수 형태로 변환
    data = []
    for byte_data in fec_payload:
        data.append(byte_data >> 4)
        data.append(byte_data & 15)
    freqs = []
    for step in data:
        freqs.append(to_freq(step))
    #주파수에 따른 소리를 만들고 출력하는 함수를 통해 HANDSHAKE 주파수와 payload 데이터들의 주파수의 소리 출력
    sound_generate(stream, HANDSHAKE_START_HZ)
    for freq in freqs:
        #payload 데이터들의 주파수를 출력
        print(freq)
        sound_generate(stream, freq)
    sound_generate(stream, HANDSHAKE_END_HZ)

def play_sound(msg):
    #RSCodec.encode 함수 오류로 인해 입력받은 msg를 encode하고 함수 실행
    byte_array = msg.encode()
    rs = RSCodec(FEC_BYTES)
    fec_payload = bytearray(rs.encode(byte_array))
    
    sound_code(fec_payload)

if __name__ == '__main__':
    input_msg = input("Input : ")

    play_sound(input_msg)
