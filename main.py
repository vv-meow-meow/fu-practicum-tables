from tabletools import Table, CSVHandler, PickleHandler

if __name__ == '__main__':
    table = Table()
    table.load_data("names.csv", CSVHandler)

    table.print_table()

    table.save_data("output.pkl", PickleHandler)
