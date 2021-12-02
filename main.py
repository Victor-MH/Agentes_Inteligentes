# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import A_Espia
import A_Guardia
from time import sleep


def newMap():
    x = int(input('Cuántas columnas quieres en el mapa? '))
    y = int(input('Cuántas filas quieres en el mapa? '))
    obstacles = int(input('Cuántos obstáculos quieres? '))

    characters = ['+', 'T', 'G', 'C']
    mapa = []

    for i in range(y):
        mapa.append([])
        for j in range(x):
            mapa[i].append('*')

    for i in range(x):
        mapa[0][i] = '='
        mapa[y - 1][i] = '='

    for i in range(y):
        mapa[i][0] = '|'
        mapa[i][x - 1] = '|'

    return mapa


def printMap(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            print(map[i][j], end=' ')
        print()


mapa = [
    ['=', 'E', '=', '=', '=', '=', '=', '='],
    ['|', ' ', ' ', ' ', '+', 'G', 'C', '|'],
    ['|', ' ', ' ', ' ', ' ', ' ', 'G', '|'],
    ['|', '+', ' ', '$', ' ', '+', '+', '|'],
    ['|', '+', '+', '+', ' ', ' ', ' ', '|'],
    ['=', '=', '=', '=', '=', '=', '=', '=']
]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Welcome to the game')

    #mapa = newMap()
    #printMap(mapa)


    a = A_Espia.A_Espia(mapa)
    g = A_Guardia.A_Guardia(mapa, [2, 6])
    g2 = A_Guardia.A_Guardia(mapa, [1, 5])
    printMap(mapa)
    sleep(2)
    simulationNotFinished = True
    capturedMove = False

    while simulationNotFinished:
        simulationNotFinished = a.isAlive(capturedMove)
        capturedMove = g.isAlive(capturedMove)
        capturedMove = g2.isAlive(capturedMove)
        if capturedMove == -1:
            print('El espía fue capturado y llegó a la celda')
            simulationNotFinished = False

    printMap(a.agentMap)
