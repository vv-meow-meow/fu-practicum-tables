from tabletools import Table, CSVHandler, TXTHandler, PickleHandler

if __name__ == '__main__':
    table = Table()
    table.load_data("./table_samples/customers-100.csv", CSVHandler)

    table.print_table()

    table.save_data("output.pkl", PickleHandler)
    table.save_data("output.txt", TXTHandler)