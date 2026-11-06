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
from robobopy.utils.IR import IR

class GoToWall(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.goal = 80

    def take_control(self): # type: ignore
        if not self.supress:
            return True  

    def run(self):
        print("GoToWall init run")
        super().run()
        print("GoToWall end run")            

    def action(self):
        print("----> control: GoToWall")
        self.supress = False
        kp = 0.5
        while (self.robot.readIRSensor(IR.FrontC) < self.goal) and (not self.supress):
            error = self.goal - self.robot.readIRSensor(IR.FrontC)
            correction = round(error * kp)
            speed = self.limit_speed(correction)
            self.robot.moveWheels(speed, speed)
            self.robot.wait(0.1)

        self.robot.stopMotors()

    def limit_speed(self,speed):
        if speed < 2:
            return 2
        return speed          
