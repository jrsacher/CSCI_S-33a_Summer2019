class Dog:
    # Initialize the class
    def __init__(self, breed, weight, good=True):
        self.breed = breed
        self.weight = weight
        self.good = good
            
    # Speak!
    def bark(self):
        if self.weight < 10:
            print("yip")
        else:
            print("ruff")
            
