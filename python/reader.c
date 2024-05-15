#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<pthread.h>
#include<semaphore.h>
#define WRITERS_COUNT 2
#define READERS_COUNT 3

sem_t r_mutex;
sem_t w_mutex;
int r_count=0;

void *reader(void *arg){
int r_id=*((int*)arg);
while(1){
sem_wait(&r_mutex);
r_count++;
if(r_count==1){
sem_wait(&w_mutex);
}
sem_post(&r_mutex);
printf("reader %d reading\n",r_id);
sleep(1);

sem_wait(&r_mutex);
r_count--;
if(r_count==0){
sem_post(&w_mutex);
}
sem_post(&r_mutex);
sleep(2);
}
pthread_exit(NULL);
}

void *writer(void *arg){
int w_id=*((int*)arg);
while(1){
printf("writer %d writing\n",w_id);
sleep(1);
sleep(2);
}
pthread_exit(NULL);
}
 int main(){
 int i;
 pthread_t readers[READERS_COUNT],writers[WRITERS_COUNT];
 int r_ids[READERS_COUNT],w_ids[WRITERS_COUNT];
 sem_init(&r_mutex,0,1);
 sem_init(&w_mutex,0,1);
 
 for(i=0;i<READERS_COUNT;i++){
 r_ids[i]=i+1;
 pthread_create(&readers[i],NULL,reader,&r_ids[i]);
 }
 
 for(i=0;i<WRITERS_COUNT;i++){
 w_ids[i]=i+1;
 pthread_create(&writers[i],NULL,writer,&r_ids[i]);
 }
 
for(i=0;i<READERS_COUNT;i++){
 pthread_join(readers[i],NULL);
}
 
for(i=0;i<WRITERS_COUNT;i++){
pthread_join(writers[i],NULL);
}
 
sem_destroy(&r_mutex);
sem_destroy(&w_mutex);
return 0;
 }