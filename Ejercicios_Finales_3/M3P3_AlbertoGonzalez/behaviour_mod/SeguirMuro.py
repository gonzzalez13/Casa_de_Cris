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


class SeguirMuro(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.goal = 50
        self.front_distance = 80
        self.speed = 15
        self.turn_speed = 5
        self.wall_distance = 50
        self.kp = 1
        self.ki = 0.2
        self.kd = 0.5

    def take_control(self): # type: ignore
        if not self.supress:
            return self.robot.readIRSensor(IR.FrontC) >= self.front_distance

    def run(self):
        print("SeguirMuro init run")
        super().run()
        print("SeguirMuro end run")

    def action(self):
        print("----> control: SeguirMuro")
        self.supress = False
        for bh in self.supress_list:
            bh.supress = True

        frontSensor = IR.FrontRR
        backSensor = IR.BackR

        integral = 0
        previous_error = 0

        self.robot.moveTiltTo(95, 20)
        self.robot.wait(1)
        print(f"Follow wall: {self.robot.readIRSensor(IR.FrontC)}")

        while not self.supress:
            if self.robot.readIRSensor(IR.FrontC) >= self.front_distance:
                self.turn_degrees(-90, self.turn_speed)
                integral = 0
                previous_error = 0
            elif self.robot.readIRSensor(frontSensor) < 30:
                self.move_until_pass_wall(backSensor, frontSensor)
                self.turn_degrees(90, self.turn_speed)
                self.robot.moveWheelsByTime(10, 10, 3)
                integral = 0
                previous_error = 0
            else:
                error = self.robot.readIRSensor(IR.FrontRR) - self.goal
                integral = integral + error
                derivative = error - previous_error
                correction = round(error * self.kp + integral * self.ki + derivative * self.kd)
                previous_error = error
                correction = self.limit_speed(correction, self.speed)
                right_speed = self.limit_speed(self.speed + correction, self.speed)
                left_speed = self.limit_speed(self.speed - correction, self.speed)
                self.robot.moveWheels(right_speed, left_speed)
            self.robot.wait(0.1)

        self.robot.stopMotors()

    ### Specific methods for this behaviour

    def limit_speed(self, speed, max_speed):
        if speed < -2:
            if speed > -5:
                speed = -5
            elif speed < -max_speed:
                speed = -max_speed
        elif speed > 2:
            if speed < 5:
                speed = 5
            elif speed > max_speed:
                speed = max_speed
        return speed

    def adjust_back(self, back_side_sensor):
        self.robot.moveWheels(5, -5)
        while self.robot.readIRSensor(back_side_sensor) < 50 and not self.supress:
            self.robot.wait(0.1)
        self.robot.stopMotors()

    def move_until_pass_wall(self, backSensor, frontSensor):
        self.adjust_back(backSensor)
        self.robot.moveWheels(10, 10)
        while self.robot.readIRSensor(frontSensor) > 10 and not self.supress:
            self.robot.wait(0.01)
        self.robot.stopMotors()

        if not self.supress:
            self.adjust_back(backSensor)
            self.robot.moveWheelsByTime(10, 10, 4)
            if self.robot.readIRSensor(IR.FrontC) >= self.front_distance and not self.supress:
                self.robot.moveWheels(-10, -10)
                while self.robot.readIRSensor(IR.FrontC) >= self.front_distance and not self.supress:
                    self.robot.wait(0.01)
                self.robot.stopMotors()

    def turn_right(self, speed, goal_angle):
        self.robot.moveWheels(-speed, speed)
        # Si pasa de 180º --> continua en -180, -179, ...
        if goal_angle > 180:
            goal_angle = goal_angle - 360
            while 0 <= round(self.robot.readOrientationSensor().yaw) <= 180 and not self.supress:
                self.robot.wait(0.001)
        while round(self.robot.readOrientationSensor().yaw) < round(goal_angle) and not self.supress:
            self.robot.wait(0.001)

    def turn_left(self, speed, goal_angle):
        self.robot.moveWheels(speed, -speed)
        # Si pasa de -180º --> continua en 180, 179, ...
        if goal_angle < -180:
            goal_angle = goal_angle + 360
            while -180 <= round(self.robot.readOrientationSensor().yaw) <= 0 and not self.supress:
                self.robot.wait(0.001)
        while round(self.robot.readOrientationSensor().yaw) > round(goal_angle) and not self.supress:
            self.robot.wait(0.001)

    def turn_degrees(self, degrees, speed):
        orientation = self.robot.readOrientationSensor()
        # Se parte de la posición actual y se suman los grados a girar
        goal_angle = orientation.yaw + degrees
        # giro a la derecha
        if degrees > 0:
            self.turn_right(speed, goal_angle)
        # giro a la izquierda
        else:
            self.turn_left(speed, goal_angle)
        self.robot.stopMotors()
