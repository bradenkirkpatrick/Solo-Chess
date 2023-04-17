
import time
class Timer():
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
    def test(self, zero, function) -> float:
        self.print()
        return self.get()


"""
testing implementation of timer
"""
def main():
    timer = Timer()
    def sigma_odd_ints_for_1_to_2aplus1(a=1000000):
        Sn = 0
        for An in range(0, a):
            Sn += 2*An + 1
        print(Sn)
    timer.test(timer.start(), sigma_odd_ints_for_1_to_2aplus1())

if __name__ == "__main__":
    main()