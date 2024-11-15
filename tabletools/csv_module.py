import csv


class CSVHandler:

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
    def save_table(data, path: str):
        with open(path, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
