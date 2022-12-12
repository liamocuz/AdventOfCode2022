MAX_SIZE = 100000
TOTAL_SPACE = 70000000
NEEDED_SPACE = 30000000

def build_fs(tree: dict, commands: list[str]):
    """
    Builds the FileSystem using a DFS
    """
    stack = []

    current_tree = tree
    for command in commands:
        parse = command.split(' ')

        if parse[0] == '$':
            cmd = parse[1]
            if cmd == "cd":
                dir_name = parse[2]
                if dir_name == "..":
                    sub_directory_size = current_tree['**']
                    current_tree = stack.pop()
                    current_tree['**'] += sub_directory_size
                else:
                    stack.append(current_tree)
                    current_tree = current_tree[dir_name]
            elif cmd == "ls":
                pass
            else:
                print("ERROR")
                return
        else:
            if parse[0] == "dir":
                dir_name = parse[1]
                init_dir(current_tree, dir_name)
            else:
                current_tree['*'].append((parse[0], parse[1]))
                current_tree['**'] += int(parse[0])

    return

def bfs_print(tree: dict, depth: int):
    indent = ' - '  * depth
    print(f"{indent}Directory Name: ", tree['name'])
    print(f"{indent}Files: ", tree['*'])
    print(f"{indent}Directory Size: ", tree['**'])

    for key in tree:
        if key not in ['name', '*', '**']:
            bfs_print(tree[key], depth + 1)

def dfs1(tree: dict) -> int:
    stack = [tree]
    size = 0

    while stack:
        current = stack.pop()
        for key in current:
            if key not in ['name', '*', '**']:
                stack.append(current[key])
        
        if current['**'] < MAX_SIZE:
            size += current['**']
    
    return size 

def dfs2(tree: dict) -> int:
    fs_size = tree['**']
    print(f"fs_size: {fs_size}")

    size_to_find = NEEDED_SPACE - (TOTAL_SPACE - fs_size)
    
    print(f"size_to_find: {size_to_find}")

    stack = [tree]
    size = float("inf")

    while stack:
        current = stack.pop()

        for key in current:
            if key not in ['name', '*', '**']:
                stack.append(current[key])

        if current['**'] > size_to_find:
            size = min(size, current['**'])

    return size



def init_dir(tree: dict, dir_name: str):
    tree[dir_name] = {}                 # track sub-directories
    tree[dir_name]['*'] = []            # track files
    tree[dir_name]['**'] = 0            # track dir size
    tree[dir_name]['name'] = dir_name   # name of directory, used to debug
    return 

    
if __name__ == "__main__":
    """
    Need to execute all commands to see all files
    Need to do a DFS with this information

    This can be done by creating a tree using a dictionary
    """

    file = open("./input.txt", "r")
    commands = file.read().splitlines()
    file.close()

    tree = {}
    init_dir(tree, '/')
    build_fs(tree, commands)

    # Part 1
    print(dfs1(tree['/']))

    # Part 2
    print(dfs2(tree['/']))
    