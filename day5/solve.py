import copy

def build_stacks(stacks: dict, stack_info: list):
    stack_info.reverse()

    parsed_stack_info = []

    # Parse the list of strings into a list of list of letters
    for row in stack_info:
        crates = []
        for offset in range(0, len(row) // 4):
            crate = row[offset * 4 + 1: offset * 4 + 2]
            crates.append(crate)
        parsed_stack_info.append(crates)

    # Take those letters and add to the stack
    for crates in parsed_stack_info:
        for index, crate in enumerate(crates):
            if crate != ' ':
                stacks[index + 1].append(crate)

    return

def execute_commands(stacks: dict, commands: list):
    
    for command in commands:
        tokens = command.split(' ')
        quantity, from_crate, to_crate = int(tokens[1]), int(tokens[3]), int(tokens[5])

        for _ in range(quantity):
            crate_val = stacks[from_crate].pop()
            stacks[to_crate].append(crate_val)

    return

def execute_commands_p2(stacks: dict, commands: list):

    for command in commands:
        tokens = command.split(' ')
        quantity, from_crate, to_crate = int(tokens[1]), int(tokens[3]), int(tokens[5])

        intermediate = []
        for _ in range(quantity):
            crate_val = stacks[from_crate].pop()
            intermediate.append(crate_val)

        while intermediate:
            crate_val = intermediate.pop()
            stacks[to_crate].append(crate_val)

    return

if __name__ == "__main__":
    
    # Treat each stack a FILO stack
    stacks = {
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: [],
        9: []
    }

    file = open("./input.txt", "r")
    file_info = file.readlines()
    file.close()

    stack_info = file_info[0:8]
    commands = file_info[10:]

    build_stacks(stacks, stack_info)
    new_stack = copy.deepcopy(stacks)

    for stack in stacks:
        print(stacks[stack])
    print()

    execute_commands(stacks, commands)

    for stack in stacks:
        print(stacks[stack])
    print()
    
    # Part 2
    for stack in new_stack:
        print(new_stack[stack])
    print()

    execute_commands_p2(new_stack, commands)

    for stack in new_stack:
        print(new_stack[stack])
    print()