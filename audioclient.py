#!/usr/bin/python3
import os
import socket
import sys
import threading
from threading import Thread
import pyaudio

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
target_ip = os.environ.get('FLOUNE_CHAT_SERVER', 'localhost')
target_port = int(os.environ.get('FLOUNE_AUDIO_PORT', 5557))
s.connect((target_ip, target_port))


chunk_size = 1024 # 512
audio_format = pyaudio.paInt16
channels = 1
rate = 20000

# initialise microphone recording
p = pyaudio.PyAudio()
playing_stream = p.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
recording_stream = p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
exit_flag = False



def receive_server_data():
    while True:
        try:
            data = s.recv(1024)
            playing_stream.write(data)
            if exit_flag: 
                break
        except:
            break


def send_data_to_server():
    while True:
        try:
            data = recording_stream.read(1024)
            s.sendall(data)
            if exit_flag: 
                break
        except:
            break


def abortMission():
    global exit_flag
    playing_stream.stop_stream()
    recording_stream.close()
    p.terminate()
    exit_flag = True
    s.close()

# start threads
def run():
    receive_thread = threading.Thread(target=receive_server_data)
    receive_thread.start()
    send_thread = threading.Thread(target=send_data_to_server)
    send_thread.start()