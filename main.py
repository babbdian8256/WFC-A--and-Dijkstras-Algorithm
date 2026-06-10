import pygame
import sys

from WFCSystem import WFCSystem
from Tile import Tile
from DijkstraPathfinder import DijkstraPathfinder
from AStarPathFinder import AStarPathfinder

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WFC Fixed")

clock = pygame.time.Clock()


def load(path):
    img = pygame.image.load(path)
    return pygame.transform.scale(img, (10, 10))


forestIMG = load("images/forest.jpg")
grassIMG = load("images/grass.jpg")
sandIMG = load("images/sand.jpg")
mountainIMG = load("images/mountain.jpg")
oceanIMG = load("images/ocean.jpg")
seaIMG = load("images/sea.jpg")


forest = Tile(0, 0, forestIMG, 1)
grass = Tile(0, 0, grassIMG, 0)
sand = Tile(0, 0, sandIMG, 0)
mountain = Tile(0, 0, mountainIMG, 2)
ocean = Tile(0, 0, oceanIMG, 2)
sea = Tile(0, 0, seaIMG, 1)


forest.AddAdjacentTile(forest)
forest.AddAdjacentTile(grass)
forest.AddAdjacentTile(mountain)

grass.AddAdjacentTile(grass)
grass.AddAdjacentTile(forest)
grass.AddAdjacentTile(sand)

sand.AddAdjacentTile(sand)
sand.AddAdjacentTile(grass)
sand.AddAdjacentTile(sea)

sea.AddAdjacentTile(sea)
sea.AddAdjacentTile(sand)
sea.AddAdjacentTile(ocean)

ocean.AddAdjacentTile(ocean)
ocean.AddAdjacentTile(sea)

mountain.AddAdjacentTile(mountain)
mountain.AddAdjacentTile(forest)

superTiles = [forest, grass, sand, mountain, ocean, sea]

wfc = WFCSystem(50, 50, superTiles)
wfc.SetTileSizeAndOffsetGrid(10,10,50,50)
wfc.InitWFC()

dijkstra = DijkstraPathfinder(wfc)

astar = AStarPathfinder(wfc)

frame = 0

running = True
while running:
    clock.tick(800)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    wfc.DoWFC()



    screen.fill((30, 30, 30))
    wfc.DrawGrid(screen)

    if event.type == pygame.MOUSEBUTTONDOWN:
        dijkstra.HandleClick(pygame.mouse.get_pos(), event.button)
        astar.HandleClick(pygame.mouse.get_pos(), event.button)
    dijkstra.Step()
    dijkstra.Draw(screen)

    astar.Step()
    astar.Draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()