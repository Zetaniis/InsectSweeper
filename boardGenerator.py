import random

# INSECT as -1
# BLANK TILE as 0


class NormalBoard:
    """generation of array with insects using random.choices, exact number of insects not guaranteed"""
    def __init__(self, height, width, insect_count, seed):
        self.height = height
        self.width = width
        self.insect_count = insect_count
        self.seed = seed
        self.tile_array = None
        self.final_insect_count = 0
        if self.seed:
            random.seed(self.seed)

    def generateFinalBoard(self):
        self.generateRandBoard()
        return self.tile_array, self.final_insect_count

    def generateRandBoard(self):
        population = [0, -1]
        weights = [1 - (self.insect_count/(self.width*self.height)), self.insect_count/(self.width*self.height)]
        self.tile_array = [[random.choices(population, weights)[0] for _ in range(self.width)] for _ in range(self.height)]
        for x in self.tile_array:
            self.final_insect_count += x.count(-1)


class GOLBoard:
    """generation of array with insects using random.choices with 10 step of Conway's game of life, high variability
    in the number of insects """
    def __init__(self, height, width, insect_count, seed):
        self.height = height
        self.width = width
        self.insect_count = insect_count
        self.seed = seed
        self.tile_array = None
        self.final_insect_count = 0
        if self.seed:
            random.seed(self.seed)

    def generateFinalBoard(self):
        self.generateRandBoard()
        for _ in range(10):
            self.step()
        return self.tile_array, self.final_insect_count

    def generateRandBoard(self):
        population = [0, -1]
        weights = [1 - (self.insect_count/(self.width*self.height)), self.insect_count/(self.width*self.height)]
        self.tile_array = [[random.choices(population, weights)[0] for _ in range(self.width)] for _ in range(self.height)]
        for x in self.tile_array:
            self.final_insect_count += x.count(-1)

    def step(self):
        tmp_array = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                nCount = self.neighbourCount(x, y)
                if self.tile_array[y][x] == -1 and (nCount == 3 or nCount == 2):
                    tmp_array[y][x] = 0
                elif self.tile_array[y][x] == 0 and nCount == 3:
                    tmp_array[y][x] = -1
                else:
                    tmp_array[y][x] = self.tile_array[y][x]
        self.tile_array = tmp_array

    def neighbourCount(self, x, y):
        count = 0
        for i in range(0, 3):
            for j in range(0, 3):
                hor = (i+x+self.width-1)%self.width
                ver = (j+y+self.height-1)%self.height
                count -= self.tile_array[ver][hor]
        count += self.tile_array[y][x]
        return count

