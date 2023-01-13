from time import sleep

class Cube:
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.surfaces = 6

    def coords(self) -> tuple:
        return (self.x, self.y, self.z)

    def __repr__(self) -> str:
        return f"x: {self.x}, y: {self.y}, z: {self.z}"

    @staticmethod
    def get_adjacent(cube: "Cube") -> list[tuple]:
        return [
            (cube.x - 1, cube.y, cube.z),
            (cube.x + 1, cube.y, cube.z),
            (cube.x, cube.y - 1, cube.z),
            (cube.x, cube.y + 1, cube.z),
            (cube.x, cube.y, cube.z - 1),
            (cube.x, cube.y, cube.z + 1),
        ]


class Glob:
    def __init__(self) -> None:
        # Keeps track of all Cubes
        self.cube_list: list[Cube] = []
        # Map a tuple of coords to a Cube class
        self.cube_dict: dict[tuple, Cube] = {}

        # Keep track of the airpocket coordinates
        self.airpockets = set()

        # Keeps track of outside coords
        self.max_x = float("-inf")
        self.max_y = float("-inf")
        self.max_z = float("-inf")
        self.min_x = float("inf")
        self.min_y = float("inf")
        self.min_z = float("inf")

    def add_cube(self, cube: Cube):
        self.cube_list.append(cube)
        self.cube_dict[(cube.x, cube.y, cube.z)] = cube

        if cube.x > self.max_x:
            self.max_x = cube.x
        if cube.y > self.max_y:
            self.max_y = cube.y
        if cube.z > self.max_z:
            self.max_z = cube.z

        if cube.x < self.min_x:
            self.min_x = cube.x
        if cube.y < self.min_y:
            self.min_y = cube.y
        if cube.z < self.min_z:
            self.min_z = cube.z

    def update_surfaces(self) -> None:
        for cube in self.cube_list:
            neighbors = Cube.get_adjacent(cube)
            for neighbor in neighbors:
                if neighbor in self.cube_dict and neighbor not in self.airpockets:
                    cube.surfaces -= 1

        return

    def get_surface_area(self) -> int:
        sa = 0
        for cube in self.cube_list:
            sa += cube.surfaces

        return sa

    def generate_all_coordinates(self) -> set:
        coords = set()

        for x in range(self.min_x, self.max_x + 1):
            for y in range(self.min_y, self.max_y + 1):
                for z in range(self.min_z, self.max_z + 1):
                    coords.add((x, y, z))

        return coords

    def get_neighbors(self, coord: tuple) -> list:
        x, y, z = coord
        neighbors = []
        possible_neighbors = [
            (x - 1, y, z),
            (x + 1, y, z),
            (x, y - 1, z),
            (x, y + 1, z),
            (x, y, z - 1),
            (x, y, z + 1),
        ]

        for possible in possible_neighbors:
            if possible not in self.cube_dict:
                neighbors.append(possible)

        return neighbors

    def out_of_bounds(self, coord: tuple) -> bool:
        x, y, z = coord
        answer = (
            self.min_x <= x <= self.max_x
            and self.min_y <= y <= self.max_y
            and self.min_z <= z <= self.max_z
        )
        return not answer

    def find_airpocket(self) -> set:
        """
        Ok, I have all coordinates of the cube that are not of the glob
        I need to loop over each coordinate and do a BFS at that coordinate
        Throughout the BFS, I need to check if that BFS run is outside
        If it is outside, don't add to airpocket
        If not, add to airpocket
        """

        airpockets = set()
        all_set = self.generate_all_coordinates()
        cube_set = set(self.cube_dict.keys())
        difference_set = all_set.difference(cube_set)

        difference_list = sorted(list(difference_set))
        visited = set()
        is_outside = False

        # iterate through difference list
        for coord in difference_list:
            # skip if already seen
            if coord in visited:
                continue

            current_bfs = set()
            queue = [coord]
            while queue:
                current_coord = queue.pop(0)
                if current_coord in visited:
                    continue
                visited.add(current_coord)
                current_bfs.add(current_coord)

                neighbors = self.get_neighbors(current_coord)
                for neighbor in neighbors:
                    if self.out_of_bounds(neighbor):
                        is_outside = True
                    else:
                        queue.append(neighbor)

            if not is_outside:
                airpockets = airpockets.union(current_bfs)
            current_bfs = set()
            is_outside = False

        self.airpockets = airpockets
        return airpockets

    def update_inside_surface_area(self):
        for coord in self.airpockets:
            neighbors = Cube.get_adjacent(Cube(*coord))
            for neighbor in neighbors:
                if neighbor in self.cube_dict:
                    self.cube_dict[neighbor].surfaces -= 1


if __name__ == "__main__":
    """
    Try and do a cumulative addition to the first cube
    Use the Glob class to continually add Cubes together

    Need to figure out how to tell if two cubes are adjacent
    I think that is done if two of their coords are the same and the other is 1 off

    Part 2
    Need to figure out which cubes are inside
    Already have all cube coords
    Need to find some sort of intersect I guess
    Need to find the outside of the glob

    Can do a 3D BFS inside of a box
    Loop across the box and keep track of coordinates already visited
    If the coordinate is not part of the glob, get all face neighbors and continue
    If you reach a point outside of the box, that entire walk is moot
    If all are explored, then those are all of the inside air pockets
    """

    file = open("./input.txt", "r")
    lines = file.read().splitlines()
    coords = [[int(val) for val in line.split(",")] for line in lines]
    file.close()

    glob = Glob()
    for coord in coords:
        x, y, z = coord
        cube = Cube(x, y, z)
        glob.add_cube(cube)

    glob.update_surfaces()
    sa = glob.get_surface_area()

    # Part 1
    # 3494 right!
    print(sa)

    # Part 2
    glob.find_airpocket()
    glob.update_inside_surface_area()
    print(glob.get_surface_area())
    # 2062 right!
