import threading
import time
import random

MAX_BUFFER_SIZE = 5  # Maximum size of the buffer
buffer = []  # Shared buffer
mutex = threading.Semaphore(1)  # Semaphore for mutual exclusion
empty = threading.Semaphore(MAX_BUFFER_SIZE)  # Semaphore to track empty slots
full = threading.Semaphore(0)  # Semaphore to track filled slots

def producer():
    while True:
        empty.acquire()  # wait until there is an empty slot
        mutex.acquire()  # acquire the lock
        item = random.randint(1, 100)  # produce an item
        buffer.append(item)  # insert the item into the buffer
        print(f"Producer produced item {item}, Buffer: {buffer}")
        mutex.release()  # release the lock
        full.release()  # increment 'full'

def consumer():
    while True:
        full.acquire()  # wait until there is a filled slot
        mutex.acquire()  # acquire the lock
        item = buffer.pop(0)  # remove an item from the buffer
        print(f"Consumer consumed item {item}, Buffer: {buffer}")
        mutex.release()  # release the lock
        empty.release()  # increment 'empty'

if __name__ == "__main__":
    # Creating producer and consumer threads
    threads = []
    threads.append(threading.Thread(target=producer))
    threads.append(threading.Thread(target=consumer))

    # Starting threads
    for thread in threads:
        thread.start()

    # Waiting for threads to complete
    for thread in threads:
        thread.join()

    print("All threads have finished execution")
