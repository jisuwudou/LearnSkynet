#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>
// ​
#define MAXLINE 128
#define SERV_PORT 9948
// ​
void* readthread(void* arg)
{
    pthread_detach(pthread_self());
    int sockfd = (int)arg;
    int n = 0;
    char buf[MAXLINE];
    while (1) 
    {
        n = read(sockfd, buf, MAXLINE);
        if (n == 0)
        {
            printf("the other side has been closed.\n");
            close(sockfd);
            exit(0);
        }
        else
            write(STDOUT_FILENO, buf, n);
    }   
    return (void*)0;
}
// ​
int main(int argc, char *argv[])
{
    struct sockaddr_in servaddr;
    int sockfd;
    char buf[MAXLINE];
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    inet_pton(AF_INET, "127.0.0.1", &servaddr.sin_addr);
    servaddr.sin_port = htons(SERV_PORT);
    connect(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr));
// ​
    pthread_t thid;
    pthread_create(&thid, NULL, readthread, (void*)sockfd);
// ​
    while (fgets(buf, MAXLINE, stdin) != NULL) 
        write(sockfd, buf, strlen(buf));
    close(sockfd);
    return 0;
}
// ————————————————
// 版权声明：本文为CSDN博主「吓人的猿」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
// 原文链接：https://blog.csdn.net/qq769651718/article/details/79434989