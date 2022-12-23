import heapq as heap
from collections import defaultdict
import itertools

MAX_DISTANCE = 10_000
START = 'AA'

class Valve:
    def __init__(self, name, rate, connections) -> None:
        self.name = name
        self.flowrate = rate
        self.connections = connections

    def __repr__(self) -> str:
        return f"{self.flowrate}, {self.connections}"

def build_graph(lines) -> dict:
    """
    Create the graph from the input
    """
    graph = {}

    for line in lines:
        splits = line.split(' ')
        name = splits[1]
        rate = int(splits[4][5:len(splits[4]) - 1])
        connections = [split.strip(',') for split in splits[9:]]

        graph[name] = Valve(name, rate, connections)

    return graph


def dijkstras(graph: dict, start: str, positives: set)-> str:
    """
    Calculates the shortest path from start node to all other nodes
    Reuturns a dict that maps path from start to all other positive flowrate valves
    """
    visited = set()
    queue = []

    # distances will keep track of the min distance to each node
    distances: dict[str, int] = defaultdict(lambda: MAX_DISTANCE)
    distances[start] = 0

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
                distances[conn] = new_distance

                heap.heappush(queue, (new_distance, conn))

    # Return only positive flowrate valves and not self
    return {key: distances[key] for key in distances if graph[key].flowrate > 0.0 and key in positives and key != start}


def simulate_valves(graph: dict[Valve], distances: dict, node: str, visited: set, time_left: int, total_flow: int) -> int:
    """
    Does a DFS on all nodes in distances and keeps track of the time and flow computed thus far
    If the time left is going to be <= 0, skip any further computations from that path
    """

    max_flow = 0
    for key in distances[node]:
        if key in visited:
            continue

        time = time_left - (distances[node][key] + 1)
        if time <= 0:
            continue

        flow = total_flow + graph[key].flowrate * time 

        visited.add(key)
        flow = simulate_valves(graph, distances, key, visited, time, flow)
        max_flow = max(max_flow, flow)
        visited.remove(key)

    return max(max_flow, total_flow)


if __name__ == "__main__":
    """
    So for part 2, need to run through all combinations of splitting the valves between me and the elephant
    and running the same algorithm
    """

    file = open("./input.txt", "r")
    lines = file.read().splitlines()
    file.close()

    # build the graph from the input
    graph = build_graph(lines)

    # build a new graph of only the positive flowrate valves and distances to all other positive flowrate valves
    positive_valves = [key for key in graph if graph[key].flowrate > 0.0]

    # Part 1
    ITERATIONS = 30 
    visited = set()
    visited.add(START)
    distances = {key: dijkstras(graph, key, set(positive_valves)) for key in positive_valves}
    distances[START] = dijkstras(graph, START, set(positive_valves))
    ans = simulate_valves(graph, distances, START, visited, ITERATIONS, 0) 
    print(ans)


    # Part 2
    # get all unique combinations of each path either you or the elephant could take
    items = frozenset(positive_valves)
    combinations = {frozenset(combination) for combination in itertools.combinations(items, len(items) // 2)}
    splits = {frozenset((combination, items - combination)) for combination in combinations}
    splits = [[list(fs) for fs in split] for split in splits]

    # find the max flow if you and elephant each handle separate valves
    ITERATIONS = 26
    max_flow = 0
    for split in splits:
        my_split = split[0]
        ele_split = split[1]

        my_distances = {key: dijkstras(graph, key, set(my_split)) for key in my_split}
        my_distances[START] = dijkstras(graph, START, set(my_split))
        ele_distances = {key: dijkstras(graph, key, set(ele_split)) for key in ele_split}
        ele_distances[START] = dijkstras(graph, START, set(ele_split))

        my_visited = set()
        my_visited.add(START)
        my_ans = simulate_valves(graph, my_distances, START, my_visited, ITERATIONS, 0)

        ele_visited = set()
        ele_visited.add(START)
        ele_ans = simulate_valves(graph, ele_distances, START, ele_visited, ITERATIONS, 0)

        total_ans = my_ans + ele_ans
        max_flow = max(max_flow, total_ans)

    print(max_flow)