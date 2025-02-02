import random


class Logic:
    def __init__(self, dictionary_path=None, word=None):

        try:
            with open(dictionary_path, 'r') as dictionary:
                self.dictionary = dictionary.readlines()
        except Exception:  # TODO Найти исключение и вписать его если файл пустой
            pass  # TODO Вызывать окно если произошла ошибка

        if word is None:
            self.word = 'АРБУЗ'# random.choice(self.dictionary)
        else:
            self.word = word

        self.right_letters = {}  # Ключ - буква, значение - правильные индексы

        for index in range(len(self.word)):
            if self.word[index] not in self.right_letters.keys():
                self.right_letters[self.word[index]] = [index]
            else:
                self.right_letters[self.word[index]].append(index)

        self.wrong_letters = []


    def get_wrong_letters(self) -> list:
        return self.wrong_letters

    def check_input_word(self, input_word: str) -> bool | dict:
        """:return False если слова нет в словаре.
           :return dict[str] = list[int] | None | str Если слово есть в словаре. None - если буквы нет в слове,
            список с индексами этих букв, если буква стоит в правильном месте, строку 'неверное положение'
            если положение неверное"""

        input_word = input_word.upper()
        if False:
            pass # if input_word not in self.dictionary:  # Если слова нет в словаре.
        #     # return False
        else:
            data = {}
            for i in range(len(input_word)):
                if input_word[i] not in self.right_letters.keys():
                    self.wrong_letters.append(input_word[i])
                    data[input_word[i].lower()] = None
                else:
                    if i in self.right_letters[input_word[i]]:
                        if input_word[i] not in data.keys():
                            data[input_word[i].lower()] = [i]
                        else:
                            if not isinstance(data[input_word[i]], str):
                                data[input_word[i].lower()].append(i)
                            else:
                                data[input_word[i].lower()] = [i]
                    else:
                        data[input_word[i].lower()] = 'неверное положение'
        return data
    def get_right_word(self):
        return self.word