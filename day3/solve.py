import sys

def get_priority(char: str) -> int:
    if 65 <= ord(char) <= 90:
        return ord(char) - ord('A') + 1 + 26
    elif 97 <= ord(char) <= 122:
        return ord(char) - ord('a') + 1
    else:
        print('Error with getting priority value')
        return -1


if __name__ == "__main__":
    """
    For each rucksack, find the item that exists in each
    Find the priority value of that item
    Add up all of the priorities for each rucksack
    """

    file = open("./input.txt", "r")
    lines = file.read().splitlines()

    # Part 1
    result = 0
    for line in lines:
        half = len(line) // 2
        first, second = set(line[0:half]), set(line[half:])

        # print(f"{first} {second}")
        leftover = first.intersection(second)
        if len(leftover) != 1:
            print("Error: Was more than one leftover")
            sys.exit(1)

        result += get_priority(list(leftover)[0])

    print(result)

    # Part 2
    result = 0
    for line in range(0, len(lines), 3):
        g1 = set(lines[line + 0])
        g2 = set(lines[line + 1])
        g3 = set(lines[line + 2])

        intermediate = g1.intersection(g2)
        leftover = intermediate.intersection(g3)

        print(leftover)

        if len(leftover) != 1:
            print("Error: Was more than one leftover")
            sys.exit(1)

        result += get_priority(list(leftover)[0])

    print(result)
            