import random


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
        print(f"{n1} + {n2} = ",int(n1) + int(n2))
    else:
        print('Введено не коректні значення!')


def task2_1():
    my_list = [1,2,3,4,5]

    copy1 = my_list.copy()
    copy2 = my_list[:]

    copy1.append(6)
    copy2.append(7)

    print(f'{copy1}\n{copy2}')

def task2_fill(min: int, max: int, i):
        return tuple(random.randint(min,max) for _ in range(i))

def task2_2():
    tuple1 = task2_fill(0, 5,10)

    tuple2 = task2_fill(-5, 0,10)

    print(f'{tuple1}\n{tuple2}')

    tuple3 = tuple1 + tuple2

    print(f"{tuple3}\nКількість нулів: {tuple3.count(0)}")

def task3_1():
    faculty = {
        'TV-31' : 21,
        'TV-32' : 22,
        'TV-33' : 24,
    }

    faculty['TV-31'] = 23
    faculty['TV-22'] = 19

    print(faculty)

    del faculty['TV-32']

    print(f"{faculty}\nКількість студентів: {sum(faculty.values())}")


def task3_rotate(dict):
       reversed_dict = {value: key for key, value in dict}
       return reversed_dict

def task3_2():
    dict = {
        1 : "Товар 1",
        2 : "Товар 2",
        3 : "Товар 3",
        4 : "Товар 4",
    }
    print(dict)

    dict_items = task3_rotate(dict.items())

    print(dict_items)

def task4_1():
    eng = 'data.txt'
    ua = 'data_ua.txt'

    dict = {
        "one": "один",
        "two": "два",
        "three": "три",
        "four": "чотири",
        "five": "п'ять"
    }
    with open(eng, 'r') as file_eng:
        with open(ua, 'w') as file_ua:
            for line in file_eng:
                for eng_word, ua_word in dict.items():
                    line = line.replace(eng_word, ua_word)
                file_ua.write(line)
    print('Перевіряйте файли')

def task4_2():
    filename = 'nums.txt'

    with open(filename, mode='r') as file_nums:
        nums = file_nums.read().split()

        print(f"Сума = {sum(map(int, nums))}")




def main():
    while True:
        print('\n1. Завдання 1.1\n2. Завдання 1.2\n3. Завдання 2.1\n4. Завдання 2.2\n5. Завдання 3.1\n6. Завдання 3.2\n7. Завдання 4.1\n8. Завдання 4.2\n0. Вийти')
        try:
            choice = int(input('Введіть значення:'))
        except ValueError:
            continue

        match choice:
            case 1:
                task1_1()
            case 2:
                task1_2()
            case 3:
                task2_1()
            case 4:
                task2_2()
            case 5:
                task3_1()
            case 6:
                task3_2()
            case 7:
                task4_1()
            case 8:
                task4_2()

            case 0:
                print('Exit')
                break
            case _:
                print('Error, wrong action!')



if __name__ == '__main__':
    main()