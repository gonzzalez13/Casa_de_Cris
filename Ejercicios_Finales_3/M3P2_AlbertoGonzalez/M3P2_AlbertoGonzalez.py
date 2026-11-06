from robobopy.Robobo import Robobo
from robobopy.utils.BlobColor import BlobColor

from behaviour_mod.Orientar_Color import OrientarColor
from behaviour_mod.buscar_color import BuscarColor
from behaviour_mod.moverse_color import MoverseColor
import time


def main():
    rob = Robobo("Localhost")
    rob.connect()
    rob.resetColorBlobs()

    rob.setActiveBlobs(True,False,False,False)

    params = {"stop": False}

    #Crar los comportamientos
    BuscarColor_behaviour = BuscarColor(rob,[],params,BlobColor.RED)
    OrientarColor_behaviour = OrientarColor(rob,[BuscarColor_behaviour],params,BlobColor.RED)
    MoverseColor_behaviour = MoverseColor(rob,[BuscarColor_behaviour,OrientarColor_behaviour],params,BlobColor.RED)

    #Se crea una lista de comportamientos
    threads = [BuscarColor_behaviour,OrientarColor_behaviour,MoverseColor_behaviour]

    #Inciamos los comportamientos
    BuscarColor_behaviour.start()
    OrientarColor_behaviour.start()
    MoverseColor_behaviour.start()

    while not params["stop"]:
        time.sleep(0.1)


    for thread in threads:
        thread.join()

    rob.disconnect()




if __name__ == "__main__":
    main()
