import threading
import time
import random

NUM_PHILOSOPHERS = 5
sticks = [threading.Semaphore(1) for _ in range(NUM_PHILOSOPHERS)]  # Semaphores for each chopstick
stop_event = threading.Event()  # Event to signal stop condition

def philosopher(i):
    while not stop_event.is_set():
        sticks[i].acquire()  # pick up left chopstick
        sticks[(i + 1) % NUM_PHILOSOPHERS].acquire()  # pick up right chopstick
        if not stop_event.is_set():
            print(f"Philosopher {i} is eating")
            time.sleep(random.random() * 2)  # eating time
        sticks[i].release()  # put down left chopstick
        sticks[(i + 1) % NUM_PHILOSOPHERS].release()  # put down right chopstick
        if not stop_event.is_set():
            print(f"Philosopher {i} is thinking")
            time.sleep(random.random() * 2)  # thinking time

if __name__ == "__main__":
    # Creating philosopher threads
    philosophers = [threading.Thread(target=philosopher, args=(i,)) for i in range(NUM_PHILOSOPHERS)]

    # Starting threads
    for philosopher_thread in philosophers:
        philosopher_thread.start()

    # Let the program run for a while
    time.sleep(10)

    # Set stop event
    stop_event.set()

    # Waiting for threads to complete
    for philosopher_thread in philosophers:
        philosopher_thread.join()

    print("All philosophers have finished dining")

