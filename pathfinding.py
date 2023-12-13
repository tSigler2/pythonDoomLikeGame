import pygame as pg
from collections import deque

class PathFinding:
    def __init__(self, game):
        self.game = game
        self.map = game.map.mm
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [-1, 1], [1, 1]
        self.graph = {}
        self.get_graph()

    def get_graph(self):
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)

    def get_path(self, start, end):
        self.visited = self.bfs(start, end, self.graph)
        path = [end]
        step = self.visited.get(end, start)

        while step and step != start:
            path.append(step)
            step = self.visited[step]
        return path[-1]

    def bfs(self, start, end, graph):
        q = deque([start])
        visited = {start: None}

        while q:
            cur_node = q.popleft()
            if cur_node == end:
                break
            next = graph[cur_node]

            for n in next:
                if n not in visited and n not in self.game.object_handler.npc_pos:
                    q.append(n)
                    visited[n] = cur_node
        return visited
    
    def get_next_nodes(self, x, y):
        return [(x + dx, y + dy) for dx, dy in self.ways if (x + dx, y + dy) not in self.game.map.world_map]
