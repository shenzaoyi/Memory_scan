#include <windows.h>
#include <iostream>
#include <string>
#include <iomanip>
#include <memoryapi.h>
#include "scan.h"

int main(){
    int pid = -1;
    // std::cout<<"Please input the pid"<<std::endl;
    std::cin>>pid;
    // std::cout<<"pid is :"<<pid<<std::endl;
    // HANDLE handle = OpenProcess(PROCESS_ALL_ACCESS,FALSE,DWORD(pid));
    HANDLE handle = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ,FALSE,DWORD(pid));
    if (handle == NULL){
        std::cout<<"Open process error"<<std::endl;
    }
    if (!Scan(handle,0)){
        std::cout<<"Scan error"<<std::endl;
    }
    // CloseHandle(handle);
    TerminateProcess(handle,0);
    return 0;
}