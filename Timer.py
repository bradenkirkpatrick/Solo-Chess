
import time
class timer():
    def __init__(self):
        self.time = time.process_time()
    def start(self):
        self.time = time.process_time()
    def get(self):
        return time.process_time() - self.time
    def print(self):
        print("time: " + str(self.get()))
    """
    @param zero is always t.start(), to set time to zero. 
    @param function runs the function
    """
    def test(self, zero, function):
        self.print()
