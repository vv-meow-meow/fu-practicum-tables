from math import ceil


class TXTHandler:
    """Handler for managing tabular data in TXT format."""

    @staticmethod
    def save_table(data, path: str, max_rows: int):
        if not data:
            raise ValueError("Table is empty")

        widths = [
            max(len(str(item)) for item in column)
            for column in zip(*data)
        ]

        def save_single_file():
            with open(path, 'w') as file:
                for row in data:
                    row_str = " | ".join(f"{str(item):{widths[i]}}" for i, item in enumerate(row))
                    file.write(row_str + "\n")

        if max_rows is None:
            save_single_file()
        elif len(data) > max_rows:
            max_counter = ceil((len(data) - 1) / max_rows)
            last_row = 1
            headers = " | ".join(f"{str(item):{widths[i]}}" for i, item in enumerate(data[0]))

            for counter in range(1, max_counter + 1):

                with open(f"{path[:-4]}_{counter}.txt", 'w') as file:
                    file.write(headers + "\n")
                    for row in data[last_row:last_row + max_rows]:
                        row_str = " | ".join(f"{str(item):{widths[i]}}" for i, item in enumerate(row))
                        file.write(row_str + "\n")

                last_row += max_rows
        else:
            save_single_file()
