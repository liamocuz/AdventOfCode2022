def check_tree(grid, rowIdx: int, colIdx: int, initial_height: int, direction: tuple) -> bool:

    row_bound = len(grid)
    col_bound = len(grid[0])

    if rowIdx < 0 or rowIdx >= row_bound or colIdx < 0 or colIdx >= col_bound:
        return True
    
    current_height = grid[rowIdx][colIdx]
    if current_height >= initial_height:
        return False

    row_mod, col_mod = direction
    return check_tree(grid, rowIdx + row_mod, colIdx + col_mod, initial_height, direction)

def find_visible(grid) -> int:
    up = (-1, 0)
    down = (1, 0)
    left = (0, -1)
    right = (0, 1)

    trees = 0

    for rowIdx in range(len(grid)):
        for colIdx in range(len(grid[rowIdx])):
            height = grid[rowIdx][colIdx]
            if check_tree(grid, rowIdx - 1, colIdx, height, up):
                trees += 1
            elif check_tree(grid, rowIdx + 1, colIdx, height, down):
                trees += 1
            elif check_tree(grid, rowIdx, colIdx - 1, height, left):
                trees += 1
            elif check_tree(grid, rowIdx, colIdx + 1, height, right):
                trees += 1

    return trees

def check_distance(grid, rowIdx: int, colIdx: int, initial_height: int, direction: tuple, distance: int) -> int:
    row_bound = len(grid)
    col_bound = len(grid[0])

    if rowIdx < 0 or rowIdx >= row_bound or colIdx < 0 or colIdx >= col_bound:
        return distance - 1
    
    current_height = grid[rowIdx][colIdx]
    if current_height >= initial_height:
        return distance

    row_mod, col_mod = direction
    return check_distance(grid, rowIdx + row_mod, colIdx + col_mod, initial_height, direction, distance + 1)

def find_scenic(grid) -> int:
    up = (-1, 0)
    down = (1, 0)
    left = (0, -1)
    right = (0, 1)

    max_score = 0
    
    for rowIdx in range(len(grid)):
        for colIdx in range(len(grid[rowIdx])):
            height = grid[rowIdx][colIdx]

            up_distance = check_distance(grid, rowIdx - 1, colIdx, height, up, 1)
            down_distance = check_distance(grid, rowIdx + 1, colIdx, height, down, 1)
            left_distance = check_distance(grid, rowIdx, colIdx - 1, height, left, 1)
            right_distance = check_distance(grid, rowIdx, colIdx + 1, height, right, 1)

            current_score = up_distance * down_distance * left_distance * right_distance
            max_score = max(max_score, current_score)

    return max_score


if __name__ == "__main__":
    """
    Need to find how many trees are visible from outside
    
    All trees on outside are already visible
    Tree is only visible is all trees between it and any edge are shorter

    Can be done by for each point, check each direction
    If any of the directions work, can exit early instead of checking all others
    If works, inc counter
    """

    file = open("./input.txt", "r")
    lines = file.read().splitlines()
    file.close()
    
    grid = [[int(char) for char in [*line]] for line in lines] # turn input into a grid of ints

    # Part 1
    visible = find_visible(grid)
    print(visible)

    # Part 2
    scenic = find_scenic(grid)
    print(scenic)

