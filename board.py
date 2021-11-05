import random
import time
from itertools import cycle

from boardGenerator import GOLBoard, NormalBoard
from tile import Tile

from tkinter import messagebox

DEBUG_FLAG = False


class Board:
    """Board object used for management and generation of tiles"""
    def __init__(self, frame, height, width, insect_count, seed, if_gol, tile_imgs, scaling, timer, insectsLeftFnc):
        self.frame = frame
        self.height = height
        self.width = width
        self.seed = seed
        self.tile_imgs = tile_imgs

        self.tile_array = None

        self.time = 0
        self.last_frame_time = 0
        self.timer_fnc = timer
        self.reset_timer = True
        self.stop_timer = False

        # variable for showing insects left on the board (aka amount of flags a player has to put on board)
        # used for updating string variable on the board
        self.insect_count = insect_count
        # real count of insects that has not been flagged yet
        self.insects_left = insect_count
        self.insectsLeftFnc = insectsLeftFnc

        self.insect_list = ["honeybee", "ladybug", "ant", "bug"]
        self.asset_data = [self.tile_imgs, self.insect_list]

        self.generateNormalBoard(scaling, if_gol)
        self.updateBoardUI(scaling)

    def generateTestNumbers(self, scaling):
        self.tile_array = [[Tile(self.frame, y, x, str((x % 8) + 1), self.asset_data, scaling)
                            for x in range(self.width)] for y in range(self.height)]
        self.bindBoardEvents()

    def generateTestInsects(self, scaling):
        self.tile_array = [[Tile(self.frame, y, x, insect, self.asset_data, scaling)
                            for x, insect in zip(range(self.width), cycle(self.insect_list))]
                           for y in range(self.height)]
        self.bindBoardEvents()

    def generateNormalBoard(self, scaling, if_gol=False):
        if if_gol:
            raw_array, self.insect_count = GOLBoard(self.height, self.width, self.insect_count,
                                                    self.seed).generateFinalBoard()
        else:
            raw_array, self.insect_count = NormalBoard(self.height, self.width, self.insect_count,
                                                       self.seed).generateFinalBoard()
        self.insects_left = self.insect_count
        self.populateWithNumbers(raw_array, scaling)
        self.bindBoardEvents()

    def populateWithNumbers(self, raw_array, scaling):
        """inserting numbers neighboring the insects in the raw_array with only insect data"""
        for y in range(self.height):
            for x in range(self.width):
                if raw_array[y][x] == -1:
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            # checking bounds
                            if 0 <= y + i < self.height and 0 <= x + j < self.width:
                                # checking if not insect
                                if raw_array[y + i][x + j] != -1:
                                    raw_array[y + i][x + j] += 1

        self.addCanvasToTiles(raw_array, scaling)

    def addCanvasToTiles(self, raw_array, scaling):
        """inserting canvas to tiles from final raw_array data"""
        self.tile_array = []
        self.insects_left = 0
        for y in range(self.height):
            tmp = []
            # generator returning random insect name from insect_list used for inserting appropriate canvas
            insect_generator = (random.choice(self.insect_list) for _ in iter(int, 1))
            for x, insect in zip(range(self.width), insect_generator):
                if raw_array[y][x] == -1:
                    tile = Tile(self.frame, y, x, insect, self.asset_data, scaling)
                    self.insects_left += 1
                elif raw_array[y][x] == 0:
                    tile = Tile(self.frame, y, x, "tile_clear", self.asset_data, scaling)
                else:
                    tile = Tile(self.frame, y, x, str(raw_array[y][x]), self.asset_data, scaling)
                tmp.append(tile)
            self.tile_array.append(tmp)

    def bindBoardEvents(self):
        """binding events to every tile on the board"""
        assert self.tile_array
        for x in self.tile_array:
            for y in x:
                y.tile.bind("<Button-1>", lambda _, y=y: self.uncoverCheck(y))
                if DEBUG_FLAG:
                    y.tile.bind("<Button-2>", lambda _, y=y: self.uncoverAll())
                else:
                    y.tile.bind("<Button-2>", lambda _, y=y: self.flagTile(y))
                y.tile.bind("<Button-3>", lambda _, y=y: self.flagTile(y))

    def flagTile(self, tile):
        """changing states of not uncovered tile"""
        # timer start
        if self.reset_timer:
            self.reset_timer = False
            self.last_frame_time = time.time()
            self.timer_fnc()

        if tile.status == "covered":
            if self.insect_count > 0:
                self.insect_count -= 1
                if tile.tile_name in self.insect_list:
                    self.insects_left -= 1
                tile.status = "flagged"
        elif tile.status == "flagged":
            self.insect_count += 1
            if tile.tile_name in self.insect_list:
                self.insects_left += 1
            tile.status = "questioned"
        elif tile.status == "questioned":
            tile.status = "covered"
        tile.updateUI()
        self.insectsLeftFnc(self.insect_count)
        # win condition can be only achieved by flagging all insects
        if self.insects_left == 0:
            self.winGame()

    def uncoverCheck(self, tile):
        """uncover tile logic"""
        # timer start
        if self.reset_timer:
            self.reset_timer = False
            self.last_frame_time = time.time()
            self.timer_fnc()

        if tile.tile_name == "tile_clear":
            self.uncoverClear(tile)
        elif tile.status == "uncovered" and tile.tile_name in [str(x) for x in range(1, 10)]:
            # right mouse btn functionality on uncovered tiles aka. uncovering neighbors if there is equal amount of
            # flags as the number
            neighbors = []
            flag_count = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= tile.y + i < self.height and 0 <= tile.x + j < self.width and not (
                            i == 0 and j == 0):
                        if self.tile_array[tile.y + i][tile.x + j].status == "flagged":
                            flag_count += 1
                        else:
                            neighbors.append(self.tile_array[tile.y + i][tile.x + j])
            if int(tile.tile_name) == flag_count:
                for x in neighbors:
                    # uncovered neighbors need to also uncover all clear tiles
                    self.uncoverClear(x, True)
        elif tile.status == "covered":
            # uncover hidden mines, numbers only when tile is not flagged or questioned or uncovered
            tile.uncover()
            if tile.tile_name in self.insect_list:
                self.loseGame()
        self.insectsLeftFnc(self.insect_count)

    def uncoverClear(self, tile, insect_check=False):
        """checking if there are any adjacent clear tiles and uncovering them"""
        stack = [tile]
        visited = set()
        while len(stack) > 0:
            tmp_tile = stack.pop()
            if tmp_tile.tile_name == "tile_clear" and tmp_tile not in visited:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if 0 <= tmp_tile.y + i < self.height and 0 <= tmp_tile.x + j < self.width and not (
                                i == 0 and j == 0):
                            stack.append(self.tile_array[tmp_tile.y + i][tmp_tile.x + j])
                visited.add(tmp_tile)
            if tmp_tile.status == "flagged":
                self.insect_count += 1
            if insect_check:
                # checking if the tile uncovered is an insect
                if tmp_tile.tile_name in self.insect_list:
                    self.loseGame()
            tmp_tile.uncover()
            tmp_tile.updateUI()

    def updateBoardUI(self, scaling):
        self.insectsLeftFnc(self.insect_count)
        for x in self.tile_array:
            for y in x:
                y.loadImages(scaling)
                y.updateUI()

    def uncoverAll(self):
        for x in self.tile_array:
            for y in x:
                y.uncover()
                y.updateUI()

    def winGame(self):
        self.stop_timer = True
        self.uncoverAll()
        messagebox.showinfo("Victory", "You won!")

    def loseGame(self):
        self.stop_timer = True
        self.uncoverAll()
        messagebox.showinfo("Defeat", "You lost!")

    def destroy(self):
        """destruction and cleanup of the Board object"""
        for x in self.tile_array:
            for y in x:
                y.destroy()
