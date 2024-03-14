"""
Утилита со всеми функциями для ПУМа
"""


from pum_def_9_1.binary import print_binary
from pum_def_9_1.linear import print_linear
from pum_def_9_1.sort import print_sort
from pum_def_9_1.error_check import check
from pum_def_9_1.converters import use_converter


while True:
    print("Введите цифру интересующей вас темы\n"
          "1. Линейный поиск\n"
          "2. Бинарный поиск\n"
          "3. Сортировки\n"
          "4. Перевод в системы счисления\n"
          "Для завершения работы введите 'exit'\n")
    select = input()
    correctNumbers = ['1', '2', '3', '4']

    checkResult = check(select, correctNumbers)
    if checkResult == '1':
        print_linear()
    if checkResult == '2':
        print_binary()
    if checkResult == '3':
        print_sort()
    if checkResult == '4':
        use_converter()
    if checkResult == 'restart':
        pass
