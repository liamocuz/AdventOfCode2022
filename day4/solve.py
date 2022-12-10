class Range():
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper

    def __repr__(self) -> str:
        return f"{self.lower}-{self.upper}"

def get_ranges(range_string: str):
        first, second = range_string.split(',')

        first_vals = first.split('-')
        first_lower = int(first_vals[0])
        first_upper = int(first_vals[1])

        second_vals = second.split('-')
        second_lower = int(second_vals[0])
        second_upper = int(second_vals[1])

        return Range(first_lower, first_upper), Range(second_lower, second_upper)


def contains(range_string: str) -> bool:
        first, second = get_ranges(range_string)    

        if first.lower <= second.lower and first.upper >= second.upper:
            return True
        elif second.lower <= first.lower and second.upper >= first.upper:
            return True
        
        return False

def overlaps(range_string: str) -> bool:
    first, second = get_ranges(range_string)

    return first.upper >= second.lower and second.upper >= first.lower


if __name__ == "__main__":
    """
    Need to find number of pairs where one fully contains the other
    """

    file = open("./input.txt", "r")
    lines = file.read().splitlines()

    # Part 1
    fully_overlap = filter(contains, lines)
    fully_count = len(list(fully_overlap))
    print(fully_count)

    # Part 2
    partially_overlap = filter(overlaps, lines)
    partially_count = len(list(partially_overlap))
    print(partially_count)
