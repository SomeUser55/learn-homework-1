"""

Домашнее задание №1

Цикл while: ask_user

* Напишите функцию ask_user(), которая с помощью input() спрашивает 
  пользователя “Как дела?”, пока он не ответит “Хорошо”
   
"""


def ask_user(*, ok_status='Хорошо', prompt='Как дела?', max_tries=-1) -> int:
    """Infitely prompt user mood until its ok."""
    retries = 0
    while mood := input(f'{prompt}\n>>>') != ok_status:
        retries += 1
        if retries == max_tries:
            break

    return retries

    
if __name__ == "__main__":
    retries = ask_user()
    print(f'{retries=}')
