import csv

class CSVHandler:

    @staticmethod
    def load_table(path):
        with open(path, "r") as file:
            reader = csv.reader(file)
            return list(reader)

    @staticmethod
    def save_table(data, path):
        with open(path, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
