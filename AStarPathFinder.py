import pygame
import math
import time

class AStarPathfinder:
    def __init__(self, wfc):
        self.wfc = wfc

        self.start = 0
        self.end = 0

        self.dist = {}
        self.prev = {}
        self.fscore = {}

        self.path = []
        self.processing = False

        self.start_time = 0
        self.end_time = 0
        self.elapsed_ms = 0

    # CLICK HANDLER
    def HandleClick(self, mouse_pos, button):
        tile = self.GetTileFromScreen(mouse_pos)

        if tile is None:
            return

        if button == 1:
            if tile.difficulty != 2:
                self.start = tile

        if button == 3:
            if tile.difficulty != 2:
                self.end = tile

        if self.start and self.end:
            self.StartSearch()

    def GetTileFromScreen(self, pos):
        mx, my = pos

        x = (mx - self.wfc.offsetX) // self.wfc.tileSizeX
        y = (my - self.wfc.offsetY) // self.wfc.tileSizeY

        if 0 <= x < self.wfc.Width and 0 <= y < self.wfc.Height:
            return self.wfc.grid[x][y]

        return None

    def StartSearch(self):
        self.dist = {}
        self.prev = {}
        self.fscore = {}
        self.path = []
        self.processing = True

        self.start_time = time.time()

        for x in range(self.wfc.Width):
            for y in range(self.wfc.Height):
                t = self.wfc.grid[x][y]
                self.dist[t] = math.inf
                self.prev[t] = None
                self.fscore[t] = math.inf
                t.visited_astar = False

        self.dist[self.start] = 0
        self.fscore[self.start] = self.Heuristic(self.start)

    def Heuristic(self, t):
        return abs(t.x - self.end.x) + abs(t.y - self.end.y)

    def Step(self):
        if not self.processing:
            return

        current = None
        best = math.inf

        # pick lowest f-score (g + h)
        for x in range(self.wfc.Width):
            for y in range(self.wfc.Height):
                t = self.wfc.grid[x][y]

                if getattr(t, "visited_astar", False):
                    continue

                if self.fscore[t] < best:
                    best = self.fscore[t]
                    current = t

        if current is None:
            self.processing = False
            return

        current.visited_astar = True

        if current == self.end:
            self.Reconstruct()
            self.processing = False
            self.end_time = time.time()
            self.elapsed_ms = self.end_time - self.start_time
            return

        for n in self.GetNeighbors(current):
            if n.difficulty == 2:
                continue

            cost = 1 if n.difficulty == 0 else 5

            tentative_g = self.dist[current] + cost

            if tentative_g < self.dist[n]:
                self.dist[n] = tentative_g
                self.prev[n] = current

                self.fscore[n] = tentative_g + self.Heuristic(n)

    def GetNeighbors(self, t):
        x, y = t.x, t.y
        n = []

        if x > 0:
            n.append(self.wfc.grid[x - 1][y])
        if x < self.wfc.Width - 1:
            n.append(self.wfc.grid[x + 1][y])
        if y > 0:
            n.append(self.wfc.grid[x][y - 1])
        if y < self.wfc.Height - 1:
            n.append(self.wfc.grid[x][y + 1])

        return n

    def Reconstruct(self):
        self.path = []
        cur = self.end

        while cur is not None:
            self.path.append(cur)
            cur = self.prev[cur]

        self.path.reverse()

    def Draw(self, screen):
        tsx = self.wfc.tileSizeX
        tsy = self.wfc.tileSizeY
        ox = self.wfc.offsetX
        oy = self.wfc.offsetY

        # visited (purple)
        for x in range(self.wfc.Width):
            for y in range(self.wfc.Height):
                t = self.wfc.grid[x][y]

                if getattr(t, "visited_astar", False):
                    pygame.draw.rect(
                        screen,
                        (180, 80, 255),
                        (ox + t.x * tsx, oy + t.y * tsy, tsx, tsy),
                        2
                    )

        # path (green)
        for t in self.path:
            pygame.draw.rect(
                screen,
                (0, 255, 0),
                (ox + t.x * tsx, oy + t.y * tsy, tsx, tsy),
                4
            )

        # start/end
        if self.start:
            pygame.draw.rect(
                screen,
                (255, 255, 0),
                (ox + self.start.x * tsx, oy + self.start.y * tsy, tsx, tsy),
                3
            )

        if self.end:
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                (ox + self.end.x * tsx, oy + self.end.y * tsy, tsx, tsy),
                3
            )

        if len(self.path):
            font = pygame.font.SysFont("Arial", 18)
            text = font.render("A* Time in seconds:"+str(self.elapsed_ms),True,(255, 255, 255))
            screen.blit(text, (10,580))