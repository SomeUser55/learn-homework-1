"""

Домашнее задание №1

Цикл while: ask_user со словарём

* Создайте словарь типа "вопрос": "ответ", например: 
  {"Как дела": "Хорошо!", "Что делаешь?": "Программирую"} и так далее
* Напишите функцию ask_user_dict() которая с помощью input() просит 
  пользователя ввести вопрос, а затем, если вопрос есть в словаре, 
  программа давала ему соотвествующий ответ. Например:

    Пользователь: Что делаешь?
    Программа: Программирую
    
"""

from random import choice

from difflib import get_close_matches
from transliterate import translit

EN_LAYOUT = "QWERTYUIOP[]ASDFGHJKL;'ZXCVBNM,."
RU_LAYOUT = "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ"

EN_RU_MAPPING = dict(zip(EN_LAYOUT, RU_LAYOUT))


def en_to_ru_layout(in_str, layout_mapping):
    out_str = ''
    for char in in_str:
        out_str += layout_mapping.get(char, char) 

    return out_str


def fix_question(from_user, *, layout_mapping, possible_questions, cutoff):
    corrected_layout = en_to_ru_layout(from_user, layout_mapping) 
    matches = get_close_matches(corrected_layout, possible_questions, cutoff=cutoff, n=1)
    if matches:
        return matches[0]   

    corrected_translit = translit(from_user, 'ru')
    matches = get_close_matches(corrected_translit, possible_questions, cutoff=cutoff, n=1)
    if matches:
        return matches[0]   

    return ''


def ask_user(question_answer_catalog, *, layout_mapping, prompt='Спроси меня: \n>>> ', default_answers=['Я не знаю.'], cutoff=0.7):
    """Infinitely answer on user questions."""
    question_answer_catalog = {question.upper(): answer
        for question, answer in question_answer_catalog.items()
    }
    possible_questions = question_answer_catalog.keys()
    while True:
        from_user = input(prompt).upper()
        user_question = fix_question(from_user, layout_mapping=layout_mapping, possible_questions=possible_questions, cutoff=cutoff)
        possible_answers = question_answer_catalog.get(user_question, default_answers) 
        answer = choice(possible_answers)
        print(answer, end='\n\n')


QA_CATALOG = {
    'Как дела?': ['Хорошо!', 'Отлично)', 'Неплохо так', 'Бывало и лучше', 'Сойдёт...'],
    'Что делаешь?': ['Программирую', 'Вышиваю крестиком', 'Отвечаю на твои вопросы'],
    'Лучший ЯП': ['Питон', 'F#', 'GoLang'],
    'Худший ЯП': ['Пыха'],
    'Кто ты': ['Избранный', 'Никто'],
}

if __name__ == "__main__":
    ask_user(QA_CATALOG, layout_mapping=EN_RU_MAPPING)
