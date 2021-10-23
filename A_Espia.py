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


class A_Espia():
    #Estados:
        #0 | libre         | ' '
        #1 | obstáculo     |  + or '|' or '='
        #2 | ya explorado  |
        #3 | guardia       |  G
        #4 | tesoro        |  $
        #5 | cárcel        |  C
    def __init__(self, originalMap):
        self.originalMap = tuple(originalMap)
        self.workingMap = originalMap
        print('El agente está vivoooo')

        # Almacena los estados en las 4 direcciones (arriba, derecha, abajo, izquierda)
        self.environment = [0, 0, 0, 0]
        # Almacena la posición del agente y,x
        self.position = [0, 1]
        # Almacena la posición donde entró el agente y,x
        self.startPosition = [0, 1]
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

        for index in range(4):
            element = self.environment[index]
            if element == self.allowedPath:
                self.environment[index] = 0
            elif element == '+' or element == '|' or element == '=':
                self.environment[index] = 1
            elif element == self.blockedPath:   #Falta analizar
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

        #self.testEnv()
        return -1

    def clearPosition(self):
        self.workingMap[self.position[0]][self.position[1]] = self.blockedPath
        pass

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
        if nextMove != -1:
            impossibleMove = False
            willGetTreasure = True

        while impossibleMove:
            nextMove = self.randNum()
            if self.environment[nextMove] == 0:
                impossibleMove = False

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
