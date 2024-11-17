from tabletools import Table, CSVHandler, TXTHandler, PickleHandler

if __name__ == '__main__':
    table = Table()
    table.load_table(CSVHandler,
                     "./table_samples/customers-100.csv",
                     "./table_samples/customers-50.csv")

    table.print_table()

    table.save_table(CSVHandler, "output.csv", max_rows=20)
    table.save_table(PickleHandler, "output.pkl")
    table.save_table(TXTHandler, "output.txt")
