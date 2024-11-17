import csv


class CSVHandler:
    """Handler for managing tabular data in CSV format."""

    @staticmethod
    def load_table(*paths: str):
        result = []
        flag = 1
        for path in paths:
            with open(path, "r") as file:
                reader = csv.reader(file)
                if flag:
                    result.extend(list(reader))
                    flag = 0
                else:
                    if (reader.__next__()) == result[0]:
                        result.extend(list(reader))
                    else:
                        raise AttributeError("Tables has different columns")
        return result

    @staticmethod
    def save_table(data, path: str, max_rows: int = None):

        def save_single_file(path):
            with open(path, "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data)

        if max_rows is None:
            save_single_file(path)
        elif len(data) > max_rows:
            counter = 1
            headers = ",".join(data[0]) + "\n"
            while True:
                if len(data) > 0:
                    with open(f"{path[:-4]}_{counter}.csv", "w", newline='') as file:
                        if counter != 1: file.write(headers)
                        writer = csv.writer(file)
                        writer.writerows(data[:max_rows if len(data) > max_rows else len(data)])
                        data = data[max_rows if len(data) > max_rows else len(data):]
                        counter += 1
                else:
                    break

        else:
            save_single_file(path)
