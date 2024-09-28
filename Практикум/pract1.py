import math

def task1():
    while True:
        try:
            a = float(input('Input a: '))
            b = float(input('Input b: '))
            c = float(input('Input c: '))
                
            while True:
                try:
                    xBeginning = int(input('Enter the beginning of the range: '))
                    xEnd = int(input('Enter the end of the range: '))
                    h = float(input('Enter the h: '))  # Ввод шага
                    
                    if xBeginning >= xEnd:
                        print("Error: The beginning of the range must be less than ending.")
                    elif h <= 0:
                        print("Error: h must be greater than 0.")
                    elif xBeginning + h >xEnd:
                        print("Error: The end of the range must be greater than beginning + h.")
                    else:
                        break
                except ValueError:
                    print("Error: Please enter a valid number.")
                
                    
            f = 0
            x = xBeginning

            while x <= xEnd:  
                if (x + 2 > 0 and c > 0):
                    f += (b + 1) / (a * x) - (1 + c) / (3 * x)
                    print('First')
                    output(x, f)
                elif (x + 2 < 0 and b - c < 0):
                    print('Second')
                    f += (x - 2 * a) / (pow(b, 2)) + x
                    output(x, f)
                else:
                    print('Third')
                    f += math.sqrt(pow(x, 2) + 1) / (3 * a * b * c)
                    output(x, f)
                
                x += h
            
        except ZeroDivisionError:
            print("Error: division by zero encountered.")
        except ValueError:
            print("Error: invalid input. Please enter valid numbers.")

def output(x, f):
    print(f"If x = {x:.2f}, f = {f:.4f}")

if __name__ == "__main__":
    task1()
