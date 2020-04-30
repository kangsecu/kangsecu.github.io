---
layout: post
title:  "Data Structure - sorting"
excerpt: "Try to know sorting & use it~_~"
date:   2019-08-08
categories: [C programming]
comments: true
---

bubble sorting

```c
#include <stdio.h>
#include <stdlib.h>
#define MAX_SIZE 10000
#define SWAP(x,y,t)((t)=(x),(x)=(y),(y)=(t))

	int i;
	int list[MAX_SIZE];
void buble_sort(int list[],int n){
    int cntA, cntB, temp;
	for(cntA = n-1;cntA >0; cntA--){
		for (cntB=0;cntB<cntA;cntB++){
			if(list[cntB]>list[cntB+1])
				SWAP(list[cntB],list[cntB+1],temp);
		}
	}
}

void main(){
	int i;
	int list[MAX_SIZE];
	int n =MAX_SIZE;
	for(i=0;i<n;i++)
	list[i]= rand()%n;
	buble_sort(list,n);
	for(int i=0;i<n;i++)
	printf("%d\n",list[i]);
	
}
```

selection sorting 

```c
#include <stdio.h>
#include <stdlib.h>
#define MAX_SIZE 10000
#define SWAP(x, y, t) ( (t)=(x), (x)=(y), (y)=(t) )

int list[MAX_SIZE];
int n;

void selection_sort(int list[],int n)
{
	int cnta,cntb,least,temp;
	for(cnta=0;cnta<n;cnta++){
		least = cnta;
		for(cntb=cnta+1; cntb<n;cntb++){
			if(list[cntb] < list[least]) least=cntb;
				 SWAP(list[cnta] , list[least],temp);
		}
	}
}
	int main()
	{
		int i;
		n = MAX_SIZE;
		for(i=0;i<n;i++)
			list[i]=rand() % n;
		selection_sort(list,n);
		for(int i=0;i<n;i++)
			printf("%d\n",list[i]);
	}
```

Insertion sorting

```c
#include <stdio.h> 
#include <stdlib.h>
#define MAX_SIZE 100000
#define SWAP(x,y,t)((t)=(x),(x)=(y),(y)=(t))
int list[MAX_SIZE];
int n;

void insertion_sort(int list[] , int n){
	int cntA,cntB,key;
	for(cntA =2;cntA <n;cntA++){
		key = list[cntA];
		for(cntB=cntA-1; cntB>=0 && list[cntB]>key;cntB--){
			list[cntB+1] = list[cntB];
		}
		list[cntB+1] = key; 
	}
}

void main(){
	int i;
	int n = MAX_SIZE;
	for(i=0; i<n;i++)
		list[i] = rand ()%n;
	
	insertion_sort(list,n);
	
	for(i=0;i<n;i++)
		printf("%d\n",list[i]);
}
```

Quick Sorting

```c
#include <stdio.h>

#define MAX_SIZE 100

int n = 9;
int list[MAX_SIZE] = {9, 8, 7, 6, 5, 4, 3, 2, 1};

#define SWAP(x, y, t) ((t)=(x), (x)=(y),(y)=(t))

void print(int list[], int n) {
    int i;
    for (i = 0; i < n; i++) {
        printf("%d ", list[i]);
    }
    printf("\n");
}

int partition(int list[], int left, int right) {
    int pivot, temp;
    int low, high;

    low = left;
    high = right + 1;

    pivot = list[left];

    do {
        do
            low++;
        while (low <= right && list[low] < pivot);
        do
            high--;
        while (high >= left && list[high] > pivot);

    if(low<high) SWAP(list[low],list[high],temp);
    } while (low < high);
    SWAP(list[left], list[high], temp);

    return high;
}

void quick_sort(int list[], int left, int right) {
    if (left < right) {
        int q = partition(list, left, right);
        print(list, 9);

        quick_sort(list, left, q - 1);
        quick_sort(list, q + 1, right);
    }
}

int main(int argc, const char *argv[]) {
    quick_sort(list, 0, 8);
    return 0;
}
```

