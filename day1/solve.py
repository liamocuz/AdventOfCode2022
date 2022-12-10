import heapq

if __name__ == "__main__":
    file = open("./input.txt", "r")
    lines = file.read().splitlines()

    heap = []

    max = 0
    current = 0
    for line in lines:
        print(line)
        if line == '':
            if current > max:
                max = current
            heapq.heappush(heap, current)
            current = 0
        else:
            line_val = int(line)
            current += line_val

    top_three = heapq.nlargest(3, heap)
    top_three_sum = sum(top_three)


    print(f"max: {max}")
    print(f"top three: {top_three}")
    print(f"top three sum: {top_three_sum}")
    