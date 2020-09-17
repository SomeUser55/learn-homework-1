"""

Домашнее задание №1

Условный оператор: Сравнение строк

* Написать функцию, которая принимает на вход две строки
* Проверить, является ли то, что передано функции, строками.
  Если нет - вернуть 0
* Если строки одинаковые, вернуть 1
* Если строки разные и первая длиннее, вернуть 2
* Если строки разные и вторая строка 'learn', возвращает 3
* Вызвать функцию несколько раз, передавая ей разные праметры
  и выводя на экран результаты

"""

from typing import Optional, Callable
from functools import wraps


def show_func_call(func: Callable) -> Callable:
    """Print function input/output."""
    # TODO func kwargs
    @wraps(func)
    def wrapper(*args):
        res = func(*args)
        args_repr = map(repr, args)
        args_str = ', '.join(args_repr)
        print('{}({}) -> {!r}'.format(
            func.__name__,
            args_str,
            res,
        ))
        return res

    return wrapper


@show_func_call
def check_strings(str1: str, str2: str) -> Optional[int]:
    """Classify input strings."""
    if not all(isinstance(string, str) for string in (str1, str2)):
        res = 0
    elif str1 == str2:
        res = 1
    elif len(str1) > len(str2):
        res = 2
    elif str2 == 'learn':
        res = 3

    return res


def main():
    """
    Эта функция вызывается автоматически при запуске скрипта в консоли
    В ней надо заменить pass на ваш код
    """
    args_to_check = [
        ('string', 1),
        ('same', 'same'),
        ('long string', 'short'),
        (' ', 'learn'),
    ]
    for arg1, arg2 in args_to_check:
        check_strings(arg1, arg2)


if __name__ == "__main__":
    main()
