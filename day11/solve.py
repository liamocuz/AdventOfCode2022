class Monkey():
    def __init__(self, id: int, items: list, op_code: str, op_val: str, test_val: int, true_loc: int, false_loc: int) -> None:
        self.id = id
        self.items = items
        self.op_code = op_code
        self.op_val = op_val
        self.test_val = test_val
        self.true_loc = true_loc
        self.false_loc = false_loc
        self.counts = 0

    def inspect(self) -> tuple[int]:
        item = self.items.pop(0)
        item = self.operation(item)
        # item //= 3 # part 1
        item = item % 9_699_690 # part 2

        self.counts += 1
        if self.test(item):
            return self.true_loc, item
        else:
            return self.false_loc, item

    def has_items(self) -> bool:
        return len(self.items) != 0

    def operation(self, value) -> int:
        clean_val = self.op_val
        if self.op_val == 'old':
            clean_val = value
        else:
            clean_val = int(self.op_val)
        
        if self.op_code == '+':
            return value + clean_val
        elif self.op_code == '*':
            return value * clean_val

    def test(self, value) -> bool:
        return value % self.test_val == 0

    def __repr__(self) -> str:
        return f"Monkey {self.id}:\nItems: {self.items}\nOperation: {self.op_code}, {self.op_val}\nTest Val: {self.test_val}\nTrue Loc: {self.true_loc}\nFalse Loc: {self.false_loc}\n"

def build_monkeys(info) -> list[Monkey]:

    monkeys = []
    line_size = 6

    for offset in range(0, len(info), line_size + 1):
        id = info[offset].split(' ')[1].strip(':')
        id = int(id)

        items = info[offset + 1].strip().split(' ')[2:]
        items = [int(item.strip(',')) for item in items]
       
        operation = info[offset + 2].strip().split(' ')
        op_code = operation[4]
        op_val = operation[5]

        test = info[offset + 3].strip().split(' ')
        test_val = int(test[3])

        true_test = info[offset + 4].strip().split(' ')
        true_loc = int(true_test[5])

        false_test = info[offset + 5].strip().split(' ')
        false_loc = int(false_test[5])

        monkeys.append(Monkey(id, items, op_code, op_val, test_val, true_loc, false_loc))

    return monkeys

def conduct_rounds(monkeys: list[Monkey], rounds: int) -> int:

    for _ in range(rounds):
        for monkey in monkeys:
            while monkey.has_items():
                send_location, item_value = monkey.inspect()
                monkeys[send_location].items.append(item_value)

    counts = [monkey.counts for monkey in monkeys]
    print(counts)
    counts.sort()

    return counts[-1] * counts[-2]

if __name__ == "__main__":

    file = open("./input.txt")
    info = file.read().splitlines()
    file.close()

    ROUNDS = 10000
    monkeys = build_monkeys(info)
    mb = conduct_rounds(monkeys, ROUNDS)
    print(mb)