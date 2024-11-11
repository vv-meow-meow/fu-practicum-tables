class TXTHandler:

    @staticmethod
    def save_table(data, path: str):
        if not data:
            raise ValueError("Table is empty")

        widths = [
            max(len(str(item)) for item in column)
            for column in zip(*data)
        ]

        with open(path, 'w') as file:
            for row in data:
                row_str = " | ".join(f"{str(item):{widths[i]}}" for i, item in enumerate(row))
                file.write(row_str + "\n")
