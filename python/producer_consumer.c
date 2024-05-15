
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

#define BUFFER_SIZE 2

int buffer[BUFFER_SIZE];
int in = 0, out = 0;
int count = 0; // Number of items in the buffer
int mutex = 1; // Binary semaphore for mutual exclusion

// Custom wait function
void wait(int *s) {
    while (*s <= 0);
    (*s)--;
}

// Custom signal function
void signal(int *s) {
    (*s)++;
}

// Producer function
void *producer(void *arg) {
    int value;
    while (1) {
        printf("Enter a value to produce: ");
        scanf("%d", &value);
        wait(&mutex); // Lock shared resources
        if (count < BUFFER_SIZE) {
            buffer[in] = value;
            printf("Producer produced: %d\n", value);
            in = (in + 1) % BUFFER_SIZE;
            count++;
        } else {
            printf("Buffer is full. Producer waits...\n");
        }
        signal(&mutex); // Unlock shared resources
        sleep(1); // Simulate work
    }
}

// Consumer function
void *consumer(void *arg) {
    while (1) {
        wait(&mutex); // Lock shared resources
        if (count > 0) {
            int value = buffer[out];
            printf("\nConsumer consumed: %d\n", value);
            out = (out + 1) % BUFFER_SIZE;
            count--;
        } else {
            printf("\nBuffer is empty. Consumer waits...\n");
        }
        signal(&mutex); // Unlock shared resources
        sleep(3); // Simulate work
    }
}

int main() {
    pthread_t producer_thread, consumer_thread;
    pthread_create(&producer_thread, NULL, producer, NULL);
    pthread_create(&consumer_thread, NULL, consumer, NULL);
    pthread_join(producer_thread, NULL);
    pthread_join(consumer_thread, NULL);
    return 0;
}