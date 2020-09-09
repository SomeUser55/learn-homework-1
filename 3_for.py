"""

Домашнее задание №1

Цикл for: Оценки

* Создать список из словарей с оценками учеников разных классов 
  школы вида [{'school_class': '4a', 'scores': [3,4,4,5,2]}, ...]
* Посчитать и вывести средний балл по всей школе.
* Посчитать и вывести средний балл по каждому классу.
"""

from statistics import mean
from typing import TypedDict, Iterable, Union, List, Dict, Callable
from pprint import pprint

numeric = Union[int, float]

class ClassroomGrades(TypedDict):
    school_class: str
    scores: Iterable[numeric]


def flatten(data: List[Dict], *, key: str) -> List:
    return [
        item
        for dict_ in data
        for item in dict_[key]
    ]
    

def groupby(data: List[Dict], *, on: str, what: str, agg: Callable) -> List[Dict]:
    """Implement pandas-like groupby."""
    total_res = []
    for dict_ in data:
        res = {
            on: dict_[on],
            what: agg(dict_[what])
        }
        total_res.append(res)
    
    return total_res


def main():
    """
    Эта функция вызывается автоматически при запуске скрипта в консоли
    В ней надо заменить pass на ваш код
    """
    school_grades: List[ClassroomGrades] = [
        {'school_class': '4a', 'scores': [3,4,4,5,2]},
        {'school_class': '6b', 'scores': [5, 2, 3, 0]},
        {'school_class': '10a', 'scores': [5, 5, 5, 4]},
        {'school_class': '9b', 'scores': [3, 2, 2, 2]},
    ]

    avg_grade_per_class: List[Dict] = groupby(
        school_grades,
        on='school_class',
        what='scores',
        agg=mean, 
    )

    avg_grade_per_class.sort(key=lambda x: x['scores'])
    print('Average grade per class:')
    pprint(avg_grade_per_class, indent=4)

    all_grades = flatten(school_grades, key='scores')
    print('Average grade in school = {:.2f}'.format(mean(all_grades)))
    
if __name__ == "__main__":
    main()
