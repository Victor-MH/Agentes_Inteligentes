import random
from time import sleep
from os import system, name


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


class A_Guardia:
    def __init__(self, originalMap, startpos):
        self.originalMap = tuple(originalMap)
        self.workingMap = originalMap
        print('El guardia está vivoooo')

        # Almacena los estados en las 4 direcciones (arriba, derecha, abajo, izquierda)
        self.environment = [0, 0, 0, 0]
        # Almacena la posición donde entró el agente y,x
        self.startPosition = startpos  # 1,5 es donde lo tenia
        # Almacena la posición del agente y,x
        self.position = [startpos[0], startpos[1]]
        # Almacena la posición anterior del agente y,x
        self.pastPosition = [startpos[0], startpos[1]]
        # Almacena el último movimiento realizado, en caso de tener que regresar puede usar esta variable. Str vacío porque no se puede vacía
        self.lastMovement = ''
        # Caracteres por los que se puede mover, cuando captura al espía solo puede moverse por el camino que ya
        # recorrió e intercambiamos los caracteres
        self.allowedPath = ' '
        self.blockedPath = '#'
        # Variable que alterna la prioridad entre ejes en la función moveTo() para evitar un ciclo infinito entre dos lugares
        self.moveToPriority = 'y'
        # Guarda el modo de simulación
        self.mode = 'reactivo'
        # Espía capturado?
        self.spyCaptured = False
        # Tiempo entre turnos
        self.turnTime = .5

        #self.isAlive()

    def isAlive(self, capturedMove):
        if capturedMove and not self.spyCaptured:
            if self.position != self.startPosition:
                self.moveTo(self.startPosition)
            return capturedMove
        elif type(capturedMove) == 'list':
            self.moveTo(capturedMove)
            self.workingMap[self.pastPosition[0]][self.pastPosition[1]] = 'E'
            return 'switched'
        else:
            if self.spyCaptured:
                if self.position == self.startPosition:
                    sleep(self.turnTime)
                    return -1  # fin de simulación por espía capturado
                else:
                    switch = self.moveTo(self.startPosition)  # Ubicación de la celda
                    if switch == 'switchPlaces':
                        return 'switchPlaces'
                sleep(self.turnTime)
                clear()
                self.printMap(self.workingMap)
                return self.pastPosition
            else:
                spyCaptured = self.randomDirection()
                if spyCaptured:
                    sleep(self.turnTime)
                    clear()
                    self.printMap(self.workingMap)
                    return self.pastPosition
                else:
                    sleep(self.turnTime)
                    clear()
                    self.printMap(self.workingMap)
                    return False

        # Si queremos simular hilos múltiples y solo imprima el espía
        # sleep(self.turnTime
        # clear()
        # self.printMap(self.workingMap)

    def randNum(self):
        num = random.randint(0, 3)
        return num

    def printMap(self, map):
        for i in range(len(map)):
            for j in range(len(map[i])):
                print(map[i][j], end=' ')
            print()

    def clearPosition(self):
        self.pastPosition[0], self.pastPosition[1] = self.position[0], self.position[1]
        self.workingMap[self.position[0]][self.position[1]] = ' '

    def updatePosition(self):
        self.workingMap[self.position[0]][self.position[1]] = 'G'

    def moveUp(self):
        self.clearPosition()
        self.position[0] -= 1
        self.updatePosition()

    def moveRight(self):
        self.clearPosition()
        self.position[1] += 1
        self.updatePosition()

    def moveDown(self):
        self.clearPosition()
        self.position[0] += 1
        self.updatePosition()

    def moveLeft(self):
        self.clearPosition()
        self.position[1] -= 1
        self.updatePosition()

    def checkEnvironment(self):
        self.environment[0] = self.workingMap[self.position[0] - 1][self.position[1]]
        self.environment[1] = self.workingMap[self.position[0]][self.position[1] + 1]
        self.environment[2] = self.workingMap[self.position[0] + 1][self.position[1]]
        self.environment[3] = self.workingMap[self.position[0]][self.position[1] - 1]

        isBounded = True

        for index in range(4):
            element = self.environment[index]
            if element == self.allowedPath:
                self.environment[index] = 0
            elif element == '+' or element == '|' or element == '=' or element == ' V':
                self.environment[index] = 1
            elif element == self.blockedPath:  # Falta analizar
                # self.environment[index] = 2
                self.environment[index] = 0
            elif element == 'G':
                self.environment[index] = 3
            elif element == '$':
                self.environment[index] = 4
                # return index
            elif element == 'C':
                self.environment[index] = 5
            elif element == 'E':
                self.environment[index] = 6
                if not self.spyCaptured:
                    return -3
            else:
                print('Revisa tus caracteres')

            # Si esta posición está en cero significa que hay camino por seguir
            # La expresión es True y entramos para settear la variable a False
            if isBounded and (self.environment[index] == 0):
                isBounded = False

        #self.testEnv()
        if isBounded:
            return -2  # Está encerrado y debe regresar un turno para retomar el curso
        else:
            return -1  # Puede moverse y tomará un camino aleatorio


    def testEnv(self):
        print(' ', self.environment[0], ' ')
        print(self.environment[3], self.workingMap[self.position[0]][self.position[1]], self.environment[1])
        print(' ', self.environment[2], ' ')

    def moveTo(self, position):

        self.checkEnvironment()
        if position == self.position:
            return False

        # TODO Limpiar este código
        if self.moveToPriority == 'y':
            # Manejo de coordenada y [y, x]
            if position[0] > self.position[0]:
                if self.environment[2] == 0:
                    self.moveDown()
                    self.lastMovement = 2
                    self.moveToPriority = 'x'
                    return True

            if position[0] < self.position[0]:
                if self.environment[0] == 0:
                    self.moveUp()
                    self.lastMovement = 0
                    self.moveToPriority = 'x'
                    return True

            # Manejo de coordenada x [y, x]
            if position[1] > self.position[1]:
                if self.environment[1] == 0:
                    self.moveRight()
                    self.lastMovement = 1
                    self.moveToPriority = 'y'
                    return True

            if position[1] < self.position[1]:
                if self.environment[3] == 0:
                    self.moveLeft()
                    self.lastMovement = 3
                    self.moveToPriority = 'y'
                    return True
        elif self.moveToPriority == 'x':
            # Manejo de coordenada x [y, x]
            if position[1] > self.position[1]:
                if self.environment[1] == 0:
                    self.moveRight()
                    self.lastMovement = 1
                    self.moveToPriority = 'y'
                    return True

            if position[1] < self.position[1]:
                if self.environment[3] == 0:
                    self.moveLeft()
                    self.lastMovement = 3
                    self.moveToPriority = 'y'
                    return True

            # Manejo de coordenada y [y, x]
            if position[0] > self.position[0]:
                if self.environment[2] == 0:
                    self.moveDown()
                    self.lastMovement = 2
                    self.moveToPriority = 'x'
                    return True

            if position[0] < self.position[0]:
                if self.environment[0] == 0:
                    self.moveUp()
                    self.lastMovement = 1
                    self.moveToPriority = 'x'
                    return True

        # Ya que revisamos que no puede avanzar hacía las direcciones que le convienen va a moverse aleatoriamente hacía donde pueda
        # y con el cambio de prioridad en ejes evitamos que quede atrapado, y sigue buscando su objetivo
        switch = self.randomDirection()
        if switch == 'switchPlaces':
            return 'switchPlaces'
        return True

    def randomDirection(self):
        impossibleMove = True
        nextMove = self.checkEnvironment()

        # Espía capturado
        if nextMove == -3 and self.mode == 'reactivo' and not self.spyCaptured:
            self.spyCaptured = True
            self.moveTo(self.startPosition)  # Ubicación de la celda
            return True

        if nextMove == -2: #Está encerrado
            if self.spyCaptured: #Está encerrado pero puede cambiar de lugar con el espía para volver por donde llegaron
                return 'switchPlaces'
            return False

        while impossibleMove:
            nextMove = self.randNum()
            if self.environment[nextMove] == 0:
                impossibleMove = False

        self.lastMovement = nextMove

        if nextMove == 0:
            self.moveUp()
        elif nextMove == 1:
            self.moveRight()
        elif nextMove == 2:
            self.moveDown()
        elif nextMove == 3:
            self.moveLeft()

        return False
