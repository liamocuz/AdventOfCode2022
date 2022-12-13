
class Node:
    def __init__(self, row: int, col: int, value):
        self.id = str(row) + '-' + str(col)
        self.row = row
        self.col = col
        self.value = value
        self.GScore = float("inf")  # distance from start
        self.FScore = float("inf")  # estimated distance to end
        self.previous = None        # node that this node came from

    def __repr__(self) -> str:
        return f"{self.id}"

def aStar(startRow, startCol, endRow, endCol, graph):
    """
    AStar algorithm 
    """
    nodes = initializeNodes(graph)
    startNode = nodes[startRow][startCol]
    endNode = nodes[endRow][endCol]

    startNode.GScore = 0
    startNode.FScore = getHeuristic(startNode, endNode)

    nodesToVisit = [startNode]
    while len(nodesToVisit) > 0:
        currentMinDistanceNode = nodesToVisit.pop(0)

        if currentMinDistanceNode == endNode:
            break
    
        neighbors = get_neighbors(nodes, currentMinDistanceNode)
        for neighbor in neighbors:

            tentativeDistanceToNeighbor = currentMinDistanceNode.GScore + 1
            if tentativeDistanceToNeighbor >= neighbor.GScore:
                continue
            neighbor.previous = currentMinDistanceNode
            neighbor.GScore = tentativeDistanceToNeighbor
            neighbor.FScore = tentativeDistanceToNeighbor + getHeuristic(neighbor, endNode)

            if neighbor not in nodesToVisit:
                nodesToVisit.append(neighbor)

    return reconstructPath(endNode)

def getHeuristic(currentNode, endNode):
    """
    Calculates a Manhattan distance from a node to the end node
    Manhattan Distance = abs(currentNode.row - endNode.row) + abs(currentNode.col - endNode.col)
    """
    return abs(currentNode.row - endNode.row) + abs(currentNode.col - endNode.col)

def get_height(nodes: list[list[Node]], coord) -> int:
    row, col = coord
    char = nodes[row][col].value
    if char == 'S':
        return ord('a')
    elif char == 'E':
        return ord('z')
    return ord(char)

def get_neighbors(nodes: list[list[Node]], node: Node):
    neighbors = []
    row, col = node.row, node.col
    current_height = get_height(nodes, (row, col))
    
    row_max = len(nodes)
    col_max = len(nodes[0])

    up, down, left, right = (row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)

    if row - 1 >= 0 and (current_height - get_height(nodes, up)) >= -1:
       x, y = up
       neighbors.append(nodes[x][y]) 
    if row + 1 < row_max and (current_height - get_height(nodes, down)) >= -1:
        x, y = down 
        neighbors.append(nodes[x][y]) 
    if col - 1 >= 0 and (current_height - get_height(nodes, left)) >= -1:
       x, y = left 
       neighbors.append(nodes[x][y]) 
    if col + 1 < col_max and (current_height - get_height(nodes, right)) >= -1:
       x, y = right
       neighbors.append(nodes[x][y]) 

    return neighbors

def reconstructPath(endNode):
    if not endNode.previous:
        return []
    
    path = []
    currentNode = endNode

    while currentNode:
        path.append([currentNode.row, currentNode.col])
        currentNode = currentNode.previous

    return path[::-1]


def initializeNodes(graph: list[list[str]]):
    """
    Turns the graph of info into a graph of nodes
    """
    nodes = []

    for i, row in enumerate(graph):
        nodes.append([])
        for j, value in enumerate(row):
            nodes[i].append(Node(i, j, value))

    return nodes


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

def get_starts(grid):
    starts = []

    for rowIdx in range(len(grid)):
        for colIdx in range(len(grid[rowIdx])):
            current_char = grid[rowIdx][colIdx] 
            if current_char == 'a':
                starts.append((rowIdx, colIdx))

    return starts 

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


    # Part 1
    path = aStar(start[0], start[1], end[0], end[1], grid)
    # print(path)
    print(len(path) - 1)

    # Part 2
    starts = get_starts(grid)
    starts.append(start)
    # print(starts)

    paths = []
    for new_start in starts:
        path = aStar(new_start[0], new_start[1], end[0], end[1], grid) 
        if len(path) > 0:
            paths.append(path)
    steps = [len(path) - 1 for path in paths] 

    shortest = min(steps)
    print(shortest)