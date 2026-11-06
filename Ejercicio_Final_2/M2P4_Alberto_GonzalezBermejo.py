from robobopy.Robobo import Robobo
from robobopy.utils.Wheels import Wheels

#Formula para obtener la distacia en cm
def calcular_distance_cm(rob: Robobo, wheel_perimeter = 20.5):
        degrees = (rob.readWheelPosition(Wheels.L) + rob.readWheelPosition(Wheels.R))/2
        cm = (degrees/360) * wheel_perimeter
        return cm


#el robot se mueve recto y leyendo los QR hasta encontrar el segundo poste 
def mover_recto(rob: Robobo,speed,qr_id1,qr_id2):
    rob.moveWheels(speed,speed)
    primerQR = True
    while rob.readQR().id != qr_id2:
        rob.wait(0.1)
        if rob.readQR().id == qr_id1 and primerQR:
            print("Primer QR visto")
            rob.resetWheelEncoders()
            primerQR = False
    rob.stopMotors()



def main():
    rob = Robobo("localhost")
    rob.connect()
    speed = 10
    qr_id1= '1'
    qr_id2= '2'
    rob.moveTiltTo(90,speed)
    rob.movePanTo(-90,speed)

    mover_recto(rob,speed,qr_id1,qr_id2)
    distancia = calcular_distance_cm(rob)
    rob.movePanTo(90,20)
    print(f"La distacia entre QR es de {distancia}")


    rob.disconnect()


if __name__ == "__main__":
    main()