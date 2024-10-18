#include "scan.h"
#define KB "kb"
#define MB "mb"
#define GB "gb"

// Scan all memery to find RW memory --> systeminformer
//  Checker 

std::string GetProtectionString(DWORD protect) {
    std::string result;
    if (protect & PAGE_NOACCESS)
        result += "No Access ";
    if (protect & PAGE_READONLY)
        result += "R ";
    if (protect & PAGE_READWRITE)
        result += "RW ";
    if (protect & PAGE_WRITECOPY)
        result += "WC ";
    if (protect & PAGE_EXECUTE)
        result += "X ";
    if (protect & PAGE_EXECUTE_READ)
        result += "XR ";
    if (protect & PAGE_EXECUTE_READWRITE)
        result += "RWX ";
    if (protect & PAGE_EXECUTE_WRITECOPY)
        result += "XWC ";
    return result;
}

std::string GetNum(SIZE_T* num){
    int i = 0;
    while(*num/1024 > 0){
        i += 1;
        *num /= 1024;
    }
    if (i == 1){
        return KB;
    }else if (i == 2){
        return MB;
    }else{
        return GB;
    }
}

bool Write() {
    // WriteProcessMemory()
    return true;
}

bool Match() {
    return true;
}

bool Scan(HANDLE handle, LPVOID base) {
    MEMORY_BASIC_INFORMATION lpbuffer = MEMORY_BASIC_INFORMATION{}; 
    if (handle == NULL){
        std::cout<<"Open Process Error"<<std::endl;
        return false;
    }
    // std::cout<<"Open process successfully"<<std::endl;
    // std::cout<<"======================"<<std::endl;
    // while(VirtualQueryEx(handle,base,&lpbuffer,sizeof(lpbuffer)) == sizeof(MEMORY_BASIC_INFORMATION)){
    while(true){
        // Only focus on this case, why? balabala
        if (VirtualQueryEx(handle,base,&lpbuffer,sizeof(lpbuffer)) != 0){
            // std::cout<<lpbuffer.BaseAddress<<"|"<<lpbuffer.RegionSize/1000<<GetProtectionString(lpbuffer.Protect)<<std::endl;
            SIZE_T size = lpbuffer.RegionSize;
            std::string sizeStr = GetNum(&size);
            // printf("%#X|%10d%s|%20s\n",lpbuffer.BaseAddress,size,sizeStr.c_str(),GetProtectionString(lpbuffer.Protect).c_str());
            printf("%#x\n",lpbuffer.BaseAddress);
        }
        // if (GetLastError() != ERROR_SUCCESS) {
        //     std::cout << "Error occurred during memory scanning" << std::endl;
        //     CloseHandle(handle);
        //     return false;
        // }
        base = LPVOID((SIZE_T)base + lpbuffer.RegionSize);
    }
    return true;
}
