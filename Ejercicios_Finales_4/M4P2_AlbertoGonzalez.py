
from robobopy.Robobo import Robobo
from robobopy.utils.IR import IR
import numpy as np
from numpy.random import default_rng



class QLearningNav:
    def __init__(self):
        # Número de acciones
        self.actions_number = 3
        # Número de estados
        self.states_number = 3
        # Número de iteraciones del algoritmo durante el aprendizaje
        self.learning_iterations = 20
        # Indica si el robot está en fase aprendizaje (True) o ejecución (False)
        self.is_learning = True

        # Tasas de aprendizaje y descuento
        self.alpha = 0.4  
        self.gamma = 0.5

        # Ratio de exploración
        self.exporation_rate = 0.4  
        self.rng = default_rng()    

        # qtable : contiene los valores Q para cada par (estado, acción)
        self.qtable = np.zeros((self.states_number, self.actions_number))

        #Para los movimientos del robot
        self.speed = 10
        self.Limit_Wall = 120
        self.margin = 5
        self.robobo = Robobo("localhost")
        self.robobo.connect()

            
    def giroDerecha(self,goal_angle):
        speed_Ruedas = 5
        self.robobo.moveWheels(0, speed_Ruedas)
        # Si pasa de 180º --> continua en -180, -179, ...
        if goal_angle > 180:
            goal_angle = goal_angle - 360
            while 0 <= self.robobo.readOrientationSensor().yaw <= 180:
                self.robobo.wait(0.001)
        while round(self.robobo.readOrientationSensor().yaw) < goal_angle:
            self.robobo.wait(0.001)


    def giroIzquierda(self,goal_angle):
        speed_Ruedas = 5
        self.robobo.moveWheels(speed_Ruedas,0)
        # Si pasa de -180º --> continua en 180, 179, ...
        if goal_angle < -180:
            goal_angle = goal_angle + 360
            while -180 <= self.robobo.readOrientationSensor().yaw <= 0:
                self.robobo.wait(0.001)
        while round(self.robobo.readOrientationSensor().yaw) > goal_angle:
            self.robobo.wait(0.001)

 
    def turn_degrees(self, angle: float, state: int):
        orientation = self.robobo.readOrientationSensor()
        # Se parte de la posición actual y se suman los grados a girar
        goal_angle = orientation.yaw + angle
        # 
        if state == 1:
            self.giroDerecha(goal_angle)
        # giro a la izquierda
        else:
            self.giroIzquierda(goal_angle)
        self.robobo.stopMotors()


    def go_straight(self):
        """Avanzar recto hacia delante.
        Antes de realizar el movimiento, se comprueba y ajusta
        la posición si es necesario llamando a "do_correction."""
        self.robobo.moveWheelsByTime(self.speed,self.speed,1)

    def go_back(self):
        """Retroceder hacia atrás.
        Antes de realizar el movimiento, se comprueba y ajusta
        la posición si es necesario llamando a "do_correction."""
        self.robobo.moveWheelsByTime(-self.speed,-self.speed,1)

    def turn_right(self):
        """Girar a la derecha.
        Antes de realizar el movimiento, se comprueba """
        # Añadir el giro a la derecha
        self.turn_degrees(40, self.get_state())       

    def turn_left(self):
        """Girar a la izquierda. 
        Antes de realizar el movimiento, se comprueba y ajusta
        la posición si es necesario llamando a "do_correction."""
        # Añadir el giro a la izquierda
        self.turn_degrees(-40, self.get_state())
        #self.robobo.moveWheelsByTime(0,-5,1)
        

    def get_state(self):
        """
        Comprobar y devolver el estado actual del robot
        """ 

        self.robobo.wait(0.1)
        
        if self.robobo.readIRSensor(IR.FrontC)<= self.robobo.readIRSensor(IR.FrontLL) and self.robobo.readIRSensor(IR.FrontC)<= self.robobo.readIRSensor(IR.FrontRR):
            state = 0
        elif self.robobo.readIRSensor(IR.FrontRR)<= self.robobo.readIRSensor(IR.FrontC) and self.robobo.readIRSensor(IR.FrontRR)<= self.robobo.readIRSensor(IR.FrontLL):
            state = 1
        else:
            state = 2

        return state

    def get_action(self, state):
        """
        Devuelve la acción a realizar por el robot.
        Durante la fase de aprendizaje, se realizan movimientos aletorios en un 
        porcentaje de las acciones y en el resto se 
        """
        if self.is_learning:
            if self.rng.uniform() < self.exporation_rate:
                action_to_do = np.random.randint(0, self.actions_number)
            else:
                action_to_do = np.argmax(self.qtable[state])    
        else:
            action_to_do = np.argmax(self.qtable[state])

        print (f"Tabla Q: {self.qtable}")           

        return action_to_do

    def do_correction(self):
        """Comprueba si el robot se encuentra desviado de la trayectoria y, en caso afirmativo,
        realiza un movimiento de corrección.
        """
        Possible_movements = True

        if (self.robobo.readIRSensor(IR.FrontC) > self.Limit_Wall) or (
            self.robobo.readIRSensor(IR.FrontLL) > self.Limit_Wall) or (
            self.robobo.readIRSensor(IR.FrontRR) > self.Limit_Wall):


            self.go_back()
            self.turn_degrees(40,1)
            self.robobo.wait(0.1)
            Possible_movements = False

        return Possible_movements

    def move(self,action):
        """Realiza la acccion que recibe como parametro, si es posible realizar la accion"""

        possible_movements = self.do_correction()

        if possible_movements:
            if action == 0: # Avanzar recto
                self.go_straight()
            elif action == 1: # Girar a la derecha
                self.turn_right()
                self.go_straight()
            elif action == 2: # Girar a la izquierda
                self.turn_left()
                self.go_straight()

        return possible_movements

    def run(self):
        """En este método:
        1 - Se comprueba el estado en el que se encuentra el robot
        2 - Se obtiene de la tabla Q la mejor acción para este estado
        la mejor acción para diho estado de la tabla Q indefinidamente,
        el robot navega con una tabla Q existente. No se incluye el 
        proceso de aprendizaje."""

        self.is_learning = False
        while True:
            state = self.get_state()
            action = self.get_action(state)
            action_done = self.move(action)
            print(f"Estado: {state}, Acción: {action}")
            self.robobo.wait(0.1)

    def get_reward(self,state, action):
        """Cálculo de la recompensa. """     
        if action == state: 
            reward = 1
        else:
            reward = -1

        return reward

    def update_qtable(self,reward, state, action):
        """Actualiza la tabla Q a partir la recompensa obtenida para un estado y acción
        """
        self.qtable[state, action] = (
            (1.0 - self.alpha) * self.qtable[state,  action]) + self.alpha * (reward + (self.gamma * max(self.qtable[state])))        

    def learn(self):
        """Proceso de aprendizaje.
        Durante el aprendizaje:
            1 - Obtener estado actual
            2 - Obtener acción para el estado actual
            3 - Calcular la recompensa
            4 - Actualizar la tabla q
        """
        self.is_learning = True
        for iteration in range(self.learning_iterations):
            print(f'\nInteraction num: {iteration}')
            state = self.get_state()
            action = self.get_action(state)
            action_done = self.move(action)
            if action_done:
                reward = self.get_reward(state, action)
                self.update_qtable(reward, state, action)
                print(f"Estado: {state}, Acción: {action}, Recompensa: {reward}")
                print(f"Tabla Q: {self.qtable}")
            self.robobo.wait(0.01)           


    def learn_and_run(self):
        """Ejecuta el método de aprendizaje y, a continuación el 
        de ejecución, para que el robot siga navegando en base a 
        lo aprendido."""
        self.learn()
        self.run()

    def ejercicio1_test(self):
        state = self.get_state()
        print(f"Estado actual: {state}")
        self.go_straight()
        self.turn_right()
        #self.turn_left()        

    def ejercicio1_test2(self):
        """Realiza la navegación con una tabla Q creada
        manualmente. Este método tiene como objetivo probar
        los movimientos desarrollados para cada acción sobre
        una tabla Q con los pesos ideales, de forma que podemos
        ver que los movimimientos desarrollados funcionan adecuadamente.
        """
        # Sustituye los valores de la tabla por los valores que
        # has estabalecido como ideales.
        self.qtable = np.array([
            [1,0,0],
            [0,1,0],
            [0,0,1]
        ])  
        self.run()


if __name__ == "__main__":
    nav = QLearningNav()
    nav.learn_and_run()
