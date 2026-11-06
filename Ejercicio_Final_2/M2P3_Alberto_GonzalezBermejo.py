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
    speed_Ruedas = 5
    rob.moveWheels(speed_Ruedas,0)
    # Si pasa de -180º --> continua en 180, 179, ...
    if goal_angle < -180:
        goal_angle = goal_angle + 360
        while -180 <= rob.readOrientationSensor().yaw <= 0:
            rob.wait(0.001)
    while rob.readOrientationSensor().yaw > goal_angle:
        rob.wait(0.001)


def turn_degrees(rob:Robobo,angle):
    orientation = rob.readOrientationSensor()
    # Se parte de la posición actual y se suman los grados a girar
    goal_angle = orientation.yaw + angle
    # giro a la derecha
    if angle > 0:
        turn_right(rob,goal_angle)
    # giro a la izquierda
    else:
        turn_left(rob,goal_angle)
    rob.stopMotors()


def mover_hasta_Pared(rob: Robobo, Pared, speed,Front):
    #El robot se mueve hasta que el sensor detecta la pared
    rob.moveWheels(speed,speed)
    while rob.readIRSensor(Front) < Pared:
        rob.wait(0.1)
    rob.stopMotors()
    

def mover_giro(rob: Robobo, Pared, speed,Front):
    #El robot se mueve hasta detectar la zona donde se va realizar el giro
    rob.moveWheels(speed,speed)
    while rob.readIRSensor(Front) > Pared:
        rob.wait(0.1)
    rob.stopMotors()


def color_detectado(rob: Robobo, color: BlobColor,speed):
    #el robot se mueve hasta tener en la posicion x el color 
    rob.moveWheels(speed,speed)
    rob.resetColorBlobs()
    i = True
    while i:
        if rob.readColorBlob(color).size > 0:
            while rob.readColorBlob(color).posx > 50:
                i = False
                rob.wait(0.1)
        else:
            rob.wait(0.1)
    rob.stopMotors()

def girar_Detectar_Color(rob: Robobo,color: BlobColor):
    rob.sayText("Voy a realizar el giro")
    centro = True
    rob.resetColorBlobs()
 
    while rob.readColorBlob(color).size == 0 :
       rob.wait(0.1)
       turn_degrees(rob,10)
          
    while centro:
        turn_degrees(rob,10)
        rob.wait(0.1)
        if  rob.readColorBlob(color).posx > 45 and rob.readColorBlob(color).posx < 55:
            rob.stopMotors()
            centro = False



def main():
    rob = Robobo("localhost")
    rob.connect()
    rob.setActiveBlobs(True,True,True,True)

    speed = 15
    ir_c = 60
    ir_L_BackL = 55
    IR_R_BackL = 20
    ir_c_Color = 30
    color = BlobColor.RED

    #El robot comienza a moverse y supera la pared
    mover_hasta_Pared(rob,ir_c,speed,IR.FrontC)
    rob.sayText("He detectado la pared")
    turn_degrees(rob,90)
    mover_giro(rob,ir_L_BackL,speed,IR.BackL)
    rob.sayText("Voy hacer el primer giro")
    turn_degrees(rob,-110)
    mover_hasta_Pared(rob,IR_R_BackL,speed,IR.BackL)
    rob.sayText("Ya he superado la pared")
    turn_degrees(rob,-70)

    #EL robot busca el globo y se acerca a el
    rob.moveTiltTo(90,speed)
    rob.movePanTo(90,speed)
    color_detectado(rob,color,speed)
    rob.sayText("He detectado el globo")
    rob.movePanTo(0,speed)
    girar_Detectar_Color(rob,color)
    #mover_hasta_Pared(rob,ir_c_Color,speed,IR.FrontC)


    rob.disconnect()



if __name__ == "__main__":
        main()