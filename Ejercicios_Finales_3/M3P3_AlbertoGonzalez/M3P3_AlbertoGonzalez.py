

from robobopy.Robobo import Robobo
from robobopy.utils.BlobColor import BlobColor

from behaviour_mod.GoToWall import GoToWall
from behaviour_mod.SeguirMuro import SeguirMuro
from behaviour_mod.BuscarColor import BuscarColor
from behaviour_mod.CogerObjeto import CogerObjeto
import time


def main():
    rob = Robobo("localhost")
    rob.connect()


    rob.setActiveBlobs(True,False,False,False)

    params = {"stop": False}


    GoToWall_behaviour = GoToWall(rob,[],params)
    SeguirMuro_behaviour = SeguirMuro(rob,[GoToWall_behaviour],params)
    BuscarColor_behaviour = BuscarColor(rob,[GoToWall_behaviour,SeguirMuro_behaviour],params,BlobColor.RED)
    CogerObjeto_behaviour = CogerObjeto(rob,[GoToWall_behaviour,SeguirMuro_behaviour,BuscarColor_behaviour],params,BlobColor.RED)

    threads = [GoToWall_behaviour,SeguirMuro_behaviour,BuscarColor_behaviour,CogerObjeto_behaviour]

    GoToWall_behaviour.start()
    SeguirMuro_behaviour.start()
    BuscarColor_behaviour.start()
    CogerObjeto_behaviour.start()

    while not params["stop"]:
        time.sleep(0.1)

    for thread in threads:
        thread.join()

    rob.stopMotors()
    rob.disconnect()



if __name__ == "__main__":
    main()





