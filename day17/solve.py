rock_shapes = [
    [[1, 1, 1, 1]],
    [[0, 1, 0],[1, 1, 1],[0, 1, 0]],
    [[1, 1, 1],[0, 0, 1],[0, 0, 1]],
    [[1],[1],[1],[1]],
    [[1, 1],[1, 1]]
]

rock_points = [
    [(0,0), (0,1), (0,2), (0,3)],
    [(0,1), (1,0), (1,1), (1,2), (2,1)],
    [(0,0), (0,1), (0,2), (1,2), (2,2)],
    [(0,0), (1,0), (2,0), (3,0)],
    [(0,0), (0,1), (1,0), (1,1)]
]

WIDTH = 7
ITERATIONS = 2022 # Part 1
NUM_ROCKS = 1_000_000_000_000 # Part 2

class Rock:
    def __init__(self, shape: list[list[int]], points: list, lrow: int, lcol: int) -> None:
        self.shape: list[list[int]] = shape
        self.points: list = points
        self.points_set = set(self.points)
        self.width: int = len(self.shape[0])
        self.height: int = len(self.shape)
        self.ll = (lrow, lcol) # row, col


    def appear(self) -> list[list[int]]:
        """
        Creates the 7x(self.height + 3) spawn zone of the new rock
        This is then added to the stack
        """
        area = [[0] * WIDTH for _ in range(3)]
        for row in self.shape:
            new_row = [0] * 2 + row + [0] * (WIDTH - len(row) - 2)
            area.append(new_row)

        points = self.points
        self.points = []
        for point in points:
            self.points.append((point[0] + self.ll[0], point[1] + self.ll[1]))
        
        self.points_set = set(self.points)
        return area

def simulate_rocks(chamber_start: list, moves: list[str], iterations: int, move_start_idx: int, rock_start_idx: int):
    """
    Simulates how the rocks fall in the chamber
    """

    rocks = []
    chamber = chamber_start
    current_move = move_start_idx

    track = {}

    i = rock_start_idx
    for _ in range(iterations):
        rock_shape = rock_shapes[i % len(rock_shapes)]
        rock_point = rock_points[i % len(rock_points)]

        rock = Rock(rock_shape, rock_point, len(chamber) + 3, 2)
        new_area = rock.appear()
        for row in new_area:
            chamber.append(row)

        moves_made = move_rock(chamber, rock, moves, current_move)
        rocks.append(rock)

        # this could be better
        to_pop = 0
        for row in reversed(chamber):
            if 1 not in row:
                to_pop += 1
            else:
                break
        for _ in range(to_pop):
            chamber.pop()

        old_move = current_move
        current_move = (current_move + moves_made) % len(moves)
        # This track and key keeps track of finding cycles by the current jetstream index and current rock
        key = (old_move, current_move, i % len(rock_shapes)) 
        if key not in track:
            track[key] = []
        track[key].append((len(chamber), len(rocks)))

        i += 1


    def is_spaced_evenly(arr) -> bool:
        if len(arr) <= 1:
            return False

        distance = arr[1][0] - arr[0][0]
        blocks = arr[1][1] - arr[0][1]
        i = 2
        while i < len(arr) and arr[i][0] - arr[i - 1][0] == distance:
            i += 1

        if i == len(arr):
            return True
        return False


    # Used to find cycles
    last_arr = None
    last_key = None
    for key in track:
        if is_spaced_evenly(track[key]):
            last_arr = track[key]
            last_key = key

    return chamber, last_key, last_arr

def move_rock(chamber, rock: Rock, moves: list[str], current_move: int) -> int:
    """
    Returns how many tiles the rock fell
    """
    moves_made = 0
    can_move = True

    # for row in reversed(chamber):
    #     print(row)

    while can_move:
        move = moves[current_move]
        current_move = (current_move + 1) % len(moves)

        if move == '<':
            move_left(chamber, rock)
        elif move == '>':
            move_right(chamber, rock)

        # print(move)
        # for row in reversed(chamber):
        #     print(row)
        # print()

        can_move = move_down(chamber, rock)
        moves_made += 1

        # print('down')
        # for row in reversed(chamber):
        #     print(row)
        # print()
    # print(moves_made)
    return moves_made

def move_left(chamber, rock) -> bool:
    for point in rock.points:
        if point[1] - 1 < 0:
            return False
        elif chamber[point[0]][point[1] - 1] == 1 and (point[0], point[1] - 1) not in rock.points_set:
            return False
    
    for idx, _ in enumerate(rock.points):
        point = rock.points[idx]
        chamber[point[0]][point[1]] = 0
        rock.points[idx] = (point[0], point[1] - 1)

    for point in rock.points:
        chamber[point[0]][point[1]] = 1

    rock.points_set = set(rock.points)

    return True

