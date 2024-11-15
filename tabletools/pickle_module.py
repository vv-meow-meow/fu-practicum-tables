import pickle


class PickleHandler:

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
    def save_table(data, path: str):
        with open(path, 'wb') as file:
            pickle.dump(data, file)
