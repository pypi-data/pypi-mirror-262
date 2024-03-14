import sys
from pum_def_9_1.error_check import check


def use_converter():
    print("""
Выберите функцию:
1. Перевод из десятичной системы в какую-то
2. Перевод из какой-то системы в десятичную
Для выхода в главное меню введите 'main'
""")

    answer = input()
    correct_numbers = ['1', '2']

    check_result = check(answer, correct_numbers)
    if check_result == '1':
        print(to_base(int(input("Введите число в десятичной системе ")), int(input("Введите систему счисления "))))
    elif check_result == '2':
        print(
            to_int(int(input("Введите число в какой-то системе счисления ")), int(input("Введите систему счисления "))))
    elif check_result == 'restart':
        use_converter()
    elif check_result == 'return_main':
        return
    use_converter()


def to_base(decimal, radix):
    if radix > 36:
        sys.exit('converting error.def_to_base')
    number = ''
    while decimal > 0:
        decimal, remainder = divmod(decimal, radix)
        if remainder > 9:
            remainder = chr(ord('A') + remainder - 10)
        number = str(remainder) + number
    return number


def to_int(number, base):
    number = str(number)
    if base > 36:
        sys.exit('converting error.def_to_int')
    table = {'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19, 'K': 20, 'L': 21,
             'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29, 'U': 30, 'W': 32, 'X': 33, 'Y': 34,
             'Z': 35}
    sum = 0
    for i in range(len(number)):
        if number[i].isalpha():
            a = int(len(number) - 1 - i)
            b = base ** a
            c = table.get(number[i])
            sum += c * b
        else:
            a = int(len(number) - 1 - i)
            b = base ** a
            c = int(number[i])
            sum += c * b
    return sum
