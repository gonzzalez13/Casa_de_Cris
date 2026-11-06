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

from behaviour_mod.behaviour import Behaviour


class BuscarColor(Behaviour):
    def __init__(self, robot, supress_list, params, color):
        super().__init__(robot, supress_list, params)
        self.color = color

    def take_control(self): # type: ignore
        if not self.supress:
            return self.robot.readColorBlob(self.color).size > 100 and self.robot.readColorBlob(self.color).size < 120

    def action(self):
        print("----> control: BuscarColor")
        self.supress = False
        for bh in self.supress_list:
            bh.supress = True

        self.turnToBlob(self.color)
        print("----")
        # self.set_stop()
        # print("after set stop")

    def run(self):
        print("BuscarColor init run")
        super().run()
        print("BuscarColor end run")

    def turnToBlob(self, color):
        speed = 10

        while (self.robot.readColorBlob(color).posx < 45) or (self.robot.readColorBlob(color).posx > 60):
            blob = self.robot.readColorBlob(color)
            if blob.posx > 55:
                self.robot.moveWheels(5, speed)
            else:  # blob.posx < 45:
                self.robot.moveWheels(speed, 5)
            self.robot.wait(0.1)

        self.robot.stopMotors()
