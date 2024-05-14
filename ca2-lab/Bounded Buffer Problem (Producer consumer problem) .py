import threading
import time
import random

MAX_BUFFER_SIZE = 5  # Maximum size of the buffer
buffer = []  # Shared buffer
mutex = threading.Semaphore(1)  # Semaphore for mutual exclusion
empty = threading.Semaphore(MAX_BUFFER_SIZE)  # Semaphore to track empty slots
full = threading.Semaphore(0)  # Semaphore to track filled slots
stop_event = threading.Event()  # Event to signal stop condition

def producer():
    while not stop_event.is_set():
        empty.acquire()  # wait until there is an empty slot
        mutex.acquire()  # acquire the lock
        if stop_event.is_set():
            mutex.release()  # release the lock if stop event is set
            break
        item = random.randint(1, 100)  # produce an item
        buffer.append(item)  # insert the item into the buffer
        print(f"Producer produced item {item}, Buffer: {buffer}")
        mutex.release()  # release the lock
        full.release()  # increment 'full'

def consumer():
    while not stop_event.is_set() or buffer:
        full.acquire()  # wait until there is a filled slot
        mutex.acquire()  # acquire the lock
        if buffer:
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

    # Let the program run for a while
    time.sleep(10)

    # Set stop event
    stop_event.set()

    # Waiting for threads to complete
    for thread in threads:
        thread.join()

    print("All threads have finished execution")

