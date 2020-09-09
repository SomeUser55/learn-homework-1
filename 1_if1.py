"""

Домашнее задание №1

Условный оператор: Возраст

* Попросить пользователя ввести возраст при помощи input и положить 
  результат в переменную
* Написать функцию, которая по возрасту определит, чем должен заниматься пользователь: 
  учиться в детском саду, школе, ВУЗе или работать
* Вызвать функцию, передав ей возраст пользователя и положить результат 
  работы функции в переменную
* Вывести содержимое переменной на экран

"""

class InvalidAge(Exception):
    """Age out of bounds!"""


def guess_activity(age: int) -> str:
    """Return activity title based on age of user."""
    if age < 0:
        raise InvalidAge

    if age < 7:
        activity = 'nursery_school' 
    elif age < 18:
        activity = 'school'
    elif age < 24:
        activity = 'high school'
    else:
        activity = 'job'
    
    return activity


def main():
    """
    Эта функция вызывается автоматически при запуске скрипта в консоли
    В ней надо заменить pass на ваш код
    """
    age: int = int(input('Enter your age (int): '))
    activity: str = guess_activity(age)
    print('You should go to {}.'.format(activity))


if __name__ == "__main__":
    main()
