def output(employees):
    
    for emp in employees:
        print(f"{emp['first_name']} {emp['last_name']}, Birth: {emp['dob']}, Position: {emp['position']}, Salary: {emp['salary']}")


def sortByAlphabet(employees):
    sortedAlpha = sorted(employees, key=lambda  x: (x['first_name'], ['last_name']))
    
    return sortedAlpha
    
def sortBySalary(employees, lowerSalary):
    sortedEmp = [emp for emp in employees if emp['salary'] >= lowerSalary]
    
    return sortedEmp    

def addEmployee():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    dob = input('Enter date of birth: ')
    position  = input('Enter position: ')
    
    try:
        salary = float(input('Enter salary: '))
    except ValueError:
        print('Invalid salary')
    
    employee = {
        "first_name": first_name,
        "last_name": last_name,
        "dob": dob,
        "position": position,
        "salary": salary
    }
    
    return employee

def main():
    employees = [
        {"first_name": "Ivan", "last_name": "Petrenko", "dob": "1990-03-15", "position": "Manager", "salary": 1200},
        {"first_name": "Olga", "last_name": "Shevchenko", "dob": "1985-07-22", "position": "Engineer", "salary": 1400},
        {"first_name": "Mykola", "last_name": "Stepanenko", "dob": "1975-09-01", "position": "Technician", "salary": 1100},
        {"first_name": "Oksana", "last_name": "Koval", "dob": "1995-11-13", "position": "Designer", "salary": 1500},
        {"first_name": "Dmytro", "last_name": "Taran", "dob": "1982-05-17", "position": "Developer", "salary": 1600}
    ]
    while True:
        try:
            print('\nMenu:')
            print('1. In alphabet order\n2. Employees with higher salary\n3. Add new employee\n4. Clear array\n0. Exit')
            choice = int(input("Enter your choice: "))
            
            match choice:
                case 1:
                    sortedEmployees = sortByAlphabet(employees)
                    print("Employees sorted by alphabet:")
                    output(sortedEmployees)
                case 2:
                    lowerSalary = float(input("Enter salary threshold: "))
                    sortedEmployees = sortBySalary(employees, lowerSalary)
                    
                    if sortedEmployees:  
                        print(f"Employees with salary greater than or equal to {lowerSalary}:")
                        output(sortedEmployees)
                    else:
                        print("No employees with salary greater than or equal to the threshold.")
                case 3:
                    newEmployee = addEmployee()
                    employees.append(newEmployee)
                    print("New employee added successfully.")
                case 4:
                    employees.clear()
                    print("Successfully cleared", employees)
                case 0:
                    print("Exiting program.")
                    break
                case _:
                    print("Invalid choice.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main() 