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


class A_Espia:
    # Estados:
    # 0 | libre         | ' '
    # 1 | obstáculo     |  + or '|' or '='
    # 2 | ya explorado  |  #
    # 3 | guardia       |  G
    # 4 | tesoro        |  $
    # 5 | cárcel        |  C
    # 6 | entrada       |  V
    def __init__(self, originalMap, mode):
        self.workingMap = originalMap
        print('El agente está vivoooo')

        # Almacena los estados en las 4 direcciones (arriba, derecha, abajo, izquierda)
        self.environment = [0, 0, 0, 0]
        # Almacena la posición donde entró el agente y,x
        self.startPosition = [0, 1]
        # Almacena la posición del agente y,x
        self.position = [0, 1]
        # Almacena la posición anterior del agente y,x
        self.pastPosition = [0, 1]
        # Almacena el último movimiento realizado, en caso de tener que regresar puede usar esta variable. Str vacío porque no se puede vacía
        self.lastMovement = ''
        # Bandera para saber si tiene el artefacto/tesoro o no
        self.hasTreasure = False
        # Caracteres por los que se puede mover, cuando tiene el artefacto solo puede moverse por el camino que ya
        # recorrió e intercambiamos los caracteres
        self.allowedPath = ' '
        self.blockedPath = '#'
        # Guarda el modo de simulación
        self.mode = mode
        # El espía y siguiendo al guardia quedaron atrapados, se hace un switch de lugares
        self.willSwitchPlaces = False
        # Primer turno que es capturado se salta para que le envíe las coordenadas al otro guardia
        self.fighting = True
        # Variable que alterna la prioridad entre ejes en la función moveTo() para evitar un ciclo infinito entre dos lugares
        self.moveToPriority = 'y'
        # Donde se el agente construye su mapa
        self.agentMap = self.createBlankMap()

        #self.isAlive()

    def isAlive(self, capturedMove):
        if self.hasTreasure and not capturedMove:
            if self.startPosition == self.position:
                print('El espía salió con el tesoro')
                return False  #False para salir el búcle principal "simulationNotFinished"
            self.moveTo(self.startPosition)
            self.printMap(self.workingMap)
            return True

        if capturedMove:
            if capturedMove == -1:  #Fin de simulación por capturado y llegar a la celda
                return False
            elif capturedMove == 'switchPlaces':
                self.switchPlaces()
                return self.pastPosition
            elif capturedMove == 'switched':
                return True
            elif capturedMove == 'die' or capturedMove == 'captured' or (self.mode == 'colaborativo' and self.fighting):
                self.fighting = False
                return capturedMove
            else:
                if self.hasTreasure:
                    self.allowedPath, self.blockedPath = self.blockedPath, self.allowedPath
                    self.hasTreasure = False
                self.moveOneTo(capturedMove)
                self.printMap(self.workingMap)
                return capturedMove
        self.randomDirection()
        self.workingMap[0][1] = 'V'
        self.printMap(self.workingMap)
        return True #True para continuar en el búcle

    def printMap(self, map):
        sleep(.5)
        clear()
        for i in range(len(map)):
            for j in range(len(map[i])):
                print(map[i][j], end=' ')
            print()

    def createBlankMap(self):
        y = len(self.workingMap)
        x = len(self.workingMap[0])

        mapa = []

        for i in range(y):
            mapa.append([])
            for j in range(x):
                mapa[i].append(' ')

        for i in range(x):
            mapa[0][i] = '='
            mapa[y - 1][i] = '='

        for i in range(y):
            mapa[i][0] = '|'
            mapa[i][x - 1] = '|'

        return mapa

    def testEnv(self):
        print(' ', self.environment[0], ' ')
        print(self.environment[3], self.workingMap[self.position[0]][self.position[1]], self.environment[1])
        print(' ', self.environment[2], ' ')

    def randNum(self):
        num = random.randint(0, 3)
        return num

    def updateAgentMap(self):
        if self.agentMap[self.position[0] - 1][self.position[1]] == ' ':
            self.agentMap[self.position[0] - 1][self.position[1]] = self.workingMap[self.position[0] - 1][self.position[1]]
        if self.agentMap[self.position[0]][self.position[1] + 1] == ' ':
            self.agentMap[self.position[0]][self.position[1] + 1] = self.workingMap[self.position[0]][self.position[1] + 1]
        if self.agentMap[self.position[0] + 1][self.position[1]] == ' ':
            self.agentMap[self.position[0] + 1][self.position[1]] = self.workingMap[self.position[0] + 1][self.position[1]]
        if self.agentMap[self.position[0]][self.position[1] - 1] == ' ':
            self.agentMap[self.position[0]][self.position[1] - 1] = self.workingMap[self.position[0]][self.position[1] - 1]

        self.agentMap[self.position[0]][self.position[1]] = '#'

    def checkEnvironment(self):
        self.environment[0] = self.workingMap[self.position[0] - 1][self.position[1]]
        self.environment[1] = self.workingMap[self.position[0]][self.position[1] + 1]
        self.environment[2] = self.workingMap[self.position[0] + 1][self.position[1]]
        self.environment[3] = self.workingMap[self.position[0]][self.position[1] - 1]

        if not self.hasTreasure:
            self.updateAgentMap()

        isBounded = True

        for index in range(4):
            element = self.environment[index]
            if element == self.allowedPath:
                self.environment[index] = 0
            elif element == '+' or element == '|' or element == '=':
                self.environment[index] = 1
            elif element == self.blockedPath:  # Falta analizar
                self.environment[index] = 2
            elif element == 'G':
                self.environment[index] = 3
                if self.willSwitchPlaces:
                    return index
                return -3
            elif element == '$':
                self.environment[index] = 4
                return index
            elif element == 'C':
                self.environment[index] = 5
            elif element == 'V':
                self.environment[index] = 6
                if self.hasTreasure:
                    return index
            else:
                print('Revisa tus caracteres')

            #Si esta posición está en cero significa que hay camino por seguir
                #La expreción es True y entramos para settear la variable a False
            if isBounded and (self.environment[index] == 0):
                isBounded = False

        # self.testEnv()
        if isBounded:
            return -2 #Está encerrado y debe regresar un turno para retomar el curso
        else:
            return -1 #Puede moverse y tomará un camino aleatorio

    def agentBounded(self):
        if self.lastMovement == 0:
            return 2
        elif self.lastMovement == 1:
            return 3
        elif self.lastMovement == 2:
            return 0
        elif self.lastMovement == 3:
            return 1

    def clearPosition(self):
        self.pastPosition[0], self.pastPosition[1] = self.position[0], self.position[1]
        self.workingMap[self.position[0]][self.position[1]] = self.blockedPath

    def updatePosition(self):
        self.workingMap[self.position[0]][self.position[1]] = 'E'

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

    def switchPlaces(self):
        self.willSwitchPlaces = True
        nextMove = self.checkEnvironment()

        if nextMove == -2: #chance y se quita
            return True

        if nextMove == 0:
            self.moveUp()
        elif nextMove == 1:
            self.moveRight()
        elif nextMove == 2:
            self.moveDown()
        elif nextMove == 3:
            self.moveLeft()

        self.workingMap[self.pastPosition[0]][self.pastPosition[1]] = 'G'
        self.willSwitchPlaces = False

    def moveOneTo(self, position):
        self.updateAgentMap()
        if position[0] > self.position[0]:
            self.moveDown()
            self.lastMovement = 2
            return

        if position[0] < self.position[0]:
            self.moveUp()
            self.lastMovement = 0
            return

        # Manejo de coordenada x [y, x]
        if position[1] > self.position[1]:
            self.moveRight()
            self.lastMovement = 1
            return

        if position[1] < self.position[1]:
            self.moveLeft()
            self.lastMovement = 3
            return

    def moveTo(self, position):
        success = self.checkEnvironment()

        if success == -2:
            self.allowedPath, self.blockedPath = self.blockedPath, self.allowedPath
            self.checkEnvironment()
            self.allowedPath, self.blockedPath = self.blockedPath, self.allowedPath

        if success > -1:
            if success == 0:
                self.moveUp()
            elif success == 1:
                self.moveRight()
            elif success == 2:
                self.moveDown()
            elif success == 3:
                self.moveLeft()
            return

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
        self.randomDirection()
        return True

    def randomDirection(self):
        impossibleMove = True
        willGetTreasure = False
        wasBounded = False

        nextMove = self.checkEnvironment()

        if nextMove == -3:
            return

        if nextMove > -1:
            impossibleMove = False
            willGetTreasure = True

        if nextMove == -2:
            self.allowedPath, self.blockedPath = self.blockedPath, self.allowedPath
            self.checkEnvironment()
            wasBounded = True

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

        if wasBounded:
            self.allowedPath, self.blockedPath = self.blockedPath, self.allowedPath
            self.workingMap[self.pastPosition[0]][self.pastPosition[1]] = self.blockedPath

        if willGetTreasure:
            self.hasTreasure = True
            self.allowedPath, self.blockedPath = self.blockedPath, self.allowedPath
