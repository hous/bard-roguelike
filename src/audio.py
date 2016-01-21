import pyo
import time
import threading

class Audio(object):
    def __init__(self):
        self.server = pyo.Server(sr=44100, nchnls=2, buffersize=256, duplex=0).boot()
        self.server.start()
        self.background_thread = None
        self.foreground_thread = None

    def play_sound(self):
        def sound():
            wav = pyo.SquareTable()
            env = pyo.CosTable([(0,0), (100, 1), (500, .3), (8191, 0)])
            met = pyo.Metro(.225, 12).play()
            amp = pyo.TrigEnv(met, table=env, dur=1, mul=.1)
            pit = pyo.TrigXnoiseMidi(met, dist='loopseg', x1=20, scale=1, mrange=(48, 84))
            out = pyo.Osc(table=wav, freq=pit, mul=amp).out()
            time.sleep(2.000000)

        self.foreground_thread = threading.Thread(target=sound)
        self.foreground_thread.start()

    def play_background(self):
        def sound():
            pass

        self.background_thread = threading.Thread(target=sound)
        self.background_thread.start()


    def kill(self):
        self.server.stop()
        time.sleep(1)
        self.server.shutdown()
