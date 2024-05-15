#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<pthread.h>
#include<semaphore.h>
#define num_phil 5

sem_t forks[num_phil];

void think(int p_id){
printf("phil %d is thinking \n", p_id);
sleep(1);
}

void eat(int p_id){
printf("phil %d is eating \n", p_id);
sleep(1);
}

void pick_fork(int p_id){
sem_wait(&forks[p_id]);
sem_wait(&forks[(p_id+1)%num_phil]);
}

void putdown_fork(int p_id){
sem_post(&forks[p_id]);
sem_post(&forks[(p_id+1)%num_phil]);
}

void *phil(void *arg){
int p_id=*(int*)arg;
while(1){
think(p_id);
pick_fork(p_id);
eat(p_id);
putdown_fork(p_id);
}
return NULL;
}

int main(){
int i;
pthread_t philosophers[num_phil];
int ids[num_phil];

for(i=0;i<num_phil;i++){
sem_init(&forks[i],0,1);
}

for(i=0;i<num_phil;i++){
ids[i]=i;
pthread_create(&philosophers[i],NULL,phil,&ids[i]);
}

for(i=0;i<num_phil;i++){
pthread_join(philosophers[i],NULL);
}

for(i=0;i<num_phil;i++){
sem_destroy(&forks[i]);
}
return 0;
}