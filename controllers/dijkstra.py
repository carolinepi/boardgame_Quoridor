from typing import Dict

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
                    unvisited[grid] = \
                        visited[current] + matrix[current][grid]
                else:
                    unvisited[grid] += matrix[current][grid]

        current = min(unvisited, key=unvisited.get)
        if unvisited[current] == float('inf'):
            return False
        visited[current] = unvisited[current]
        unvisited.pop(current)

    return False
