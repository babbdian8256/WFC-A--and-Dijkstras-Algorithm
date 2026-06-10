import pygame
import math
import time


class DijkstraPathfinder:
    def __init__(self, wfc):
        self.wfc = wfc

        self.start = None
        self.end = None

        self.startTime =0
        self.endTime =0
        self.elaspedTime=0

        self.dist = {}
        self.prev = {}

        self.path = []
        self.processing = False

    # CLICK HANDLER
    def HandleClick(self, mouse_pos, button):
        tile = self.GetTileFromScreen(mouse_pos)

        if tile is None:
            return

        # left click = start
        if button == 1:
            if tile.difficulty != 2:
                self.start = tile

        # right click = end
        if button == 3:
            if tile.difficulty != 2:
                self.end = tile

        if self.start and self.end:
            self.StartSearch()

    def GetTileFromScreen(self, pos):
        mx, my = pos

        local_x = mx - self.wfc.offsetX
        local_y = my - self.wfc.offsetY

        if local_x < 0 or local_y < 0:
            return None

        grid_x = int(local_x // self.wfc.tileSizeX)
        grid_y = int(local_y // self.wfc.tileSizeY)

        if 0 <= grid_x < self.wfc.Width and 0 <= grid_y < self.wfc.Height:
            return self.wfc.grid[grid_x][grid_y]

        return None

    def StartSearch(self):
        self.dist = {}
        self.prev = {}
        self.path = []
        self.processing = True

        self.startTime=time.time()
        self.endTime=0
        self.elaspedTime=0

        for x in range(self.wfc.Width):
            for y in range(self.wfc.Height):
                t = self.wfc.grid[x][y]
                self.dist[t] = math.inf
                self.prev[t] = None
                t.visited = False

        self.dist[self.start] = 0

    # SIMPLE DIJKSTRA STEP
    def Step(self):
        if not self.processing:
            return

        current = None
        best = math.inf

        for x in range(self.wfc.Width):
            for y in range(self.wfc.Height):
                t = self.wfc.grid[x][y]

                if getattr(t, "visited", False):
                    continue

                if self.dist[t] < best:
                    best = self.dist[t]
                    current = t

        if current is None:
            self.processing = False
            return

        current.visited = True

        if current == self.end:
            self.Reconstruct()
            self.processing = False
            self.endTime=time.time()
            self.elaspedTime=self.endTime-self.startTime

            return

        for n in self.GetNeighbors(current):
            if n.difficulty == 2:
                continue

            cost = 1 if n.difficulty == 0 else 5

            new_cost = self.dist[current] + cost

            if new_cost < self.dist[n]:
                self.dist[n] = new_cost
                self.prev[n] = current

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

        # visited nodes
        for x in range(self.wfc.Width):
            for y in range(self.wfc.Height):
                t = self.wfc.grid[x][y]

                if getattr(t, "visited", False):
                    pygame.draw.rect(
                        screen,
                        (80, 80, 255),
                        (ox + t.x * tsx, oy + t.y * tsy, tsx, tsy),
                        2
                    )

        for t in self.path:
            pygame.draw.rect(
                screen,
                (0, 255, 0),
                (ox + t.x * tsx, oy + t.y * tsy, tsx, tsy),
                4
            )

        if len(self.path)>0:
            font = pygame.font.SysFont("Arial", 20)
            text = font.render("Dijkstras Time in seconds :"+str(self.elaspedTime), True, (255, 255, 255))
            screen.blit(text,(10,555))

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