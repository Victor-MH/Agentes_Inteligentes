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
    # 2 | ya explorado  |
    # 3 | guardia       |  G
    # 4 | tesoro        |  $
    # 5 | cárcel        |  C
    def __init__(self, originalMap):
        self.originalMap = tuple(originalMap)
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
        # Donde se el agente construye su mapa
        self.agentMap = [
            ['=', 'E', '=', '=', '=', '=', '=', '='],
            ['|', ' ', ' ', ' ', ' ', ' ', ' ', '|'],
            ['|', ' ', ' ', ' ', ' ', ' ', ' ', '|'],
            ['|', ' ', ' ', ' ', ' ', ' ', ' ', '|'],
            ['|', ' ', ' ', ' ', ' ', ' ', ' ', '|'],
            ['=', '=', '=', '=', '=', '=', '=', '=']
        ]

        self.isAlive()

    def isAlive(self):
        while True:
            if self.hasTreasure and self.startPosition == self.position:
                print('El espía salió con el tesoro')
                break
            self.randomDirection()
            sleep(1)
            clear()
            self.printMap(self.workingMap)

    def printMap(self, map):
        for i in range(len(map)):
            for j in range(len(map[i])):
                print(map[i][j], end=' ')
            print()

    def testEnv(self):
        print(' ', self.environment[0], ' ')
        print(self.environment[3], self.workingMap[self.position[0]][self.position[1]], self.environment[1])
        print(' ', self.environment[2], ' ')

    def randNum(self):
        num = random.randint(0, 3)
        return num

    def updateAgentMap(self):
        self.agentMap[self.position[0] - 1][self.position[1]] = self.workingMap[self.position[0] - 1][self.position[1]]
        self.agentMap[self.position[0]][self.position[1] + 1] = self.workingMap[self.position[0]][self.position[1] + 1]
        self.agentMap[self.position[0] + 1][self.position[1]] = self.workingMap[self.position[0] + 1][self.position[1]]
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
            elif element == '$':
                self.environment[index] = 4
                return index
            elif element == 'C':
                self.environment[index] = 5
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
        self.pastPosition = self.position
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

    def randomDirection(self):
        impossibleMove = True
        willGetTreasure = False

        nextMove = self.checkEnvironment()
        if nextMove > -1:
            impossibleMove = False
            willGetTreasure = True

        # TODO What happens when spy gets blocked by his path and not even going back is enough?
        if nextMove == -2:
            impossibleMove = False
            nextMove = self.agentBounded()

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

        if willGetTreasure:
            self.hasTreasure = True
            self.allowedPath, self.blockedPath = self.blockedPath, self.allowedPath
