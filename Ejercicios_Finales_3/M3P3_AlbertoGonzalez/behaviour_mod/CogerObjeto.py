

from behaviour_mod.behaviour import Behaviour
from robobopy.utils.IR import IR

class CogerObjeto(Behaviour):
    def __init__(self,robot,supress_list,params,color):
        super().__init__(robot,supress_list,params)
        self.goal = 80
        self.color = color

    def take_control(self): # type: ignore
        if not self.supress:
            return self.robot.readColorBlob(self.color).posx > 45 and self.robot.readColorBlob(self.color).posx < 60 and self.robot.readColorBlob(self.color).size > 120

    def run(self):
        print("CogerObjeto init run")
        super().run()
        print("CogerObjeto end run")


    def action(self):
        print("----> control: CogerObjeto")
        self.supress = False
        for bh in self.supress_list:
            bh.supress = True
        self.irObjeto()
        print("----")
        self.set_stop()
        print("after set stop")

    def irObjeto(self):
        kp = 0.5

        while self.robot.readIRSensor(IR.FrontC) < self.goal:
            error = self.goal - self.robot.readIRSensor(IR.FrontC)
            speed = round(error * kp)
            self.robot.moveWheels(speed, speed)
            self.robot.wait(0.1)


