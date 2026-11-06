#
# Copyright (c) 2022 Manufactura de ingenios tecnológicos SL.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from robobopy.Robobo import Robobo
from threading import Thread
import time


class Behaviour(Thread):
    def __init__(self, robot: Robobo, supress_list, params, **kwargs):
        super().__init__(**kwargs)
        self.robot = robot
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
