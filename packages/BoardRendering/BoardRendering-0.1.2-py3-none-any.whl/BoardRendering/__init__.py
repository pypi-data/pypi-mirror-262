
class Exceptions:
    """All Exceptions"""
    class InvalidPosition(Exception):
        """Caused by a position value being invalid"""
        pass

class Board:
    """Class of the board to use them"""
    def __init__(self, size : int, default : str):
        self.size = size
        if default is not None: self.default = default
        else: self.default = "0"
        self.pixels = size * size
        xbase = ""
        for i in range(0, size):
            xbase = xbase + self.default
        sd = ""
        for i in range(0, size):
            sd = sd + xbase
        self.BD = sd
        display = ""
        for i in range(0, size):
            if i != self.size - 1: n = "\n"
            else: n = ""
            display = display + f"{xbase}{n}"
        self.display = display

    def get(self, position : tuple):
        """Returns the value of the position"""
        x = position[0]
        y = position[1]
        if x > self.size - 1: raise Exceptions.InvalidPosition("Position out of range")
        if y > self.size - 1: raise Exceptions.InvalidPosition("Position out of range")
        if x <  0: raise Exceptions.InvalidPosition("Position out of range")
        if y < 0: raise Exceptions.InvalidPosition("Position out of range")
        b = self.display.replace("\n", "")
        return(b[x + (y * self.size)])
    
    def set(self, position : tuple, new : str):
        """Sets the position of a value"""
        x = position[0]
        y = position[1]
        if x > self.size - 1: raise Exceptions.InvalidPosition("Position out of range")
        if y > self.size - 1: raise Exceptions.InvalidPosition("Position out of range")
        if x <  0: raise Exceptions.InvalidPosition("Position out of range")
        if y < 0: raise Exceptions.InvalidPosition("Position out of range")
        b = self.display
        b = b.replace("\n", "")
        bl = list(b)
        bl[x + (y * self.size)] = new
        newb = ""
        index = 0
        for l in bl:
            if index != self.size - 1: 
                newb = newb + l
                index += 1
            else: 
                newb = newb + f"{l}\n"
                index = 0
        self.display = newb
    
    def instances(self, search : str):
        """Returns a list of tuples of the positions of all instances of the provided Search"""
        found = []
        for y in range(0, self.size):
            for x in range(0, self.size):
                if self.get(position=(x, y)) == search: found.append((x, y))
        return(found)

    def randomposition(self):
        import random
        x = random.randint(0, self.size - 1)
        y = random.randint(0, self.size - 1)
        return((x,y))

    def DisplayBoard(self, update):
        """Starts a listener which constantly updates the board by you updating it
        
            Use the Update param to set a Update function"""
        pastboard = ""
        while True:
            s = update()
            if s is True:
                break
            if pastboard != self.display:
                pastboard = self.display
                import os
                os.system("cls")
                print(self.display)


