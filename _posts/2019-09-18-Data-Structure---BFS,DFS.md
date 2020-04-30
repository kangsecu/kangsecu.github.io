---
layout: post
title:  "Data Structure - BFS,DFS"
excerpt: "Try to know DFS, BFS & use it~_~"
date:   2019-09-18
categories: [C programming]
comments: true
---

BFS - 인접 리스트

```c
#include <stdio.h>
#include <stdlib.h>
#define TRUE 1
#define FALSE 0
#define MAX_VERTICES 50

typedef struct GraphNode
{
	int vertex;
	struct GraphNode *link;
} GraphNode;

typedef struct GraphType {
	int n;	// 정점의 개수
	GraphNode *adj_list[MAX_VERTICES];
} GraphType;

// 그래프 초기화 
void graph_init(GraphType *g)
{
	int v;
	g->n = 0;
	for (v = 0; v<MAX_VERTICES; v++)
		g->adj_list[v] = NULL;
}
// 정점 삽입 연산
void insert_vertex(GraphType *g, int v)
{
	if (((g->n) + 1) > MAX_VERTICES) {
		fprintf(stderr, "그래프: 정점의 개수 초과");
		return;
	}
	g->n++;
}
// 간선 삽입 연산, v를 u의 인접 리스트에 삽입한다.
void insert_edge(GraphType *g, int u, int v)
{
	GraphNode *node;
	if (u >= g->n || v >= g->n) {
		fprintf(stderr, "그래프: 정점 번호 오류");
		return;
	}
	node = (GraphNode *)malloc(sizeof(GraphNode));
	node->vertex = v;
	node->link = g->adj_list[u];
	g->adj_list[u] = node;
}
int visited[MAX_VERTICES];

#define MAX_QUEUE_SIZE 100
typedef int element;
typedef struct {
	element  queue[MAX_QUEUE_SIZE];
	int  front, rear;
} QueueType;
//
void error(char *message)
{
	fprintf(stderr, "%s\n", message);
	exit(1);
}
// 초기화 함수
void init(QueueType *q)
{
	q->front = q->rear = 0;
}
// 공백 상태 검출 함수
int is_empty(QueueType *q)
{
	return (q->front == q->rear);
}
// 포화 상태 검출 함수
int is_full(QueueType *q)
{
	return ((q->rear + 1) % MAX_QUEUE_SIZE == q->front);
}
// 삽입 함수
void enqueue(QueueType *q, element item)
{
	if (is_full(q))
		error("큐가 포화상태입니다");
	q->rear = (q->rear + 1) % MAX_QUEUE_SIZE;
	q->queue[q->rear] = item;
}
// 삭제 함수
element dequeue(QueueType *q)
{
	if (is_empty(q))
		error("큐가 공백상태입니다");
	q->front = (q->front + 1) % MAX_QUEUE_SIZE;
	return q->queue[q->front];
}
// 삭제 함수
element peek(QueueType *q)
{
	if (is_empty(q))
		error("큐가 공백상태입니다");
	return q->queue[(q->front + 1) % MAX_QUEUE_SIZE];
}
void bfs_list(GraphType *g, int v)
{
	GraphNode *w;
	QueueType q;
	init(&q);    				// 큐 초기 화 
	visited[v] = TRUE;      // 정점 v 방문 표시 
	printf("%d ", v);          // 방문한 정점 출력 
	enqueue(&q, v);			// 시작정점을 큐에 저장 
	while (!is_empty(&q)) {
		v = dequeue(&q);		// 큐에 저장된 정점 선택 
		for (w = g->adj_list[v]; w; w = w->link) //인접 정점 탐색
			if (!visited[w->vertex]) {	// 미방문 정점 탐색 
				visited[w->vertex] = TRUE;   // 방문 표시
				printf("%d ", w->vertex);
				enqueue(&q, w->vertex);	//정점을 큐에 삽입
			}
	}
}
//
main()
{
	int i;
	GraphType g;

	graph_init(&g);
	// 인접 리스트 생성 
	for (i = 0; i<4; i++)
		insert_vertex(&g, i);
	insert_edge(&g, 0, 1);
	insert_edge(&g, 1, 0);
	insert_edge(&g, 0, 3);
	insert_edge(&g, 3, 0);
	insert_edge(&g, 1, 2);
	insert_edge(&g, 2, 1);
	insert_edge(&g, 1, 3);
	insert_edge(&g, 3, 1);
	insert_edge(&g, 2, 3);
	insert_edge(&g, 3, 2);
	bfs_list(&g, 0);
}
```

 

