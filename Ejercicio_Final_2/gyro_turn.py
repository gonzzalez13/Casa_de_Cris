from robobopy.Robobo import Robobo


class Gyroturn():
    def __init__(self, robot: Robobo, speed=5):
        self.robot = robot
        self.speed = speed
    
    def turn_right(self,goal_angle):
        self.robot.moveWheels(0, self.speed)
        # Si pasa de 180º --> continua en -180, -179, ...
        if goal_angle > 180:
            goal_angle = goal_angle - 360
            while 0 <= self.robot.readOrientationSensor().yaw <= 180:
                self.robot.wait(0.001)
        while round(self.robot.readOrientationSensor().yaw) < goal_angle:
            self.robot.wait(0.001)


    def turn_left(self,goal_angle):
        self.robot.moveWheels(self.speed,0)
        # Si pasa de -180º --> continua en 180, 179, ...
        if goal_angle < -180:
            goal_angle = goal_angle + 360
            while -180 <= self.robot.readOrientationSensor().yaw <= 0:
                self.robot.wait(0.001)
        while self.robot.readOrientationSensor().yaw > goal_angle:
            self.robot.wait(0.001)


    def turn_degrees(self,angle):
        orientation = self.robot.readOrientationSensor()
        # Se parte de la posición actual y se suman los grados a girar
        goal_angle = orientation.yaw + angle
        # giro a la derecha
        if angle > 0:
            self.turn_right(goal_angle)
        # giro a la izquierda
        else:
            self.turn_left(goal_angle)
        self.robot.stopMotors()