def move_right(chamber, rock) -> bool:
    for point in rock.points:
        if point[1] + 1 >= WIDTH:
            return False
        elif chamber[point[0]][point[1] + 1] == 1 and (point[0], point[1] + 1) not in rock.points_set:
            return False
    
    for idx, _ in enumerate(rock.points):
        point = rock.points[idx]
        chamber[point[0]][point[1]] = 0
        rock.points[idx] = (point[0], point[1] + 1)

    for point in rock.points:
        chamber[point[0]][point[1]] = 1

    rock.points_set = set(rock.points)

    return True

def move_down(chamber, rock) -> bool:
    for point in rock.points:
        if point[0] - 1 < 0:
            return False
        elif chamber[point[0] - 1][point[1]] == 1 and (point[0] - 1, point[1]) not in rock.points_set:
            return False

    for idx, _ in enumerate(rock.points):
        point = rock.points[idx]
        chamber[point[0]][point[1]] = 0
        rock.points[idx] = (point[0] - 1, point[1])
    
    for point in rock.points:
        chamber[point[0]][point[1]] = 1

    rock.points_set = set(rock.points)

    return True


if __name__ == "__main__":
    """
    width is 7 units
    
    each rock start so left side is 2 units from left wall
    bottom edge is 3 units above highest rock in room or floow if no rock

    after a rock appears, it alternates between being pushed by gas one unit and then falling one unit

    if any movement would cause the rock to move into the walls, floor, or a stopped rock,
    the rock instead does not move.
    if a downward movement would make the rock stop moving into the floor or another rock,
    the rock stops moving and another rock begins falling


    need to figure out how to represent the rock in space per rock type
    think I can achieve this by just keep track of previous and current rock

    can just keep track of how each row in the stack looks by using a stack
    rocks will be a matrix but can have differing height and width

    [0][0] is always the bottom left of the shape
    ex  #### is [[1, 1, 1, 1]]

    ex  .#. is [[0, 1, 0],[1, 1, 1],[0, 1, 0]]
        ###
        .#.

    ex  #   is [[1],[1],[1],[1]]
        #
        #
        #

    ex  ..# is [[1, 1, 1],[0, 0, 1],[0, 0, 1]]
        ..#
        ###

    ex  ##  is [[1, 1],[1, 1]]
        ##
    """

    file = open("./input.txt", "r")
    moves = file.read()
    file.close()

    # part 1
    chamber, key, arr = simulate_rocks([], moves, ITERATIONS, 0, 0)
    next_move = key[1]
    next_rock = key[2] + 1
    print(len(chamber))

    # part 2
    ITERATIONS = len(moves) * len(rock_shapes)
    print(f"Rocks to simulate: {ITERATIONS}")
    
    # Finds cycles in the initial simulated rocks
    chamber, key, arr = simulate_rocks([], moves, ITERATIONS, 0, 0)
    height_already_simulated = arr[-1][0]
    rocks_already_simulated = arr[-1][1]
    print(f"Height already simulated: {height_already_simulated}")
    print(f"Rocks already simulated: {rocks_already_simulated}")

    height_per_cycle = arr[1][0] - arr[0][0]
    rocks_per_cycle = arr[1][1] - arr[0][1]
    print(f"Height per cycle: {height_per_cycle}")
    print(f"Rocks per cycle: {rocks_per_cycle}")

    # Gets how many more rocks needs to be simulated
    cyclic_iterations_left = (NUM_ROCKS - rocks_already_simulated) // rocks_per_cycle
    remainder = (NUM_ROCKS - rocks_already_simulated) % rocks_per_cycle
    print(f"Cycles left: {cyclic_iterations_left}")
    print(f"Remainder: {remainder}")

    # If there is a remainder, we need to simulate that last bit of rocks
    remainder_height = 0
    if remainder > 0:
        old_chamber = chamber[0:height_already_simulated]
        old_height = len(old_chamber)
        print(f"Old Chamber Height: {old_height}")
        new_chamber, _, _ = simulate_rocks(old_chamber, moves, remainder, next_move, next_rock) 
        new_height = len(new_chamber)
        print(f"New Chamber Height: {new_height}")
        remainder_height = new_height - old_height
        print(f"Remainder height: {remainder_height}")
    
    # Calculate the total height of the chamber for all 1 trillion rocks
    total_height = (cyclic_iterations_left * height_per_cycle) + height_already_simulated + remainder_height

    print(f"Total Height: {total_height}")
