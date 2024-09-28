
class Int:
    def __init__(self, value):
        if isinstance(value, int):
            self.value = value
        else:
            raise ValueError("The value must be an integer.")
        
    def __add__(self, other):
        if  isinstance(other, Int):
            return  Int(self.value + other.value)
        else:
            raise ValueError("The other value must be an integer.")
    
    def __sub__(self, other):
        if  isinstance(other, Int):
            return  Int(self.value - other.value)
        else:
            raise  ValueError("The other value must be an integer.")
    
    def  __mul__(self, other):
        if  isinstance(other, Int):
            return  Int(self.value * other.value)
        else:
            raise  ValueError("The other value must be an integer.")
    
    def  __truediv__(self, other):
        if  isinstance(other, Int):
            if other.value == 0:
                raise  ValueError("Cannot divide by zero.")
            return  Int(self.value // other.value)
        else:
            raise  ValueError("The other value must be an integer.")
        
    def output(self):
        print("the value is: ", self.value)
        
if __name__ == "__main__":
    a = Int(10)
    b = Int(5)
    
    a.output()
    b.output()
    
    c = a + b
    c.output()
    
    d = c - a
    d.output()
    
    e = a * b
    e.output()
    
    f = a / b
    f.output()