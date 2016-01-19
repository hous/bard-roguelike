import pyo
import time


class Audio(object):
    def __init__(self):
        self.server = pyo.Server(sr=44100, nchnls=2, buffersize=256, duplex=0).boot()
        self.server.start()


    def play_sound(self):
        sine = pyo.Sine(freq=[400,500], mul=.2).out()
        time.sleep(1.000000)


    def kill(self):
        self.server.stop()
        time.sleep(1)
        self.server.shutdown()
