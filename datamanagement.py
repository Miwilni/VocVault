class VocabularyMemory:
    def __init__(self, vocab: dict):
        self.__vocab_dict_first_lang_key: dict = vocab
        self.__vocab_dict_second_lang_key: dict = {v: k for k, v in self.__vocab_dict_first_lang_key.items()}
        self.__vocab_list_first_lang: list = [self.__vocab_dict_first_lang_key.keys()]
        self.__vocab_list_second_lang: list = [self.__vocab_dict_first_lang_key.values()]

    def get_vocab_dict_first_lang_key(self) -> dict:
        return self.__vocab_dict_first_lang_key

    def set_vocab_dict_first_lang_key(self, vocab: dict):
        self.__vocab_dict_first_lang_key = vocab
        self.update_vocab_dict_second_lang_key()

    def add_vocab_dict_first_lang_key(self, vocab: dict):
        self.__vocab_dict_first_lang_key.update(vocab)

    def remove_vocab_dict_first_lang_key(self, vocab: dict):
        self.__vocab_dict_first_lang_key.pop(vocab)

    def get_vocab_dict_second_lang_key(self) -> dict:
        return self.__vocab_dict_second_lang_key

    def update_vocab_dict_second_lang_key(self):
        self.__vocab_dict_second_lang_key: dict = {v: k for k, v in self.__vocab_dict_first_lang_key.items()}

    def update_shuffled_vocab(self, vocab: dict):
        pass
