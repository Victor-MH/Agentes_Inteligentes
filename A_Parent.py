import random

class A_Parent:
    def randNum(self):
        num = random.randint(0, 3)
        return num

    def printMap(self, map):
        for i in range(len(map)):
            for j in range(len(map[i])):
                print(map[i][j], end=' ')
            print()