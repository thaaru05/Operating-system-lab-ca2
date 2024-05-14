import threading
import time
import random

class ReaderWriter:
    def __init__(self):
        self.resource = 0
        self.readers = 0
        self.lock = threading.Lock()
        self.stop_condition = threading.Event()  # Event to signal stop condition

    def read(self, reader_id):
        while not self.stop_condition.is_set():
            time.sleep(random.random())  # Simulate reading time
            with self.lock:
                self.readers += 1
                print(f"Reader {reader_id} is reading. Resource value: {self.resource}. Readers: {self.readers}")
                self.readers -= 1

    def write(self, writer_id):
        while not self.stop_condition.is_set():
            time.sleep(random.random())  # Simulate writing time
            with self.lock:
                self.resource += 1
                print(f"Writer {writer_id} is writing. Resource value: {self.resource}")

    def stop(self):
        self.stop_condition.set()

if __name__ == "__main__":
    rw = ReaderWriter()

    # Create reader threads
    reader_threads = []
    for i in range(3):
        t = threading.Thread(target=rw.read, args=(i,))
        reader_threads.append(t)
        t.start()

    # Create writer threads
    writer_threads = []
    for i in range(2):
        t = threading.Thread(target=rw.write, args=(i,))
        writer_threads.append(t)
        t.start()

    # Let the threads run for a while
    time.sleep(10)

    # Signal stop condition
    rw.stop()

    # Join all threads
    for t in reader_threads + writer_threads:
        t.join()

    print("Program stopped.")
