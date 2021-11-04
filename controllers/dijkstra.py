from typing import Dict, Tuple, List

from models.grid_position import GridPosition


def calculate_path_from_position(
    matrix: Dict[GridPosition, Dict[GridPosition, int]],
    position: GridPosition,
    destination: GridPosition
) -> bool:
    visited = {position: 0, }
    current = position
    unvisited = {grid: float('inf') for grid in matrix if grid != position}

    while unvisited:
        for grid in matrix[current]:
            if grid == destination:
                return True
            if grid not in visited:
                if unvisited[grid] == float('inf'):
                    unvisited[grid] = visited[current] + matrix[current][grid]
                else:
                    unvisited[grid] += matrix[current][grid]

        current = min(unvisited, key=unvisited.get)
        if unvisited[current] == float('inf'):
            return False
        visited[current] = unvisited[current]
        unvisited.pop(current)

    return False


def calculate_shortest_path_from_position(
    matrix: Dict[GridPosition, Dict[GridPosition, int]],
    position: GridPosition
) -> Tuple[Dict[GridPosition, GridPosition], Dict[GridPosition, int]]:
    visited = {position: 0, }
    current = position
    unvisited = {grid: float('inf') for grid in matrix if grid != position}
    previous_grids = {}

    while unvisited:
        for grid in matrix[current]:
            if grid not in visited:
                if unvisited[grid] == float('inf'):
                    unvisited[grid] = visited[current] + matrix[current][grid]
                    previous_grids[grid] = current
                elif unvisited[grid] >= unvisited[grid] + matrix[current][grid]:
                    unvisited[grid] += matrix[current][grid]
                    previous_grids[grid] = current

        current = min(unvisited, key=unvisited.get)
        visited[current] = unvisited[current]
        unvisited.pop(current)

    return previous_grids, visited