DFS - 인접 리스트 

```c
#include <stdio.h>
#include <stdlib.h>
#define TRUE 1	
#define FALSE 0
#define MAX_VERTICES 50
#define MAX_QUEUE_SIZE 100 

int visited[MAX_VERTICES];

typedef struct GraphNode
{
	int vertex;
	struct GraphNode *link;
}GraphNode;

typedef struct GraphType
{
	int n;
	GraphNode *adj_list[MAX_VERTICES];
}GraphType;

void graph_init(GraphType *g){
	int v;
	g->n=0;
	for(v=0;v<MAX_VERTICES;v++)
		g->adj_list[v]= NULL;
}

void insert_vertex(GraphType *g, int v)
	{
	if (((g->n) + 1) > MAX_VERTICES) {
		fprintf(stderr, "그래프: 정점의 개수 초과");
		return;
		}
	g->n++;
	}
void insert_edge(GraphType *g, int u, int v)
	{
	GraphNode *node;
	if (u >= g->n || v >= g->n) {
		fprintf(stderr, "그래프: 정점 번호 오류");
		return;
	}
	node = (GraphNode *)malloc(sizeof(GraphNode));
	node->vertex = v;
	node->link = g->adj_list[u];
	g->adj_list[u] = node;
}
typedef int element;
typedef struct {
element  queue[MAX_QUEUE_SIZE];
	int  front, rear;
} QueueType;
void error(char *message)
{
	fprintf(stderr, "%s\n", message);
 exit(1);
}
void init(QueueType *q){
	q->front = q->rear = 0;
}
int is_empty(QueueType *q){
	return (q->front == q->rear);
}
int is_full(QueueType *q){
	return ((q->rear + 1) % MAX_QUEUE_SIZE == q->front);
}

void enqueue(QueueType *q, element item){
	if (is_full(q))
		error("큐가 포화상태입니다");
	q->rear = (q->rear + 1) % MAX_QUEUE_SIZE;
	q->queue[q->rear] = item;
}
element dequeue(QueueType *q){
	if (is_empty(q))
		error("큐가 공백상태입니다");
	q->front = (q->front + 1) % MAX_QUEUE_SIZE;
	return q->queue[q->front];
}
element peek(QueueType *q){
	if (is_empty(q))
		error("큐가 공백상태입니다");
	return q->queue[(q->front + 1) % MAX_QUEUE_SIZE];
}

void dfs_list(GraphType *g, int v){
	GraphNode *w;
	visited[v] = TRUE;   
	printf("%d ", v);   
for (w = g->adj_list[v]; w; w = w->link)// 인접 정점 탐색 
	if (!visited[w->vertex])
		dfs_list(g, w->vertex); //정점 w에서 DFS 새로시작
}

int main(){
	int i;
	GraphType g;
	graph_init(&g);
for (i = 0; i<4; i++)
  	insert_vertex(&g, i);
	insert_edge(&g, 0, 1);
	insert_edge(&g, 1, 0);
	insert_edge(&g, 0, 3);
	insert_edge(&g, 3, 0);
	insert_edge(&g, 1, 2);
	insert_edge(&g, 2, 1);
	insert_edge(&g, 1, 3);
	insert_edge(&g, 3, 1);
  insert_edge(&g, 2, 3);
	insert_edge(&g, 3, 2);
	dfs_list(&g, 0);
	        return 0;
}
```