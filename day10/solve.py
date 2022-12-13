
def execute(commands: list[str]) -> list[int]:
    """
    Executes the commands and returns the register value at each cycle
    """
    registers: list[int] = []
    register: int = 1

    for command in commands:
        instructions = command.split(' ')
        value = 0

        if len(instructions) == 1:
            registers.append(register)
        elif len(instructions) == 2:
            value = int(instructions[1])
            registers.append(register)
            registers.append(register)
            register += value
        else:
            print("ERROR")
            return None

    return registers 


HEIGHT = 6
WIDTH = 40

def print_image(image):
    for row in image:
        print(row)


def draw_image(registers: list[int]) -> list[list[str]]:
    """
    Given the register value at each cycle, create the image
    """
    image = [['.' for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for cycle, value in enumerate(registers):
        row = cycle // WIDTH
        col = cycle % WIDTH

        if col in [value - 1, value, value + 1]:
            image[row][col] = '#'
    
    return image 


if __name__ == "__main__":
    
    file = open("./input.txt", "r")
    commands = file.read().splitlines()
    file.close()

    # Part 1
    registers = execute(commands)
    signals = [((idx+1) * strength) for idx, strength in enumerate(registers)]
    total = signals[19] + signals[59] + signals[99] + signals[139] + signals[179] + signals[219]
    print(total)

    # Part 2
    image = draw_image(registers)
    print_image(image)
