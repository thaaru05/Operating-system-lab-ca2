#include<stdio.h>
int main(){
int n,m,i,j,k;
printf("enter processors:");
scanf("%d",&n);
printf("enter resources:");
scanf("%d",&m);

int alloc[n][m],max[n][m],avail[m];

printf("enter alloc matrix:\n");
for(i=0;i<n;i++){
printf("for process P%d:",i);
for(j=0;j<m;j++){
scanf("%d",&alloc[i][j]);
}
}

printf("enter max matrix:\n");
for(i=0;i<n;i++){
printf("for process P%d:",i);
for(j=0;j<m;j++){
scanf("%d",&max[i][j]);
}
}

printf("enter avail resources:\n");
for(j=0;j<m;j++){
scanf("%d",&avail[j]);
}

int f[n],ans[n],ind=0;
for(k=0;k<n;k++){
f[k]=0;
}

int need[n][m];
for(i=0;i<n;i++){
for(j=0;j<m;j++){
need[i][j]=max[i][j]-alloc[i][j];
}
}

int y=0;
for(k=0;k<n;k++){
for(i=0;i<n;i++){
if(f[i]==0){
int flag=0;
for(j=0;j<m;j++){
if(need[i][j]>avail[j]){
flag=1;
break;
}
}

if(flag==0){
ans[ind++]=i;
for(y=0;y<m;y++){
avail[y]+=alloc[i][y];
}
f[i]=1;
}
}
}
}
int flag=1;
for(i=0;i<n;i++){
if(f[i]==0){
flag=0;
printf("not safe");
break;
}
}
if(flag==1){
printf("safe sequenceis:\n");
for(i=0;i<n-1;i++){
printf("P%d-->",ans[i]);
}
printf("P%d",ans[n-1]);
}
}