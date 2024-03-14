"""
Проверка на наличие ошибок в воде
"""


def check(str, num):
    if str in num:
        return str
    elif str == 'exit':
        exit()
    elif str == 'main':
        return 'return_main'
    elif str.isalpha() and str != 'exit' and str != 'main':
        print("Неправильная команда. Допустимые команды: 'exit', 'main'\n")
        return 'restart'
    elif str.isnumeric() and str not in num:
        print(f"Неправильное число. Допустимые числа: {num}\n")
        return 'restart'
    else:
        print('Ошибка ввода. Неправильный ввод\n')
        return 'restart'
