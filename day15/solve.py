class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

def manhattan_distance(source: Point, dest: Point):
    return float(abs(source.x - dest.x) + abs(source.y - dest.y))

def get_sensors(lines) -> list:
    # sensors should a tuple where [0] is sensor, [1] is closest becon
    sensors = []

    for line in lines:
        splits = line.split(' ')

        sensor_x = int(splits[2][2:len(splits[2]) - 1])
        sensor_y = int(splits[3][2:len(splits[3]) - 1])

        beacon_x = int(splits[8][2:len(splits[8]) - 1])
        beacon_y = int(splits[9][2:len(splits[9])])

        sensor = Point(sensor_x, sensor_y)
        beacon = Point(beacon_x, beacon_y)
        sensors.append((sensor, beacon))
    
    return sensors

def find_no_beacons(sensors, y: int) -> list:

    locs = set()
    for sensor, beacon in sensors:
        x1 = sensor.x
        x2 = sensor.x

        curr1 = Point(x1, y)
        curr2 = Point(x2, y)

        curr1_manhattan = manhattan_distance(sensor, curr1)
        curr2_manhattan = manhattan_distance(sensor, curr2)
        sensor_manhattan = manhattan_distance(sensor, beacon)

        no_beacon = True
        while no_beacon:
            no_beacon = False
            if curr1_manhattan <= sensor_manhattan:
                if curr1 != beacon:
                    locs.add((curr1.x, curr1.y))
                x1 += 1
                curr1 = Point(x1, y)
                curr1_manhattan = manhattan_distance(sensor, curr1)
                no_beacon = True


            if curr2_manhattan <= sensor_manhattan:
                if curr2 != beacon:
                    locs.add((curr2.x, curr2.y))
                x2 -= 1
                curr2 = Point(x2, y)
                curr2_manhattan = manhattan_distance(sensor, curr2)
                no_beacon = True

    return list(locs)


def find_beacon(sensors, cutoff) -> Point:
    """
    Get the coords for each sensor just outside of their border
    Check each one of those coords against every other sensor
    If not in any sensor, is the proper coord
    """
    for sensor1, beacon1 in sensors:
        border = get_border(sensor1, beacon1)

        for point in border:
            if point.x > cutoff or point.y > cutoff:
                continue
            elif point.x < 0 or point.y < 0:
                continue

            valid = True
            for sensor2, beacon2 in sensors:
                if  sensor1 == sensor2:
                    continue
                point_manhattan = manhattan_distance(sensor2, point)
                sensor2_manhattan = manhattan_distance(sensor2, beacon2)

                if point_manhattan <= sensor2_manhattan:
                    valid = False

            if valid:
                return point

    return None


def get_border(sensor, beacon) -> list[Point]:
    """
    Gets all points just outside of radius of sensor to beacon
    """
    x = sensor.x

    curr = Point(x, sensor.y)
    curr_manhattan = manhattan_distance(sensor, curr)
    sensor_manhattan = manhattan_distance(sensor, beacon)

    while curr_manhattan < sensor_manhattan:
        x += 1
        curr = Point(x, sensor.y)
        curr_manhattan = manhattan_distance(sensor, curr)

    radius = x - sensor.x + 1

    border = []
    x, y = sensor.x, sensor.y + radius
    curr = Point(x, y)

    # get border clockwise
    while curr != Point(sensor.x + radius, sensor.y):
        border.append(curr)
        x += 1
        y -= 1
        curr = Point(x, y)
    while curr != Point(sensor.x, sensor.y - radius):
        border.append(curr)
        x -= 1
        y -= 1
        curr = Point(x, y)
    while curr != Point(sensor.x - radius, sensor.y):
        border.append(curr)
        x -= 1
        y += 1
        curr = Point(x, y)
    while curr != Point(sensor.x, sensor.y + radius):
        border.append(curr)
        x += 1
        y += 1
        curr = Point(x, y)

    return border

if __name__ == "__main__":
    file = open("./input.txt", "r")
    lines = file.read().splitlines()
    file.close()

    sensors = get_sensors(lines)

    Y_CONST = 2_000_000

    # Part 1: takes about 12 sec
    no_beacons = find_no_beacons(sensors, Y_CONST)
    print(len(no_beacons))

    CUTOFF = 4_000_000
    TUNING = 4_000_000
    
    # Part 2: takes about 5 min
    beacon = find_beacon(sensors, CUTOFF)
    print(beacon)

    freq = beacon.x * TUNING + beacon.y
    print(freq)
