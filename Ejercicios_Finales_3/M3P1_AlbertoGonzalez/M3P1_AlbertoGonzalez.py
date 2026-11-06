from robobopy.Robobo import Robobo
from robobopy.utils.IR import IR
from robobopy.utils.BlobColor import BlobColor


def turn_right(rob: Robobo,goal_angle):
    speed_Ruedas = 5
    rob.moveWheels(0, speed_Ruedas)
    # Si pasa de 180º --> continua en -180, -179, ...
    if goal_angle > 180:
        goal_angle = goal_angle - 360
        while 0 <= rob.readOrientationSensor().yaw <= 180:
            rob.wait(0.001)
    while round(rob.readOrientationSensor().yaw) < goal_angle:
        rob.wait(0.001)


def turn_left(rob:Robobo,goal_angle):
    speed_Ruedas = 15
    rob.moveWheels(speed_Ruedas,0)
    # Si pasa de -180º --> continua en 180, 179, ...
    if goal_angle < -180:
        goal_angle = goal_angle + 360
        while -180 <= rob.readOrientationSensor().yaw <= 0:
            rob.wait(0.001)
    while rob.readOrientationSensor().yaw > goal_angle:
        rob.wait(0.001)


def turn_degrees(rob:Robobo,angle,color: BlobColor):
    orientation = rob.readOrientationSensor()
    # Se parte de la posición actual y se suman los grados a girar
    goal_angle = orientation.yaw + angle
    # giro a la derecha de pendiendo de la posicion del color detectado se ajusta en su direccion
    if rob.readColorBlob(color).posx <= 40 and rob.readColorBlob(color).posx != 0:
        turn_right(rob,goal_angle)
    # giro a la izquierda
    else:
        turn_left(rob,goal_angle)
    rob.stopMotors()


def girar_Detectar_Color(rob: Robobo,color: BlobColor):
    centro = True
    rob.resetColorBlobs()
 
    while rob.readColorBlob(color).size == 0 :
       rob.wait(0.1)
       turn_degrees(rob,10,color)
          
    while centro:
        turn_degrees(rob,10,color)
        rob.wait(0.1)
        if  rob.readColorBlob(color).posx > 45 and rob.readColorBlob(color).posx < 52:
            print("DECTECTADO el color")
            rob.stopMotors()
            centro = False
        else:
            rob.wait(0.1)


def main ():
    rob = Robobo ("Localhost")
    rob.connect()
    rob.setActiveBlobs(True,True,True,True)


    goal = 100
    speed = 10
    kp = 0.5

    rob.moveTiltTo(90,speed)
    rob.movePanTo(0,speed)
    color = BlobColor.GREEN

# Gira el robot hasta encontrase delante del objeto en los grados deseados
    girar_Detectar_Color(rob,color)
# Utilizando el sensor delantero mide la velocidad y la ajusta para detenerse delante el objeto 
    while rob.readIRSensor(IR.FrontC) < goal:
        error = goal - rob.readIRSensor(IR.FrontC)
        speed = round(error * kp)
        rob.moveWheels(speed, speed)
        rob.wait(0.1)


    rob.stopMotors()
    rob.disconnect()



if __name__ == "__main__":
    main()