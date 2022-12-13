
def get_locations(grid):
    """
    Finds the coordinates of the starting and ending position

    Return: ((start.row, start.col), (end.row, end.col))
    """
    start_char = 'S'
    end_char = 'E'

    for rowIdx in range(len(grid)):
        for colIdx in range(len(grid[rowIdx])):
            current_char = grid[rowIdx][colIdx] 
            if current_char == start_char:
                start = (rowIdx, colIdx)
            if current_char == end_char:
                end = (rowIdx, colIdx)

    return (start, end)
    
def get_height(grid, coord) -> int:
    char = grid[coord[0]][coord[1]]
    if char == 'S':
        return ord('a')
    elif char == 'E':
        return ord('z')
    return ord(char)

def get_neighbors(grid, coords):
    neighbors = []
    row, col = coords
    current_height = get_height(grid, coords)
    
    row_max = len(grid)
    col_max = len(grid[0])

    up, down, left, right = (row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)

    if row - 1 >= 0 and (current_height - get_height(grid, up)) >= -1:
       neighbors.append(up) 
    if row + 1 < row_max and (current_height - get_height(grid, down)) >= -1:
        neighbors.append(down) 
    if col - 1 >= 0 and (current_height - get_height(grid, left)) >= -1:
       neighbors.append(left) 
    if col + 1 < col_max and (current_height - get_height(grid, right)) >= -1:
       neighbors.append(right) 

    return neighbors
    

def bfs(grid, start, end):
    queue = [(start, [])]
    track = set()

    while queue:
        current_coords, path = queue.pop(0)
        path.append(current_coords)
        track.add(current_coords)

        print(path)
        if current_coords == end:
            return len(path) - 1

        for neighbor in get_neighbors(grid, current_coords):
            if neighbor not in track:
                queue.append((neighbor, path[:]))


    return -1


if __name__ == "__main__":
    """
    Can be done with a BFS 
    Or something like Dijkstras or A*
    A* would probably be best, but more complicated to implement
    """

    file = open("./input.txt", "r")
    lines = file.read().splitlines()
    file.close()

    grid = [[*line] for line in lines]

    start, end = get_locations(grid)
    print(start, end)

    # Part 1
    min_length = bfs(grid, start, end) # too slow!
    print(min_length)