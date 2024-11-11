import pickle


class PickleHandler:

    @staticmethod
    def load_table(path):
        with open(path, 'rb') as file:
            return pickle.load(file)

    @staticmethod
    def save_table(data, path):
        with open(path, 'wb') as file:
            pickle.dump(data, file)
