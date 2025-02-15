from random import shuffle

class VocabularyMemory:
    def __init__(self):
        self.__vocab_dict_first_lang_key: dict = {}
        self.__vocab_dict_second_lang_key: dict = {v: k for k, v in self.__vocab_dict_first_lang_key.items()}
        self.__vocab_list_first_lang: list = [self.__vocab_dict_first_lang_key.keys()]
        self.__vocab_list_second_lang: list = [self.__vocab_dict_first_lang_key.values()]
        #shuffled vocabulary
        self.__shuffled_vocab_dict_first_lang_key: dict = {}
        self.__shuffled_vocab_dict_second_lang_key: dict = {}
        self.__shuffled_vocab_list_first_lang: list = []
        self.__shuffled_vocab_list_second_lang: list = []
        #copy of shuffled to test and delete vocab
        self.__copy_shuffled_vocab_dict_first_lang_key: dict = {}
        self.__copy_shuffled_vocab_dict_second_lang_key: dict = {}
        self.__copy_shuffled_vocab_list_first_lang: list = []
        self.__copy_shuffled_vocab_list_second_lang: list = []

    def get_vocab_dict_first_lang_key(self) -> dict:
        return self.__vocab_dict_first_lang_key

    def set_vocab_dict_first_lang_key(self, vocab: dict):
        self.__vocab_dict_first_lang_key = vocab
        self.update_vocab_dicts()

    def add_vocab_dict_first_lang_key(self, vocab: dict):
        self.__vocab_dict_first_lang_key.update(vocab)

    def remove_vocab_dict_first_lang_key(self, vocab: dict):
        self.__vocab_dict_first_lang_key.pop(vocab)

    def get_vocab_dict_second_lang_key(self) -> dict:
        return self.__vocab_dict_second_lang_key
    def get_vocab_list_first_lang(self) -> list:
        return self.__vocab_list_first_lang
    def get_vocab_list_second_lang(self) -> list:
        return self.__vocab_list_second_lang
    def get_shuffled_vocab_dict_first_lang_key(self) -> dict:
        return self.__shuffled_vocab_dict_first_lang_key
    def get_shuffled_vocab_dict_second_lang_key(self) -> dict:
        return self.__shuffled_vocab_dict_second_lang_key
    def get_shuffled_vocab_list_first_lang(self) -> list:
        return self.__shuffled_vocab_list_first_lang
    def get_shuffled_vocab_list_second_lang(self) -> list:
        return self.__shuffled_vocab_list_second_lang
    def get_copy_shuffled_vocab_dict_first_lang_key(self) -> dict:
        return self.__copy_shuffled_vocab_dict_first_lang_key
    def get_copy_shuffled_vocab_dict_second_lang_key(self) -> dict:
        return self.__copy_shuffled_vocab_dict_second_lang_key
    def get_copy_shuffled_vocab_list_first_lang(self) -> list:
        return self.__copy_shuffled_vocab_list_first_lang
    def get_copy_shuffled_vocab_list_second_lang(self) -> list:
        return self.__copy_shuffled_vocab_list_second_lang
    def remove_item__copy_shuffled_vocab_dict_first_lang_key(self):
        pass

    def update_vocab_dicts(self):
        self.update_vocab_dict_second_lang_key()
        self.update_vocab_list_first_lang()
        self.update_vocab_list_second_lang()
        self.update_shuffled_vocab()

    def update_vocab_dict_second_lang_key(self):
        self.__vocab_list_first_lang: dict = {v: k for k, v in self.__vocab_dict_first_lang_key.items()}

    def update_vocab_list_first_lang(self):
        self.__vocab_list_first_lang: list = [self.__vocab_dict_first_lang_key.keys()]

    def update_vocab_list_second_lang(self):
        self.__vocab_list_second_lang: list = [self.__vocab_dict_first_lang_key.values()]

    def update_shuffled_vocab(self):
        hilf: list = list(self.__vocab_dict_first_lang_key.copy().items())
        shuffle(hilf)
        self.__shuffled_vocab_dict_first_lang_key: dict = dict(hilf)
        self.__shuffled_vocab_dict_second_lang_key: dict = {v: k for k, v in self.__shuffled_vocab_dict_first_lang_key.items()}
        self.__shuffled_vocab_list_first_lang: list = [self.__shuffled_vocab_dict_first_lang_key.keys()]
        self.__shuffled_vocab_list_second_lang: list = [self.__shuffled_vocab_dict_first_lang_key.values()]

    def update_shuffled_copy(self):
        self.__copy_shuffled_vocab_dict_first_lang_key: dict = self.__shuffled_vocab_dict_first_lang_key.copy()
        self.__copy_shuffled_vocab_dict_second_lang_key: dict = self.__shuffled_vocab_dict_second_lang_key.copy()
        self.__copy_shuffled_vocab_list_first_lang: list = self.__shuffled_vocab_list_first_lang.copy()
        self.__copy_shuffled_vocab_list_second_lang: list = self.__shuffled_vocab_list_second_lang.copy()