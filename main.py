# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import A_Espia
import A_Guardia
from time import sleep
from random import randint


def newMap():
    print('NOTA: No cuentan los límites para las cantidades que ingreses')
    print('NOTA: Usar mapas mayores a 4x4')
    print('NOTA: No usar más obstaculos de los que el mapa puede aceptar [(x*y)-10]')
    print()
    badDimensions = True
    while badDimensions:
        x = int(input('Cuántas columnas quieres en el mapa? ')) + 2
        y = int(input('Cuántas filas quieres en el mapa? ')) + 2
        if x > 6 and y > 6:
            badDimensions = False
        else:
            print('NOTA: Usar mapas mayores a 4x4')

    manyObstacles = True
    while manyObstacles:
        obstacles = int(input('Cuántos obstáculos quieres? '))
        maxObst = ((x-2)*(y-2))-10
        if obstacles <= maxObst:
            manyObstacles = False
        else:
            print('NOTA: No usar más obstaculos de los que el mapa puede aceptar [(x*y)-10]')

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

    for o in range(obstacles):
        o_x = randint(1, x - 2)
        o_y = randint(1, y - 2)
        mapa[o_y][o_x] = '+'

    # Tesoro
    t_x = 1
    t_y = 1
    while (t_x == 1 and t_y == 1)\
            or (t_x == 1 and t_y == 2)\
            or (t_x == 2 and t_y == 1)\
            or (t_x == 2 and t_y == 2):
        t_x = randint(1, x - 2)
        t_y = randint(1, y - 2)
    mapa[t_y][t_x] = '$'

    #Carcel
    imposiblePrison = True
    while imposiblePrison:
        c_x = randint(1, x - 2)
        c_y = randint(1, y - 2)
        if (c_x != t_x or c_y != t_y)\
                and (c_x != 1 and c_y != 1) \
                and (c_x != 1 and c_y != 2) \
                and (c_x != 2 and c_y != 1) \
                and (c_x != 2 and c_y != 2):
            mapa[c_y][c_x] = 'C'
        else:
            continue

        c_env = [0, 0, 0, 0]
        c_env[0] = mapa[c_y - 1][c_x]
        c_env[1] = mapa[c_y][c_x + 1]
        c_env[2] = mapa[c_y + 1][c_x]
        c_env[3] = mapa[c_y][c_x - 1]

        for index in range(4):
            element = c_env[index]
            if element == ' ':
                c_env[index] = 0
            elif element == '+' or element == '|' or element == '=' or element == '$':
                c_env[index] = 1
            else:
                print('Revisa tus caracteres')

        if c_env.count(0) >= 2:
            imposiblePrison = False
        else:
            mapa[c_y][c_x] = ' '

    #Guardias
    c_env[0] = mapa[c_y - 1][c_x]
    c_env[1] = mapa[c_y][c_x + 1]
    c_env[2] = mapa[c_y + 1][c_x]
    c_env[3] = mapa[c_y][c_x - 1]

    contadorGuardias = 0
    if c_env[0] == ' ':
        if contadorGuardias < 2:
            mapa[c_y - 1][c_x] = 'G'
            if contadorGuardias < 1:
                g1_coord = [c_y - 1, c_x]
            else:
                g2_coord = [c_y - 1, c_x]
            contadorGuardias += 1
    if c_env[1] == ' ':
        if contadorGuardias < 2:
            mapa[c_y][c_x + 1] = 'G'
            if contadorGuardias < 1:
                g1_coord = [c_y, c_x + 1]
            else:
                g2_coord = [c_y, c_x + 1]
            contadorGuardias += 1
    if c_env[2] == ' ':
        if contadorGuardias < 2:
            mapa[c_y + 1][c_x] = 'G'
            if contadorGuardias < 1:
                g1_coord = [c_y + 1, c_x]
            else:
                g2_coord = [c_y + 1, c_x]
            contadorGuardias += 1
    if c_env[3] == ' ':
        if contadorGuardias < 2:
            mapa[c_y][c_x - 1] = 'G'
            if contadorGuardias < 1:
                g1_coord = [c_y, c_x - 1]
            else:
                g2_coord = [c_y, c_x - 1]
            contadorGuardias += 1

    #Abrir paso al espía que siempre inicia en 0,1
    mapa[1][1] = ' '
    mapa[1][2] = ' '
    mapa[2][1] = ' '
    mapa[2][2] = ' '

    #Espía
    mapa[0][1] = 'E'

    return mapa, g1_coord, g2_coord


def printMap(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            print(map[i][j], end=' ')
        print()


mapa = [
    ['=', 'E', '=', '=', '=', '=', '=', '=', '=', '='],
    ['|', ' ', ' ', ' ', ' ', ' ', '+', 'G', 'C', '|'],
    ['|', ' ', ' ', ' ', ' ', '+', ' ', ' ', 'G', '|'],
    ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|'],
    ['|', '+', ' ', ' ', ' ', ' ', ' ', ' ', '+', '|'],
    ['|', '+', ' ', '$', ' ', ' ', ' ', '+', ' ', '|'],
    ['|', '+', '+', '+', ' ', ' ', ' ', ' ', ' ', '|'],
    ['=', '=', '=', '=', '=', '=', '=', '=', '=', '=']
]

def menu():
    print('''    
    1. Reactivo
    2. Colaborativo
    3. Crear mapa
    4. Salir

    ''')
    seleccion = input('Selecciona la opción que deseas: ')

    if seleccion == '1':
        mapa, g1_pos, g2_pos = newMap()
        return 'reactivo', mapa, g1_pos, g2_pos
    elif seleccion == '2':
        mapa, g1_pos, g2_pos = newMap()
        return 'colaborativo', mapa, g1_pos, g2_pos
    elif seleccion == '3':
        mapa, g1_pos, g2_pos = newMap()
        printMap(mapa)
        a = A_Espia.A_Espia(mapa, 'reactivo')
        printMap(a.agentMap)
        return 0, 0, 0, 0
    else:
        return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Welcome to the game')

    mode, map, g1_pos, g2_pos = menu()
    if mode != 0:
        a = A_Espia.A_Espia(map, mode)
        g = A_Guardia.A_Guardia(map, g1_pos, mode)
        g2 = A_Guardia.A_Guardia(map, g2_pos, mode)
        printMap(map)

        print('Última escena')
        sleep(1)
        simulationNotFinished = True
        capturedMove = False

        while simulationNotFinished:
            simulationNotFinished = a.isAlive(capturedMove)
            if not simulationNotFinished:
                break
            if isinstance(simulationNotFinished, list):
                capturedMove = simulationNotFinished
            capturedMove = g.isAlive(capturedMove)
            capturedMove = g2.isAlive(capturedMove)
            if capturedMove == -1:
                print('El espía fue capturado y llegó a la celda')
                simulationNotFinished = False

        print('Mapa del espía:')
        printMap(a.agentMap)
