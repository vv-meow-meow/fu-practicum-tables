data1 = [
    ["ID", "Name", "Age"],
    [1, "Alice", 23],
    [2, "Bob", 25],
]


class Table:
    def __init__(self, data):
        self.data = data

    def print_table(self):
        for row in self.data:
            print(*row, sep=" | ")


const = Table(data=data1)
const.print_table()
