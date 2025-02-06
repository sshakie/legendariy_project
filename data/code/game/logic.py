import random


class Logic:
    def __init__(self, dictionary_path=None):
        with open(dictionary_path, 'r', encoding='utf-8') as dictionary:
            self.dictionary = dictionary.read().split('\n')
        self.word = random.choice(self.dictionary).lower()
        print(self.word)

    def check_input_word(self, input_word: str) -> list | bool:  # Функция, возвращающая информацию о слове
        """:return                      | False если слова нет в словаре
           :return list[bool | str]     | False/True Если буквы/буква нет/есть в слове"""

        if input_word not in self.dictionary:
            return False
        data = []
        for i, letter in enumerate(input_word):
            if letter not in self.word:
                data.append(False)
            elif letter != self.word[i]:
                data.append('неверное положение')
            else:
                data.append(True)
        return data
