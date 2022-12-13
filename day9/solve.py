class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y

# x-y coords
UP = Point(0, 1)
DOWN = Point(0, -1)
LEFT = Point(-1, 0)
RIGHT = Point(1, 0)

cmd = {
    'U': UP,
    'D': DOWN,
    'L': LEFT,
    'R': RIGHT
}

def find_move(leading: Point, following: Point) -> Point:
    """
    Leading should already have been moved before this function
    
    Find the direction that following will have to move
    """
    x_diff = leading.x - following.x
    y_diff = leading.y - following.y

    new_mod = Point(0, 0)
    if abs(x_diff) == 2:
        new_mod.x += x_diff // 2
        if abs(y_diff) == 1:
            new_mod.y += y_diff

    if abs(y_diff) == 2:
        new_mod.y += y_diff // 2
        if abs(x_diff) == 1:
            new_mod.x += x_diff

    return new_mod

def follow(commands) -> int:
    track = set()

    head = Point(0, 0)
    tail = Point(0, 0)
    track.add((tail.x, tail.y))

    for command in commands:
        direction, distance = command.split(' ')
        distance = int(distance)

        mod = cmd[direction]
        
        for _ in range(distance):
            head += mod
            tail += find_move(head, tail)
            
            track.add((tail.x, tail.y))

    return len(track)


def simulate_knots(commands) -> int:
    """
    Find how many positions the tail of the rope hits
    """
    ROPE_LENGTH = 10

    knots = [Point(0, 0) for _ in range(ROPE_LENGTH)]
    track = set()

    for command in commands:
        direction, distance = command.split(' ')
        distance = int(distance)
        mod = cmd[direction]

        for _ in range(distance):
            knots[0] += mod
            for idx in range(0, len(knots) - 1):
                knots[idx+1] += find_move(knots[idx], knots[idx + 1])

            tail = knots[ROPE_LENGTH - 1]
            track.add((tail.x, tail.y))

    return len(track)


if __name__ == "__main__":
    
    file = open("./input.txt", "r")
    commands = file.read().splitlines()
    file.close()

    # Part 1
    points = follow(commands)
    print(points)

    # Part 2
    points2 = simulate_knots(commands)
    print(points2)