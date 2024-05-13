import threading
import time
import random

database = {}  # Shared resource
read_count = 0
m = threading.Semaphore(1)  # Semaphore for mutual exclusion
w = threading.Semaphore(1)  # Semaphore for writer preference

def writer():
    while True:
        w.acquire()
        # Write operation
        print(f"Writer {threading.current_thread().name} is writing to database")
        database[threading.current_thread().name] = random.randint(1, 100)
        time.sleep(random.randint(1, 3))
        w.release()

def reader():
    global read_count  # declare read_count as global
    while True:
        m.acquire()
        read_count += 1
        if read_count == 1:
            w.acquire()
        m.release()

        # Read operation
        print(f"Reader {threading.current_thread().name} is reading database: {database}")
        time.sleep(random.randint(1, 3))

        m.acquire()
        read_count -= 1
        if read_count == 0:
            w.release()
        m.release()

if __name__ == "__main__":
    # Creating reader and writer threads
    threads = []
    for i in range(5):
        threads.append(threading.Thread(target=reader))
        threads.append(threading.Thread(target=writer))

    # Starting threads
    for thread in threads:
        thread.start()

    # Waiting for threads to complete
    for thread in threads:
        thread.join()

    print("All threads have finished execution")
