from copy import deepcopy


class Table:
    def __init__(self, data=None):
        self._data = data or []

    def load_data(self, path, handler):
        self._data = handler.load_table(path)

    def save_data(self, path, handler):
        handler.save_table(self._data, path)

    def _get_column_widths(self) -> list[int]:
        """Определяет максимальные ширины колонок для красивого форматирования таблицы"""
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

    def get_rows_by_number(self, start, stop=None, copy_table=False):
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
        result = [row for row in self._data if row[0] in values]
        if copy_table: result = deepcopy(result)
        return result

    def _infer_type(self, column):
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
        if not self._data: return {}

        column_types = {}
        for index, column in enumerate(zip(*self._data[1:])):
            inferred_type = self._infer_type(column)
            column_name = index if by_number else self._data[0][index]
            column_types[column_name] = inferred_type
        return column_types

    def set_column_types(self, column_types, by_number=True):
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
        if len(self._data) < 2:
            raise ValueError("Table is empty")

        if isinstance(column, int):
            target_index = column
        elif isinstance(column, str):
            target_index = self._data[0].index(column)
        else:
            raise TypeError("Unexpected type for column")

        return self._data[1][target_index]

    def set_values(self, values: list, column: list | str = 0):
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