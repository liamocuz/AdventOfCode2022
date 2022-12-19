"""
For part 2
"""
def valid_path(grid, origin) -> bool:
    sand_y, sand_x = 0, origin
    left_bound = 0
    right_bound = len(grid[0])
    max_depth = len(grid)

    obstacles = ['#', 'O']

    if grid[sand_y][sand_x] in obstacles:
        return False

    falling = True
    while falling:
        if sand_y + 1 >= max_depth:
            return False
        elif sand_x - 1 < left_bound or sand_x + 1 > right_bound:
            return False
        
        if grid[sand_y + 1][sand_x] not in obstacles:
            sand_y += 1
        elif grid[sand_y + 1][sand_x - 1] not in obstacles:
            sand_y += 1
            sand_x -= 1
        elif grid[sand_y + 1][sand_x + 1] not in obstacles:
            sand_y += 1
            sand_x += 1
        else:
            grid[sand_y][sand_x] = 'O'
            falling = False

    return True

def sim_sand(grid, origin):
    count = 0
    while valid_path(grid, origin):
        count += 1

    return count

def fill_rocks(grid, start, end):
    start_y, start_x = start
    end_y, end_x = end

    diff_x = end_x - start_x
    diff_y = end_y - start_y

    if diff_x != 0:
        while start_x != end_x:
            grid[start_x][start_y] = '#'
            start_x += (diff_x // abs(diff_x))
        grid[start_x][start_y] = '#'
    elif diff_y != 0:
        while start_y != end_y:
            grid[start_x][start_y] = '#'
            start_y += (diff_y // abs(diff_y))
        grid[start_x][start_y] = '#'


def draw_rocks(grid, lines):
    for line in lines:
        for idx in range(len(line) - 1):
            start = line[idx]
            end = line[idx + 1]
            fill_rocks(grid, start, end)

    grid.append(['.' for _ in range(len(grid[0]))])
    grid.append(['#' for _ in range(len(grid[0]))])


if __name__ == "__main__":
    file = open("./input.txt", "r")
    lines = file.read().splitlines() 
    file.close()


    # Removes arrows, turn coords into tuples of ints
    lines = [line.strip().split(' -> ') for line in lines]
    lines = [[[(int(coord)) for coord in coords.split(',')] for coords in line] for line in lines]

    depth_bound = 0
    for line in lines:
        for coord in line:
            depth_bound = max(depth_bound, coord[1])


    grid = [['.' for _ in range(1001)] for _ in range(depth_bound + 1)]
    origin = 500

    draw_rocks(grid, lines)

    sands = sim_sand(grid, origin)
    print(sands)