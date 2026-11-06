from robobopy.Robobo import Robobo
from threading import Thread
import time

class Behaviour(Thread):
    def __init__(self, rob:Robobo, supress_list, params, **kwargs):
        super().__init__(**kwargs)
        self.rob = rob
        self.__supress = False
        self.supress_list = supress_list
        self.params = params

    def take_control(self):
        pass

    def action(self):
        pass

    def run(self):
        while not self.params["stop"]:
            while not self.take_control() and not self.params["stop"]:
                time.sleep(0.01)
            if not self.params["stop"]:
                self.action()

    @property
    def supress(self):
        return self.__supress

    @supress.setter
    def supress(self, state):
        self.__supress = state

    def set_stop(self):
        self.params["stop"] = True

    def stopped(self):
        return self.params["stop"]
    