
def task1_1():
    string = str(input('Введіть текст:'))

    charU = 0
    charL = 0

    for char in string:
        if char.isalpha():
            if char.isupper():
                charU += 1
            elif char.islower():
                charL += 1
    print(charU, ", ", charL)
    if charU == charL:
        print(string.lower(), ' 1')
    elif charU > charL:
        print(string.upper(), ' 2')
    elif charU < charL:
        print(string.lower(), ' 3')

def task1_2():
    n1 = input('Введіть 1 число: ')
    n2 = input('Введіть 2 число: ')

    if n1.isdigit() and n2.isdigit():
        print(f"{n1} + {n2} = ",n1+n2)
    else:
        print('Введено не коректні значення!')


def task2_1():


def main():
    task2_1()

if __name__ == '__main__':
    main()