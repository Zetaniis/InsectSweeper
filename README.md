# Insect Sweeper
Minesweeper clone with 3 modes of difficulty, UI scaling and custom games feature. Mines are replaced with random insects that a player marks as biohazard.

## Features
- 3 difficulty modes
- custom game mode with adujstable width, height, insect count, seed and [generation mode](#generation-modes)
- changing UI scaling for 2 times and 4 times the original size
- normal left and right mouse button functionality of minesweeper

## Generation modes
There are two generation modes for insects:
- Normal - used by predifined difficulty modes, uses random.choices to generate insects for every tile. The exact number of insects is not guaranteed but close.
- Game of life - uses normal generation as a first step. Later uses 10 steps of Conway's game of life propagate the insects across the board. High variability in the number of insects on the board.

## Project structure
- [main.py](./main.py) - main window of tkinter, init of main UI elements, loading assets, handling timer and insect count UI elements
- [board.py](./board.py) - board object resposible for handling insectsweeper board, changing states of tiles 
- [tile.py](./tile.py) - tile object handling rendering of single tile on board
- [boardGenerator.py](./boardGenerator.py) - providing raw array data with insects to board object 

## Release
[Link to release](https://github.com/Zetaniis/InsectSweeper/releases)

## Packages
Main packages used in this application:
- [Pillow](https://pillow.readthedocs.io/en/stable/)
