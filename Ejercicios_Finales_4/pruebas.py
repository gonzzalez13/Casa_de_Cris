from robobopy.Robobo import Robobo
from robobopy.utils.IR import IR
import numpy as np

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


def turn_left(rob: Robobo,goal_angle):
    speed_Rudeas = 20
    rob.moveWheels(speed_Rudeas,0)
    if goal_angle < -180:
        goal_angle = goal_angle + 360
        while -180 <= rob.readOrientationSensor().yaw <= 0:
            rob.wait(0.001)
    while rob.readOrientationSensor().yaw > goal_angle:
        rob.wait(0.001)


# def turn_left(rob:Robobo,goal_angle):
#     speed_Ruedas = 20
#     print ("velocidad de giro: ", speed_Ruedas)
#     rob.moveWheels(speed_Ruedas,0)
#     # Si pasa de -180º --> continua en 180, 179, ...
#     if goal_angle < -180:
#         goal_angle = goal_angle + 360
#         while -180 <= rob.readOrientationSensor().yaw <= 0:
#             rob.wait(0.001)
#     while rob.readOrientationSensor().yaw > goal_angle:
#         rob.wait(0.001)


def turn_degrees(rob:Robobo,angle,state):
    orientation = rob.readOrientationSensor()
    # Se parte de la posición actual y se suman los grados a girar
    goal_angle = orientation.yaw + angle
    # giro a la derecha de pendiendo de la posicion del color detectado se ajusta en su direccion
    if state == 1:
        turn_right(rob,goal_angle)
    # giro a la izquierda
    else:
        turn_left(rob,goal_angle)
    rob.stopMotors()

def main():
    rob = Robobo("localhost")
    rob.connect()
    qtable = np.array([
                [0,0,0],
                [0,0,0],
                [0,0,0]
            ])


    while True:
        rob.wait(0.1)

        if rob.readIRSensor(IR.FrontC)<= rob.readIRSensor(IR.FrontLL) and  rob.readIRSensor(IR.FrontC)<= rob.readIRSensor(IR.FrontRR):
            state = 0
        elif rob.readIRSensor(IR.FrontRR)<= rob.readIRSensor(IR.FrontC) and  rob.readIRSensor(IR.FrontRR)<= rob.readIRSensor(IR.FrontLL):
            state = 1
        else:
            state = 2
        print("Estado: ", state)  

        if state == 0:
            rob.moveWheelsByTime(10,10,1)
        elif state == 1:
            turn_degrees(rob,40,state)
            #rob.moveWheelsByTime(10,-10,1)
        else:
            turn_degrees(rob,40,state)
            #rob.moveWheelsByTime(-10,10,1)
        qtable[state][state] += state 

        valor = np.argmax(qtable[state])
        print("Valor: ", valor)
        print("Q-Table: ")
        print(qtable)
        rob.wait(0.1)


if __name__ == "__main__":
    main()

