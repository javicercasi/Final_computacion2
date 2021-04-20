import threading
import time
from ads import pr
import queue

compartida = 5

def thread_function2():

    global compartida
    compartida = 10


def thread_function():
    global compartida
    compartida = 7
    print("COM", compartida)
    print ("Thread %s: starting")



if __name__ == "__main__":
    #thread_function2()
    q = queue.Queue()
    x = threading.Thread(target=pr, args=(q,))
    
    x.start()
    print(q.get())
    x.join()
    exit(0)
