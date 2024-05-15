#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<pthread.h>
#include<semaphore.h>
#define num_chairs 3

sem_t mutex;
sem_t customer;
sem_t barber;

int num_cus_wai=0;

void *barber_(void *arg){
while(1){
sem_wait(&customer);
sem_wait(&mutex);
num_cus_wai--;
sem_post(&mutex);
sem_post(&barber);
printf("barber cutting hair\n");
sleep(3);
printf("barber completed cutting\n");
}
}

void *customer_(void *arg){
while(1){
sem_wait(&mutex);
if(num_cus_wai<num_chairs){
num_cus_wai++;
printf("customer entered shop\n");
sem_post(&customer);
sem_post(&mutex);
sem_wait(&barber);
}
else{
printf("customer left\n");
sem_post(&mutex);
sleep(3);
}
}
}


int main(){
pthread_t barber_thread,customer_thread;
sem_init(&mutex,0,1);
sem_init(&barber,0,0);
sem_init(&customer,0,0);
pthread_create(&barber_thread,NULL,barber_,NULL);
pthread_create(&customer_thread,NULL,customer_,NULL);
pthread_join(barber_thread,NULL);
pthread_join(customer_thread,NULL);
sem_destroy(&mutex);
sem_destroy(&barber);
sem_destroy(&customer);
return 0;
}