import sys

if __name__ == "__main__":
    """
    Does this in O(N) time
    Uses a sliding window with a dict
    """

    file = open("./input.txt", "r")
    buffer = file.read()
    file.close()

    # test = "qvllwowms|nnt"

    # Part 1 window length
    # WINDOW_LEN = 4

    # Part 2 window length
    WINDOW_LEN = 14

    # Map letters to counts
    seen = {}

    left = 0
    right = 0
    for _ in range(WINDOW_LEN):
        if buffer[right] not in seen:
            seen[buffer[right]] = 0
        seen[buffer[right]] += 1
        right += 1

    if len(seen) == WINDOW_LEN:
        print(f"Found: {right}")
        sys.exit(1)

    for _ in range(WINDOW_LEN, len(buffer)):
        seen[buffer[left]] -= 1
        if seen[buffer[left]] == 0:
            del seen[buffer[left]]
        left += 1
        if buffer[right] not in seen:
            seen[buffer[right]] = 0
        seen[buffer[right]] += 1
        right += 1

        if len(seen) == WINDOW_LEN:
            print(f"Found: {right}")
            sys.exit(1) 


    print("ERROR")
