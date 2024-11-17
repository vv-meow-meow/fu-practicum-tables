from __future__ import annotations  # Type hinting

from copy import deepcopy
from typing import Type, TYPE_CHECKING, Tuple  # Type hinting

if TYPE_CHECKING:  # Type hinting
    from tabletools import CSVHandler, PickleHandler, TXTHandler  # Type hinting


class Table:
    """Class to manage tabular data in memory with support for various file operations.

    Attributes:
        _data (list[list[Any]]): Internal representation of table data as a list of lists.
    """

    def __init__(self, data=None):
        self._data = data or []

    def load_table(self,
                   handler: Type[CSVHandler | PickleHandler],
                   *paths: str):
        """Loads table data using the specified handler"""
        self._data = handler.load_table(*paths)

    def save_table(self,
                   handler: Type[CSVHandler | PickleHandler | TXTHandler],
                   path: str,
                   max_rows: int = None):
        """
        Saves table data using the specified handler.

        Args:
            handler (Type[CSVHandler | PickleHandler | TXTHandler]): Handler class to save data.
            path (str): Path to save the file.
            max_rows (int, optional): Maximum rows per file. Defaults to None.
        """
        handler.save_table(self._data, path, max_rows)

    def _get_column_widths(self) -> list[int]:
        return [
            max(len(str(item)) for item in column)
            for column in zip(*self._data)
        ]

    def print_table(self) -> None:
        if not self._data:
            print("Table is empty")
            return

        widths = self._get_column_widths()
        for row in self._data:
            row_str = " | ".join(f"{str(item):<{widths[i]}}" for i, item in enumerate(row))
            print(row_str)

    def get_rows_by_number(self,
                           start,
                           stop=None,
                           copy_table=False):
        """
        Retrieves rows by their numeric indices.

        Args:
            start (int): The starting row index.
            stop (int, optional): The stopping row index. Defaults to None.
            copy_table (bool, optional): Whether to return a copy of the rows. Defaults to False.

        Returns:
            list[list[Any]]: A list of rows from the specified range.
        """
        match stop:
            case None:
                result = [self._data[start]]
            case -1:
                result = self._data[start:]
            case _:
                result = self._data[start - 1:stop]

        return deepcopy(result) if copy_table else result

    def get_rows_by_index(self,
                          *values,
                          copy_table=False):
        """Retrieves rows by matching the first column's value"""
        result = [row for row in self._data if row[0] in values]
        if copy_table: result = deepcopy(result)
        return result

    def _infer_type(self, column):
        """Infers the data type of column"""
        types = set()
        for value in column:
            if isinstance(value, int):
                types.add(int)
            elif isinstance(value, bool):
                types.add(bool)
            elif isinstance(value, float):
                types.add(float)
            else:
                if value.isdigit():
                    types.add(int)
                else:
                    try:
                        float(value)
                        types.add(float)
                    except ValueError:
                        if value.lower() in ('true', 'false'):
                            types.add(bool)
                        else:
                            types.add(str)

        if len(types) == 1:
            return next(iter(types))
        return str

    def get_column_types(self, by_number=True):
        """Determines the types of each column in the table.

        Args:
            by_number (bool, optional): Whether to use column numbers as keys. Defaults to True.

        Returns:
            dict: A dictionary mapping column names or indices to their inferred types.
        """
        if not self._data: return {}

        column_types = {}
        for index, column in enumerate(zip(*self._data[1:])):
            inferred_type = self._infer_type(column)
            column_name = index if by_number else self._data[0][index]
            column_types[column_name] = inferred_type
        return column_types

    def set_column_types(self,
                         column_types,
                         by_number=True):
        """Sets the types of specified columns.

        Args:
            column_types (dict): A dictionary mapping column names or indices to desired types.
            by_number (bool, optional): Whether to use column numbers as keys. Defaults to True.

        Raises:
            ValueError: If the table is empty or conversion fails for a value.
        """
        if not self._data:
            raise ValueError("Table is empty")

        for key, desired_type in column_types.items():
            col_index = key if by_number else self._data[0].index(key)

            for row in self._data[1:]:
                try:
                    row[col_index] = desired_type(row[col_index])
                except ValueError:
                    raise ValueError(f"Cannot convert value '{row[col_index]}' to {desired_type}'")

    def get_values(self, column: int | str = 0) -> list:
        """Retrieves all values in a specified column.

        Args:
            column (int | str, optional): The column index or name. Defaults to 0.

        Returns:
            list: A list of values from the specified column.

        Raises:
            TypeError: If the column type is invalid.
        """
        if isinstance(column, int):
            target_index = column
        elif isinstance(column, str):
            target_index = self._data[0].index(column)
        else:
            raise TypeError("Unexpected type for column")

        for index, column in enumerate(zip(*self._data[1:])):
            if index == target_index:
                return list(column)

    def get_value(self, column=0):
        """Retrieves the first value in a specified column.

        Args:
            column (int | str, optional): The column index or name. Defaults to 0.

        Returns:
            Any: The first value in the specified column.

        Raises:
            ValueError: If the table is empty.
            TypeError: If the column type is invalid.
        """
        if len(self._data) < 2:
            raise ValueError("Table is empty")

        if isinstance(column, int):
            target_index = column
        elif isinstance(column, str):
            target_index = self._data[0].index(column)
        else:
            raise TypeError("Unexpected type for column")

        return self._data[1][target_index]

    def set_values(self,
                   values: list,
                   column: list | str = 0):
        """Updates all values in a specified column.

        Args:
            values (list): The new values to set in the column.
            column (int | str, optional): The column index or name. Defaults to 0.

        Raises:
            TypeError: If the column type is invalid.
            ValueError: If the number of values does not match the table rows.
        """
        if isinstance(column, int):
            target_col_index = column
        elif isinstance(column, str):
            target_col_index = self._data[0].index(column)
        else:
            raise TypeError("Unexpected type for column")

        if len(values) != len(self._data[1:]):
            raise ValueError("Values must have same amount as original table")

        for i, value in enumerate(values):
            self._data[i + 1][target_col_index] = value

    def set_value(self,
                  value,
                  column: list | str = 0):
        """Updates the first value in a specified column.

        Args:
            value (Any): The new value to set.
            column (int | str, optional): The column index or name. Defaults to 0.

        Raises:
            ValueError: If the table is empty.
            TypeError: If the column type is invalid.
        """
        if len(self._data) < 2:
            raise ValueError("Table is empty")

        if isinstance(column, int):
            target_index = column
        elif isinstance(column, str):
            target_index = self._data[0].index(column)
        else:
            raise TypeError("Unexpected type for column")

        self._data[1][target_index] = value

    def concat(self,
               table_1: Table,
               table_2: Table):
        """Concatenates two tables into the current table.

        Args:
            table_1 (Table): The first table.
            table_2 (Table): The second table.

        Raises:
            ValueError: If the current table is not empty or headers conflict.
        """
        if self._data:
            raise ValueError("Table is not empty, cannot concatenate tables")

        if not table_1._data:
            raise ValueError("Table #1 is empty")
        elif not table_2._data:
            raise ValueError("Table #2 is empty")

        data_1 = table_1._data
        data_2 = table_2._data

        headers = [*data_1[0], *data_2[0]]

        if len(headers) != len(set(headers)):
            duplicates = [header for header in headers if headers.count(header) > 1]
            raise ValueError(f"Duplicate header found: {', '.join(duplicates)}")

        result_data = [*list(zip(*data_1)), *list(zip(*data_2))]
        expected_row_length = len(result_data[0])
        for row in result_data:
            if len(row) != expected_row_length:
                raise ValueError("Row length mismatch")

        self._data = [list(item) for item in list(zip(*result_data))]

    def split(self,
              row_number: int) -> Tuple[Table, Table]:
        """Splits the table into two parts based on a row number.

        Args:
            row_number (int): The row number to split at.

        Returns:
            tuple[Table, Table]: Two `Table` objects representing the split data.

        Raises:
            ValueError: If the table is empty.
        """
        if not self._data:
            raise ValueError("Table is empty")

        transported = [list(item) for item in zip(*self._data)]
        data_part_1 = [list(item) for item in zip(*transported[:row_number - 1])]
        data_part_2 = [list(item) for item in zip(*transported[row_number - 1:])]

        return (
            Table(data=data_part_1),
            Table(data=data_part_2)
        )
