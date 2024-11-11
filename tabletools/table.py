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
