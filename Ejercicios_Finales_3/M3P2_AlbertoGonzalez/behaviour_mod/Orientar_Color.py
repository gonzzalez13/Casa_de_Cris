from behaviour_mod.behaviour import Behaviour


class OrientarColor(Behaviour):
    def __init__(self, rob, supress_list, params, color):
        super().__init__(rob, supress_list, params)
        self.color = color

    def take_control(self): # type: ignore
        if not self.supress:
            return self.rob.readColorBlob(self.color).size > 30

    def action(self):
        print("----> control: OrientarColor")
        self.supress = False
        for bh in self.supress_list:
            bh.supress = True

        self.turnToBlob(self.color)      
        print("----")
        self.set_stop()
        print("after set stop")

    def run(self):
        print("OrientarColor init run")
        super().run()
        print("OrientarColor end run")


    #una vez se ha locazado el blob con la posx giramos hasta locazarlo y luego se sige ajustando hasta estar en la posicion entre 45/55 
    def turnToBlob(self, color):
        size = self.rob.readColorBlob(self.color).size
        print(f"Size2: {size}") 
        speed = 10
        orientation = self.rob.readOrientationSensor()
        Posx = self.rob.readColorBlob(color).posx
        blob = self.rob.readColorBlob(color)
        self.rob.wait(0.2)
        print(f"Posx: {Posx}")
        self.rob.movePanTo(0,speed)
        while self.rob.readColorBlob(color).size == 0:
            goal_angle = orientation.yaw + 10
            if Posx > 40:
                self.turn_right(goal_angle)
            else:
                self.turn_left(goal_angle)
            self.rob.wait(0.1)


        while (self.rob.readColorBlob(color).posx < 45) or (self.rob.readColorBlob(color).posx > 55):
            goal_angle = orientation.yaw + 10
            if blob.posx > 40:
                self.turn_right(goal_angle)
            else:
                self.turn_left(goal_angle)
            self.rob.wait(0.1)

        self.rob.stopMotors()

    #giro a la derecha con los grados
    def turn_right(self,goal_angle):
        speed_Ruedas = 5
        self.rob.moveWheels(0, speed_Ruedas)
        # Si pasa de 180º --> continua en -180, -179, ...
        if goal_angle > 180:
            goal_angle = goal_angle - 360
            while 0 <= self.rob.readOrientationSensor().yaw <= 180:
                self.rob.wait(0.001)
        while round(self.rob.readOrientationSensor().yaw) < goal_angle:
            self.rob.wait(0.001)

    #giro a la izquierda con los grados
    def turn_left(self,goal_angle):
        speed_Ruedas = 5
        self.rob.moveWheels(speed_Ruedas,0)
        # Si pasa de -180º --> continua en 180, 179, ...
        if goal_angle < -180:
            goal_angle = goal_angle + 360
            while -180 <= self.rob.readOrientationSensor().yaw <= 0:
                self.rob.wait(0.001)
        while round(self.rob.readOrientationSensor().yaw) > goal_angle:
            self.rob.wait(0.001)
