from tabletools import Table, CSVHandler, TXTHandler, PickleHandler

if __name__ == '__main__':
    table = Table()
    table.load_table(CSVHandler,
                     "./table_samples/customers-100.csv",
                     "./table_samples/customers-50.csv")

    table.print_table()

    splitted_table_1, splitted_table_2 = table.split(5)

    splitted_table_1.save_table(CSVHandler, "splitted_table_1.csv", max_rows=20)
    splitted_table_2.save_table(PickleHandler, "splitted_table_2.pkl")

    table.save_table(TXTHandler, "table.txt")
