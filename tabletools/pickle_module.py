import pickle
from math import ceil


class PickleHandler:
    """Handler for managing tabular data in Pickle format."""

    @staticmethod
    def load_table(*paths: str):
        result = []
        flag = 1
        for path in paths:
            with open(path, 'rb') as file:
                pkl_file: list = pickle.load(file)
                if flag:
                    result.extend(pkl_file)
                    flag = 0
                else:
                    if pkl_file[0] == result[0]:
                        result.extend(pkl_file[1:])
                    else:
                        raise AttributeError("Tables has different columns")

        return result

    @staticmethod
    def save_table(data, path: str, max_rows: int = None):

        def save_single_file():
            with open(path, 'wb') as file:
                pickle.dump(data, file)

        if max_rows is None:
            save_single_file()
        elif len(data) > max_rows:
            max_counter = ceil((len(data) - 1) / max_rows)
            last_row = 1
            headers = data[0]

            for counter in range(1, max_counter + 1):
                cached_data = [headers]
                cached_data += data[last_row:last_row + max_rows]
                with open(f"{path[:-4]}_{counter}.pkl", 'wb') as file:
                    pickle.dump(cached_data, file)

                last_row += max_rows
        else:
            save_single_file()
