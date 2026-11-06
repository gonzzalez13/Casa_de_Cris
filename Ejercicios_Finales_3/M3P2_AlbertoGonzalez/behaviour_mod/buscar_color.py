
from behaviour_mod.behaviour import Behaviour


class BuscarColor(Behaviour):
    def __init__(self, rob, supress_list, params,color):
        super().__init__(rob, supress_list, params)
        self.color = color

    def take_control(self): # type: ignore
        if not self.supress:
                return True

    def run(self):
        print("BuscarColor init run")
        super().run()
        print("BuscarColor end run")


    def action(self):
        print("----> control: BuscarColor")
        self.supress = False
        speed = 10
        self.rob.moveTiltTo(100,speed)
        self.moverPanx(self.color,speed)

    #Movemos el Pan de 5 en 5 mientras revisamos que el size del blob no a sido visto si se ve se para el movimiento
    def moverPanx(self,color,speed):
        Grados = 10
        Localizado = False
        while self.rob.readColorBlob(color).size < 30 or not Localizado:
            size = self.rob.readColorBlob(color).size
            print(f"Size1: {size}")

            if  self.rob.readColorBlob(color).size > 20:
                Localizado = True
                print("Blob localizado")
            if Grados > 0 and Grados < 180 and size < 20:
                print("1")
                Grados = Grados + 5
                self.rob.movePanTo(Grados,speed)
                self.rob.wait(0.1) 
            if Grados >= 180 or Grados <= -180 and size < 20:
                print("2")
                self.rob.movePanTo(0,speed)
                self.rob.wait(0.1)
                Grados = 0
            elif Grados <= 0 and size < 20:
                print("3")
                Grados = Grados - 5
                self.rob.movePanTo(Grados,speed)
                self.rob.wait(0.1)
            self.rob.wait(0.1) 


