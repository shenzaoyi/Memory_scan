#include <iostream>
#include <unistd.h>

int main() {
    int pid = getpid();
    std::cout<<pid<<std::endl;
    getchar();
    return 0;
}