#include <iostream>
#include <unistd.h>

int main() {
    int a = 4;
    int pid = getpid();
    std::cout<<pid<<std::endl;
    // getchar();
    while(1) {
        std::cin>>a;
    }
    return 0;
}