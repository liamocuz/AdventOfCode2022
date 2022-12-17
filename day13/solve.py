import ast
from enum import Enum, auto

class Signal(Enum):
    IN_ORDER = auto()
    CONTINUE = auto()
    OUT_OF_ORDER = auto()

def check_arr(left, right) -> Signal:
    llen = len(left)
    rlen = len(right)

    leftIdx = 0
    rightIdx = 0

    inOrder = Signal.CONTINUE
    while leftIdx < llen and rightIdx < rlen:
        leftObj = left[leftIdx]
        rightObj = right[rightIdx]

        isLeftInt = isinstance(leftObj, int)
        isRightInt = isinstance(rightObj, int)

        if isLeftInt and isRightInt:
            if leftObj < rightObj:
                inOrder = Signal.IN_ORDER
            elif leftObj > rightObj:
                inOrder = Signal.OUT_OF_ORDER

        elif isLeftInt and not isRightInt:
            inOrder = check_arr([leftObj], rightObj)

        elif not isLeftInt and isRightInt:
            inOrder = check_arr(leftObj, [rightObj])

        else:
            inOrder = check_arr(leftObj, rightObj)

        if inOrder != Signal.CONTINUE:
            return inOrder

        leftIdx += 1
        rightIdx += 1

    if llen - leftIdx < rlen - rightIdx:
        return Signal.IN_ORDER
    elif llen - leftIdx > rlen - rightIdx:
        return Signal.OUT_OF_ORDER

    return inOrder

def insertion_sort(arrs):
    
    for i in range(1, len(arrs)):
        j = i
        while j > 0 and check_arr(arrs[j], arrs[j - 1]) == Signal.IN_ORDER:
            swap = arrs[j - 1]
            arrs[j - 1] = arrs[j]
            arrs[j] = swap

            j -= 1
    
    return arrs 

if __name__ == "__main__":
    
    file = open("./input.txt", "r")
    lines = file.read().splitlines()
    file.close()

    pairs = []
    for i in range(0,len(lines), 3):
        first, second = lines[i:i+2]
        first = ast.literal_eval(first)
        second = ast.literal_eval(second)
        pairs.append(first)
        pairs.append(second)
        
    # Part 1
    # num = 1
    # total = 0
    # for idx in range(0, len(pairs), 2):
    #     check = check_arr(pairs[idx], pairs[idx + 1])
    #     if check == Signal.IN_ORDER:
    #         total += num
    #     num += 1
    # print(total)

    # Part 2
    # Need to now sort these lines
    sorted_arrs = insertion_sort(pairs)

    idx = 1
    keys = [[[2]], [[6]]]
    decode = 1
    for arr in sorted_arrs:
        # print(idx, arr) 
        if arr in keys:
            decode *= idx
        idx += 1
    print(decode)
    