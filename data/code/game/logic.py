import random


class Logic:
    def __init__(self, weight: int, height: int, dictionary_path=None, word=None):
        self.weight = weight
        self.height = height

        try:
            with open(dictionary_path, 'r') as dictionary:
                self.dictionary = dictionary.readlines()
        except Exception:  # TODO Найти исключение и вписать его если файл пустой
            pass  # TODO Вызывать окно если произошла ошибка

        if word is None:
            self.word = random.choice(self.dictionary)
        else:
            self.word = word

        self.right_letters = {}  # Ключ - буква, значение - правильные индексы

        for index in range(len(self.word)):
            if self.word[index] not in self.right_letters.keys():
                self.right_letters[self.word[index]] = [index]
            else:
                self.right_letters[self.word[index]].append(index)

        self.input_word = ''
        self.wrong_letters = []

    def keyboard_press(self, key) -> str:
        if key != 'backspace':  # TODO: Посмотреть как выглядит event backspace
            self.input_word += key
        else:
            self.input_word = self.input_word[:-1]

        return self.input_word

    def get_input_word(self) -> str:
        return self.input_word

    def get_wrong_letters(self) -> list:
        return self.wrong_letters

    def check_input_word(self) -> bool | dict:
        """:return False если слова нет в словаре.
           :return dict[str] = list[int] | None | str Если слово есть в словаре. None - если буквы нет в слове,
            список с индексами этих букв, если буква стоит в правильном месте, строку 'неверное положение'
            если положение неверное"""

        if self.input_word not in self.dictionary:  # Если слова нет в словаре.
            return False
        else:
            data = {}
            for i in range(len(self.input_word)):
                if self.input_word[i] not in self.right_letters.keys():
                    self.wrong_letters.append(self.input_word[i])
                    data[self.input_word[i]] = None
                else:
                    if i in self.right_letters[self.input_word[i]]:
                        if self.input_word[i] not in data.keys():
                            data[self.input_word[i]] = [i]
                        else:
                            if not isinstance(data[self.input_word[i]], str):
                                data[self.input_word[i]].append(i)
                            else:
                                data[self.input_word[i]] = [i]
                    else:
                        data[self.input_word[i]] = 'неверное положение'

        self.input_word = ''
        return data
