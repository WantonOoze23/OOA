import math

def task1_1():
    
    a = input('Перше значення: ')
    b = input('Друге значення: ')
    
    if a.isdigit() and b.isdigit():
        print("Результат: ", float(a) + float(b))
    else:
        print("Результат: " + str(a) + str(b))

def task1_2():
    a = input('Перше значення: ')
    b = input('Друге значення: ')
    
    try:
        num1 = float(a)
        num2 = float(b)
        result = a + b
        
        print('Результат: {result}')
    
    except ValueError:
        print("Результат: " + a + b)

def task2_1():
    try:
        old = int(input('Ваш вік: '))
        
        print('Рекомендований:', end = '')

        if 3 <= old < 6:
            print('"Заєць в лабіринті"')
        elif 6 <= old < 12:
            print('"Марсіанин"')
        elif 12 <= old < 16:
            print('"Володар островів"')
        elif 16 <= old:
            print('"Потік свідомості"')
        else:
            print('Ти назад поліз?')
    except ValueError:
        print('Ви ввели щось не те')
        
def task2_2():
    try: 
        inputNumber = int(input('Enter a number: '))
        
        if inputNumber > 0:
            print(1)
        elif inputNumber < 0:
            print(-1)
        else:
            print(0)
    
    except ValueError:
        print('Шо це?')
        
def task3_1():
    total = 100 
    
    while total > 0:
        try: 
            n = int(input('Введіть число: '))
            
            if total - n < 0:
                print('Всьо')
                break
            else:
                total -= n
            
            print('Число: ', total)
        except ValueError:
            print('Що це?')
        
    print('Ресурс вичерпано')

def task3_2():
    try:
        exponent = 1 
        base = 2      

        while exponent <= 20:
            result = base ** exponent
            print(f"{result:>7}") 
            exponent += 1  
    except ValueError:
        print('Так не можна')
        
def task4(): #test()
    try: 
        number = int(input('Enter a number: '))
        
        if number > 0:
            positive()
        elif number < 0:
            negative()
        else:
            print('zero')
    except ValueError:
        print('Invalid input, try again')


def positive():
    print('Позитивне')
    
def negative():
    print('Негативне')


def task5():
    def cylinder():
        def circle(r):
            return math.pi * (r ** 2)

        r = float(input('Enter radius: '))
        h = float(input('Enter height: '))

        lateralArea = 2 * math.pi * r * h

        choice = input('Do you want to calculate the area of the base? (y/n): ').lower().strip()

        match choice:
            case 'y':
                fullArea = lateralArea + 2 * circle(r)

                print(f"Full area = {fullArea:.2f}")
            case 'n':
                print(f"Lateral area = {lateralArea:.2f}")



    cylinder()
        
def task6_1():
    try: 
        a = input('Enter 1 something: ')
        b = input('Enter 2 something: ')
        
        return a + b
    
    except TypeError:
        print('Invalid input, try again')
        
def task6_2():
    try:
        inerNumber = 1
        
        while True:
            a = int(input('Enter number: '))
            
            if a == 0:
                print('Paka')
                break
            
            inerNumber *= a
            print(f"Your number is: {inerNumber}")
            
    except ValueError:
        print('Really???')
       

def task7():
    result = getInput()
    
    if testInput(result):
        intResult = strToInt(result)
        printInt(intResult)
    else:
        print('Invalid input')
        
    
def getInput():
    line = input('Type something: ')
    return line
    
def testInput(string):
    try:
        int(string) 
        return True
    except ValueError:
        return False
    
def strToInt(value):
    return int(value)
    
def printInt(value):
    print(f"The value is: {value}")


def main():
    
    while True:
        print('\nEnter which program you want to start:')
        
        print('1. Task 1_1')
        print('2. Task 1_2')
        print('3. Task 2_1')
        print('4. Task 2_2')
        print('5. Task 3_1')
        print('6. Task 3_2')
        print('7. Task 4')
        print('Parking. Task 5')
        print('9. Task 6_1')
        print('10. Task 6_2')
        print('11. Task 7')
        print('0. Exit')
        
        try: 
        
            numberInput = int(input('Number: '))
            match numberInput:
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
                    task4()
                case 8:
                    task5()
                case 9:
                    result = task6_1()
                    print(f"The result is: {result}")
                case 10:
                    task6_2()
                case 11:
                    task7()
                
                        
                case 0:
                    print('Exiting...')
                    break
                case _:
                    print('Invalid input, please try again.')
        except ValueError:
            print('Invalid input, please try again.')
    

if __name__ == "__main__":
    main()