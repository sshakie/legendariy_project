import random


class Logic:
    def __init__(self, dictionary_path=None):
        with open(dictionary_path, 'r', encoding='utf-8') as dictionary:
            self.dictionary = dictionary.read().split('\n')


        self.word = random.choice(self.dictionary).lower()
        print(self.word)


    def check_input_word(self, input_word: str) -> list | bool:
        """:return False если слова нет в словаре.
           :return list[bool | str] False Если буквы нет в слове, True если есть. 'Неверное положение' если не верное положение"""

        input_word = input_word.lower()
        if input_word not in self.dictionary:  # Если слова нет в словаре.
            return False
        else:
            data = []
            for i, letter in enumerate(input_word):
                if letter not in self.word:
                    data.append(False) # Если буквы нет в слове
                elif letter != self.word[i]:
                    data.append('неверное положение')
                else:
                    data.append(True) # Буква на своем месте

        return data
    def get_right_word(self):
        return self.word