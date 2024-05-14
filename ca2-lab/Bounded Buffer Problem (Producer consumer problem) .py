
import threading
import random
import time

# Buffer size
BUFFER_SIZE = 5

# Shared buffer
buffer = []
buffer_lock = threading.Lock()
empty_semaphore = threading.Semaphore(BUFFER_SIZE)
full_semaphore = threading.Semaphore(0)

# Event to signal threads to stop
stop_event = threading.Event()

def producer():
    global buffer
    while not stop_event.is_set():
        item = random.randint(1, 5)  # Produce an item
        empty_semaphore.acquire()  # Wait if buffer is full
        buffer_lock.acquire()  # Acquire lock
        buffer.append(item)  # Put the item into the buffer
        print(f"Produced: {item}, Buffer: {buffer}")
        buffer_lock.release()  # Release lock
        full_semaphore.release()  # Signal that buffer is not empty
        time.sleep(random.random())  # Simulate some time passing

def consumer():
    global buffer
    while not stop_event.is_set():
        full_semaphore.acquire()  # Wait if buffer is empty
        buffer_lock.acquire()  # Acquire lock
        item = buffer.pop(0)  # Consume an item from the buffer
        print(f"Consumed: {item}, Buffer: {buffer}")
        buffer_lock.release()  # Release lock
        empty_semaphore.release()  # Signal that buffer is not full
        time.sleep(random.random())  # Simulate some time passing

# Create producer and consumer threads
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

# Start the threads
producer_thread.start()
consumer_thread.start()

# Wait for 0.2 seconds
time.sleep(0.2)

# Set the event to stop the threads
stop_event.set()

# Join the threads
producer_thread.join()
consumer_thread.join()
