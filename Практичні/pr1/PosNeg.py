def main():
    inputNumber = float(input('Enter a number: '))
    
    if inputNumber < 0:
        print('-1')
    elif inputNumber >= 0:
        print('1')


if __name__ == "__main__":
    main()