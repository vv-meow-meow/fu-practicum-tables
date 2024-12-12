from __future__ import annotations  # Type hinting

from copy import deepcopy
from typing import Type, TYPE_CHECKING, Tuple  # Type hinting

if TYPE_CHECKING:  # Type hinting
    from tabletools import CSVHandler, PickleHandler, TXTHandler  # Type hinting


class Table:
    """Класс для работы с табличными данными в памяти с поддержкой операций с файлами.

    Attributes:
        _data (list[list[Any]]): Внутреннее представление таблицы в виде списка списков.
    """

    def __init__(self, data=None):
        self._data = data or []

    def load_table(self,
                   handler: Type[CSVHandler | PickleHandler],
                   *paths: str):
        """Загружает данные таблицы с использованием указанного обработчика."""
        self._data = handler.load_table(*paths)

    def save_table(self,
                   handler: Type[CSVHandler | PickleHandler | TXTHandler],
                   path: str,
                   max_rows: int = None):
        """
        Сохраняет данные таблицы с использованием указанного обработчика.

        Args:
            handler (Type[CSVHandler | PickleHandler | TXTHandler]): Класс обработчика для сохранения данных.
            path (str): Путь для сохранения файла.
            max_rows (int, optional): Максимальное количество строк на файл. По умолчанию None.
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
        Извлекает строки по их числовым индексам.

        Args:
            start (int): Начальный индекс строки.
            stop (int, optional): Конечный индекс строки. По умолчанию None.
            copy_table (bool, optional): Возвращать ли копию строк. По умолчанию False.

        Returns:
            list[list[Any]]: Список строк из указанного диапазона.
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
        """Извлекает строки, соответствующие значениям в первом столбце."""
        result = [row for row in self._data if row[0] in values]
        if copy_table: result = deepcopy(result)
        return result

    def _infer_type(self, column):
        """Определяет тип данных для столбца."""
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
        """
        Определяет типы данных для каждого столбца таблицы.

        Args:
            by_number (bool, optional): Использовать ли номера столбцов в качестве ключей. По умолчанию True.

        Returns:
            dict: Словарь, сопоставляющий названия или индексы столбцов с их определёнными типами.
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
        """
        Устанавливает типы данных для указанных столбцов.

        Args:
            column_types (dict): Словарь, сопоставляющий названия или индексы столбцов с желаемыми типами.
            by_number (bool, optional): Использовать ли номера столбцов в качестве ключей. По умолчанию True.

        Raises:
            ValueError: Если таблица пуста или преобразование значения не удалось.
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
        """
        Извлекает все значения из указанного столбца.

        Args:
            column (int | str, optional): Индекс или название столбца. По умолчанию 0.

        Returns:
            list: Список значений из указанного столбца.

        Raises:
            TypeError: Если тип столбца недопустим.
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
        """
        Извлекает первое значение из указанного столбца.

        Args:
            column (int | str, optional): Индекс или название столбца. По умолчанию 0.

        Returns:
            Any: Первое значение в указанном столбце.

        Raises:
            ValueError: Если таблица пуста.
            TypeError: Если тип столбца недопустим.
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
        """
        Обновляет все значения в указанном столбце.

        Args:
            values (list): Новые значения для столбца.
            column (int | str, optional): Индекс или название столбца. По умолчанию 0.

        Raises:
            TypeError: Если тип столбца недопустим.
            ValueError: Если количество значений не совпадает с количеством строк в таблице.
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
        """
        Обновляет первое значение в указанном столбце.

        Args:
            value (Any): Новое значение.
            column (int | str, optional): Индекс или название столбца. По умолчанию 0.

        Raises:
            ValueError: Если таблица пуста.
            TypeError: Если тип столбца недопустим.
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
        """
        Объединяет две таблицы в текущую таблицу.

        Args:
            table_1 (Table): Первая таблица.
            table_2 (Table): Вторая таблица.

        Raises:
            ValueError: Если текущая таблица не пуста или заголовки конфликтуют.
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
        """
        Разделяет таблицу на две части по номеру строки.

        Args:
            row_number (int): Номер строки, по которой будет выполнено разделение.

        Returns:
            tuple[Table, Table]: Два объекта `Table`, представляющих разделённые данные.

        Raises:
            ValueError: Если таблица пуста.
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
