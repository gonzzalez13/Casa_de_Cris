

from behaviour_mod.behaviour import Behaviour
from robobopy.utils.IR import IR

class MoverseColor(Behaviour):
    def __init__(self,rob,supress_list,params,color):
        super().__init__(rob,supress_list,params)
        self.goal = 80
        self.color = color

    def take_control(self): # type: ignore
        if not self.supress:
            return self.rob.readColorBlob(self.color).posx > 45 and self.rob.readColorBlob(self.color).posx < 55

    def run(self):
        print("MoverseColor init run")
        super().run()
        print("MoverseColor end run")


    #una vez estamos en la posicion adecuada respecto a la posx el robot va hacia delante y si la posy es superior 50 se activa el tilt para ajustarse 
    def action(self):
        print("----> control: MoverseColor")
        self.supress = False
        kp = 0.5

        while self.rob.readIRSensor(IR.FrontC) < self.goal:
            if self.rob.readColorBlob(self.color).posy > 50:
                error = self.goal - self.rob.readIRSensor(IR.FrontC)
                speed = round(error * kp)
                self.rob.moveWheels(speed, speed)
                self.rob.wait(0.1)
            else:
                self.rob.stopMotors()
                self.moverTilt(self.color,10)

        self.rob.stopMotors()


    def moverTilt(self,color,speed):
        Grados = 100
        print("Mover Tilt")
        while self.rob.readColorBlob(color).size < 100:
            Grados = Grados + 5
            self.rob.moveTiltTo(Grados,speed)
            self.rob.wait(0.1)
