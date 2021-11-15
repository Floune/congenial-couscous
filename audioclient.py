#!/usr/bin/python3
import os
import socket
import sys
import threading
from threading import Thread
import pyaudio

class Client(Thread):
    def __init__(self):
        Thread.__init__(self)
        

    def run(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        while 1:
            try:
                self.target_ip = os.environ.get('FLOUNE_CHAT_SERVER', 'localhost')
                self.target_port = int(os.environ.get('FLOUNE_AUDIO_PORT', 5557))
                self.s.connect((self.target_ip, self.target_port))
                break
            except:
                print("Couldn't connect to server")

        chunk_size = 1024 # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        # initialise microphone recording
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
        self.exit_flag = False
        print("Connected to Server")

        # start threads
        self.receive_thread = threading.Thread(target=self.receive_server_data).start()
        self.send_data_to_server()

    def receive_server_data(self):
        while True:
            try:
                data = self.s.recv(1024)
                self.playing_stream.write(data)
                if self.exit_flag: 
                    sys.exit()
            except:
                pass


    def send_data_to_server(self):
        while True:
            try:
                data = self.recording_stream.read(1024)
                self.s.sendall(data)
            except:
                pass

    def abortMission(self):
        self.playing_stream.stop_stream()
        self.recording_stream.close()
        self.p.terminate()
        self.exit_flag = True 

