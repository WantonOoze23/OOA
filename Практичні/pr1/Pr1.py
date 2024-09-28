def task1():
    varInt = 10
    varFloat = 8.4 
    var_str = "No"

    varBig = varInt * 3.5
    varFloat -= 1
    varStr = var_str * 2 + "Yes" * 3

    print(varInt)
    print(varFloat)
    print(var_str)
    print(varBig)
    print(varStr)

def task2():
    name = input('What is your name? ')
    age = input('How old are you? ')
    placeToLive = input('Where do you live? ')

    print('This is ' + name)
    print('They are ' + age + ' years old')
    print('They live in ' + placeToLive)

    task = 4 * 100 - 54
    
    userInput = int(input('What is the answer to 4 * 100 - 54? '))
    
    if userInput == task:
        print(f'{userInput} is the right answer')
    else:
        print(f'{userInput} is not correct')

    first = int(input('Enter first number: '))
    second = int(input('Enter second number: '))
    third = int(input('Enter third number: '))
    fourth = int(input('Enter fourth number: '))

    print(f"{(first + second) / (third + fourth):.2f}")
    
def task3():
    cost = int(input('Enter actual cost: '))
    amount = int(input('Enter amount: '))
    
    price = cost * amount
    
    if cost < 0 and amount < 0:
        print('Invalid input. Error')
    else:
        print(f"Actual price is: {price:.2f}")
    
    a = int(input('\nEnter first number: '))
    b = int(input('Enter second number: '))
    
    if a > 10 or b < 15:
        print(a*b)
    else:
        print('Da')

    
def main():
    while True:
        print('Enter which program you want to start:')
        print('1. Task 1')
        print('2. Task 2')
        print('3. Task 3')
        
        print('0. Exit')

        numberInput = int(input('Number: '))

        if numberInput == 1:
            task1()
        elif numberInput == 2:
            task2()
        elif numberInput == 3:
            task3()
        elif numberInput == 0:
            print('Exiting...')
            break
        else:
            print('Invalid input, please try again.')

if __name__ == "__main__":
    main()
