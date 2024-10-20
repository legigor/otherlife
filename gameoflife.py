from typing import Dict


class GameState:
    def __init__(self):
        self.__index: Dict[int, Dict[int, int]] = {}
        self.__state = []

    def append(self, i, j):
        if i not in self.__index:
            self.__index[i] = {}
        self.__index[i][j] = 1
        if (i, j) not in self.__state:
            self.__state.append((i, j))

    def get_neighbors(self, i, j):
        neighbors = []
        for ni in range(i - 1, i + 2):
            for nj in range(j - 1, j + 2):
                if ni == i and nj == j:
                    continue
                if ni in self.__index and nj in self.__index[ni]:
                    neighbors.append((ni, nj))
        return neighbors

    def get_empty_neighbors(self, i, j):
        neighbors = []
        for ni in range(i - 1, i + 2):
            for nj in range(j - 1, j + 2):
                if ni == i and nj == j:
                    continue
                if ni not in self.__index or nj not in self.__index[ni]:
                    neighbors.append((ni, nj))
        return neighbors

    def get_state(self):
        return self.__state


class GameOfLife:
    def __init__(self, state):
        self.__state = GameState()
        for i, j in state:
            self.__state.append(i, j)

    def get_state(self):
        return self.__state.get_state()

    def turn(self):
        # pass
        new_state = GameState()
        state = self.__state.get_state()
        for i, j in state:
            neighbors = self.__state.get_neighbors(i, j)
            # Survival
            if len(neighbors) == 2 or len(neighbors) == 3:
                new_state.append(i, j)
            # Death
            if len(neighbors) < 2 or len(neighbors) > 3:
                continue
            # Birth
            empty_neighbors = self.__state.get_empty_neighbors(i, j)
            for ni, nj in empty_neighbors:
                neighbors = self.__state.get_neighbors(ni, nj)
                if len(neighbors) == 3:
                    new_state.append(ni, nj)
        self.__state = new_state
