import pymorphy3

def filter_nouns(text):
    morph = pymorphy3.MorphAnalyzer()

    nouns = [word.lower() for word in text if 'NOUN' in morph.parse(word)[0].tag and morph.parse(word)[0].tag.case == 'nomn' and '-' not in word]
    return '\n'.join(nouns)

# Пример использования
with open('words-length-8.txt', encoding='utf-8') as f:
    text = f.read().split('\n')
filtered_text = filter_nouns(text)
with open('words-length-8.txt', 'w', encoding='utf-8') as f:
    f.write(filtered_text)