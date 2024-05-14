import threading

# Shared resource
shared_resource = 0

# Mutex for writers
writer_mutex = threading.Semaphore(1)

# Mutex for readers
reader_mutex = threading.Semaphore(1)

# Variable to count readers
reader_count = 0

def writer():
    global shared_resource
    global writer_mutex

    writer_mutex.acquire()
    shared_resource += 1
    print(f"Writer writes: {shared_resource}")
    writer_mutex.release()

def reader():
    global reader_count
    global shared_resource
    global reader_mutex

    reader_mutex.acquire()
    reader_count += 1
    if reader_count == 1:
        writer_mutex.acquire()  # First reader acquires the writer lock
    reader_mutex.release()

    print(f"Reader reads: {shared_resource}")

    reader_mutex.acquire()
    reader_count -= 1
    if reader_count == 0:
        writer_mutex.release()  # Last reader releases the writer lock
    reader_mutex.release()

# Create some threads
threads = []
for _ in range(5):
    threads.append(threading.Thread(target=reader))
    threads.append(threading.Thread(target=writer))

# Start the threads
for thread in threads:
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()
