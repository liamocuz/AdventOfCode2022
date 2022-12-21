import heapq as heap
from collections import defaultdict

ITERATIONS = 30
MAX_DISTANCE = 10_000
START = 'AA'

class Valve:
    def __init__(self, name, rate, connections) -> None:
        self.name = name
        self.flowrate = rate
        # self.is_open = False
        self.connections = connections

    def __repr__(self) -> str:
        return f"{self.flowrate}, {self.connections}"

def build_graph(lines) -> dict:
    graph = {}

    for line in lines:
        splits = line.split(' ')
        name = splits[1]
        rate = int(splits[4][5:len(splits[4]) - 1])
        connections = [split.strip(',') for split in splits[9:]]

        graph[name] = Valve(name, rate, connections)

    return graph

def build_path(path_map: dict, start: str, next: str) -> list:
    current = next
    path = []
    while current != start:
        path.append(current)
        current = path_map[current]

    path.append(current)
    return path[::-1]



def dijkstras(graph: dict, start: str, time_left: int) -> str:
    """
    At each node, do dijkstras and get the best node to go to next
    This can be done by finding the flowrate / length to get to each node

    Once a node is turned on, then it's flow rate can be set to 0
    
    Need to make sure the path is weary of how many iterations are left 
    If there is a best path but not enough iterations left to get there,
    then find a shorter path
    """
    visited = set()
    queue = []

    # will keep track of the path back from any node to the start
    path_map = {}

    # distances will keep track of the min distance to each node
    distances: dict[str, int] = defaultdict(lambda: MAX_DISTANCE)
    distances[start] = 0

    # priorities will be the highest priority node
    priorities: dict[str, float] = {}
    priorities[start] = 0.0
    highest_priority: str = start

    # the queue will be used to keep track of next smallest distance
    queue = []

    # add the start to the queue
    heap.heappush(queue, (0, start))

    # get the best distances to all other nodes
    while queue:
        _, node = heap.heappop(queue)
        visited.add(node)

        for conn in graph[node].connections:
            if conn in visited:
                continue

            new_distance = distances[node] + 1
            if new_distance < distances[conn]:
                path_map[conn] = node
                distances[conn] = new_distance + 1

                priorities[conn] = float(graph[conn].flowrate * (time_left - distances[conn]))
                if priorities[conn] > priorities[highest_priority]:
                    highest_priority = conn
                heap.heappush(queue, (new_distance, conn))

    # print(f"distances from {start}", dict(distances))
    # print(f"{priorities}")
    # print(time_left)
    pl = [(key, priorities[key]) for key in priorities]
    pl.sort(key=lambda x: x[1])
    pl.reverse()
    # print(dict(distances))
    # print(pl)
    # print(f"highest priority: {highest_priority}")
    # print(f"path map: {path_map}")
    path = build_path(path_map, start, highest_priority)
    # print(f"path: {path}")
    print(start, path_map)
    # print()

    return path


def simulate_valves(graph: dict[Valve], start: str, iterations: int) -> int:
    total_flow = 0
    current_flow = 0

    iters = iterations
    current_node = start

    while iters > 0:
        # print(f"Iterations left: {iters}")
        path = dijkstras(graph, current_node, iters)
        current_node = path[-1]
        travel_dist = len(path)

        total_flow += current_flow * travel_dist
        current_flow += graph[current_node].flowrate

        graph[current_node].flowrate = 0.0
        if iters - travel_dist < 0:
            print("ERROR")
        # print(iters, travel_dist)
        iters -= travel_dist
        # print(f"current flow: {current_flow}")
        # print(f"total flow: {total_flow}")

    return total_flow


if __name__ == "__main__":
    """
    Need to construct a graph using dicts
    Conduct a dijkstras algorithm where the next move will be made depending on
    the flow rates of the connections rather than a distance or something traditional

    At each step, do dijkstras to all other nodes finding the highest path / rate score
    """

    file = open("./test.txt", "r")
    lines = file.read().splitlines()
    file.close()

    graph = build_graph(lines)
    # print(graph)
    pos_flows = [key for key in graph if graph[key].flowrate > 0]
    print(pos_flows)
    
    # 2591 too high
    # 2426 too high
    # 2261 too low
    total_flow = int(simulate_valves(graph, START, ITERATIONS))
    print(total_flow)