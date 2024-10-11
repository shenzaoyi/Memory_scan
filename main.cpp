#include <windows.h>
#include <iostream>
#include <string>
#include <iomanip>
#include <memoryapi.h>
#include "scan.h"

int main(){
    int pid = -1;
    std::cout<<"Please input the pid"<<std::endl;
    std::cin>>pid;
    std::cout<<"pid is :"<<pid<<std::endl;
    HANDLE handle = OpenProcess(PROCESS_ALL_ACCESS,FALSE,DWORD(pid));
    if (handle == NULL){
        std::cout<<"Open process error"<<std::endl;
    }
    if (!Scan(handle,0)){
        std::cout<<"Scan error"<<std::endl;
    }
    return 0;
    // read memory layout
    // LPSYSTEM_INFO SystemINfo;
    // GetSystemInfo(SystemINfo);
    // PMEMORY_BASIC_INFORMATION MemoryInfo;
    // SIZE_T memorySize = sizeof(MemoryInfo);
    // if (VirtualQueryEx(handle,NULL,MemoryInfo,memorySize) == 0){
    //     std::cout<<"VirtualQueryEX query error"<<std::endl;
    // }

    // // ReadProcessMemory 
    // SIZE_T size = 1024 * 1024;
    // LPVOID* buffer = new LPVOID[size];
    // SIZE_T* num = new SIZE_T;
    // //if  (!ReadProcessMemory(handle,(LPCVOID)0x7FF66BED7000,buffer,size,num)){
    // //    std::cout<<"ReadMemoryError"<<std::endl;
    // //}
    // if  (!ReadProcessMemory(handle,NULL,buffer,size,num)){
    //     std::cout<<"ReadMemoryError"<<std::endl;
    //     std::cout<<GetLastError()<<std::endl;
    // }
    // if (*num <= 0){
    //     std::cout<<"Read Nothing"<<std::endl;
    // }
    // // 以十六进制格式输出 buffer 中的内容
    // for (SIZE_T i = 0; i < *num; ++i) {
    //     std::cout << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(reinterpret_cast<BYTE*>(buffer)[i]) << " ";
    // }
    // std::cout << std::endl;

    // delete[] reinterpret_cast<BYTE*>(buffer); // 释放 buffer
    // system("pause");
    // return 0;
}