import ctypes as ct
from ctypes import wintypes as w

# func & prepare windows
PROCESS_ALL_ACCESS = 0x1F0FFF
SIZE_T = ct.c_size_t
dll = ct.WinDLL('kernel32', use_last_error=True)
ReadProcessMemory = ct.windll.kernel32.ReadProcessMemory
WriteProcessMemory = ct.windll.kernel32.WriteProcessMemory
VirtualQueryEx = dll.VirtualQueryEx
CreateBufferString = ct.create_string_buffer
CreateBufferInt = ct.c_int


def get_rwx(protect):
    protection_flags = {
        0x01: "PAGE_NOACCESS",        # 无访问权限
        0x02: "R--",                  # 只读
        0x04: "RW-",                  # 可读可写
        0x08: "R--X",                 # 可执行且可读
        0x10: "RWX",                  # 可读可写可执行
        0x20: "--X",                  # 仅可执行
        0x40: "COW",                  # 写时复制 (Copy-on-Write)
        0x80: "RW-C",                 # 可读写且为缓存
        0x100: "R--NC",               # 只读且不可缓存
    }
    if protect in protection_flags:
        return protection_flags[protect]
    else:
        return "Unknown"
    
def is_rw(protect): 
    protection_flags = {
        0x04: "RW-",                  # 可读可写
        0x10: "RWX",                  # 可读可写可执行
        0x40: "COW",                  # 写时复制 (Copy-on-Write)
        0x80: "RW-C",                 # 可读写且为缓存
    }
    if protect in protection_flags:
        return True
    else:
        return False
# https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-memory_basic_information
class MEMORY_BASIC_INFORMATION(ct.Structure):

    _fields_ = [("BaseAddress", w.LPVOID),
                ("AllocationBase", w.LPVOID),
                ("AllocationProtect", w.DWORD),
                ("PartitionId", w.WORD),
                ("RegionSize", SIZE_T),
                ("State", w.DWORD),
                ("Protect", w.DWORD),
                ("Type", w.DWORD)]

    def __repr__(self):
        return f'{self.BaseAddress if self.BaseAddress is not None else 0:#x}  ' \
        f'{get_rwx(self.Protect)}' \
        f'RegionSize={self.RegionSize:#x} \n' 
                    # f'{self.RegionSize/1024}'\
                                        # f'AllocationBase={self.AllocationBase if self.AllocationBase is not None else 0:#x}, ' \
                                        # f'AllocationProtect={self.AllocationProtect:#x}, ' \
                                        # f'PartitionId={self.PartitionId:#x}, ' \
                                        # f'RegionSize={self.RegionSize:#x}, ' \
                                        # f'State={self.State:#x}, ' \ 
                                        # f'Type={self.Type:#x})'

PMEMORY_BASIC_INFORMATION = ct.POINTER(MEMORY_BASIC_INFORMATION)

def get_handle(): 
    # https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualqueryex
    GetHandle = dll.OpenProcess
    GetHandle.argtypes = [w.DWORD, w.BOOL, w.DWORD]
    GetHandle.restype = w.HANDLE
    pid = input("Please input the pid: ")
    h = GetHandle(PROCESS_ALL_ACCESS,False,int(pid))
    return h

def scan(h): 
    VirtualQueryEx.argtypes = w.HANDLE, w.LPCVOID, PMEMORY_BASIC_INFORMATION, SIZE_T
    VirtualQueryEx.restype = SIZE_T
    address = 0
    mbi_list = []
    while True:
        mbi = MEMORY_BASIC_INFORMATION()
        result = VirtualQueryEx(h, address, ct.byref(mbi), ct.sizeof(mbi))
        if result:
            print(mbi)
            address += mbi.RegionSize
            mbi_list.append(mbi)
        else:
            print(f'err={ct.get_last_error()}')
            break
    return mbi_list

def filter(mbi_list): 
    result = []
    for item in mbi_list: 
        if (is_rw(item.Protect)):
            result.append(item)
    return result
def save_in_list(mbi_list,h):
    buffer_list = []
    for item in mbi_list:
        buffer = CreateBufferString(item.RegionSize)
        read_size = ct.c_size_t()
        ReadProcessMemory(h,ct.c_void_p(item.BaseAddress),buffer,ct.sizeof(buffer),ct.byref(read_size))
        if (read_size == read_size):
            buffer_list.append(buffer)
        else: 
            print("error" + str(ct.get_last_error()))
    return buffer_list

# 得到所有和给定值匹配的地址
def pattern_match(buffer_list, target_value,result):
    pattern = (target_value).to_bytes(4, byteorder='little')
    address_list = []
    for i in range(len(buffer_list)): 
        data = buffer_list[i].raw
        # index = data.find(pattern) find只能找第一个，垃圾Python, 毁我青春，断我前途
        start_index = 0  # 初始化搜索的起始位置
        while True:
            index = data.find(pattern, start_index)
            if index == -1:
                break  # 如果没有找到更多匹配项，退出循环
            address_list.append(result[i].BaseAddress + index)
            start_index = index + len(pattern)  # 更新起始位置，继续搜索下一个匹配项
    return address_list
        
def select(address_list, target, h):
    pattern = (target).to_bytes(4, byteorder='little')
    buffer = CreateBufferString(4)
    size = ct.c_size_t()
    filtered_list = []
    for item in address_list:
        if ReadProcessMemory(h, ct.c_void_p(item), buffer, ct.sizeof(buffer), size) != 0:
            if buffer.raw == pattern:
                filtered_list.append(item)
        else:
            print("error" + str(ct.get_last_error()))
    return filtered_list

def write_memory(h, address, value):
    buffer = CreateBufferString(4)
    buffer.raw = (value).to_bytes(4, byteorder='little')
    size = ct.c_size_t()
    WriteProcessMemory(h, ct.c_void_p(address), buffer, ct.sizeof(buffer), size)
    print(size.value)
    print(ct.sizeof(buffer))
    if size.value == ct.sizeof(buffer):
        print("write success")
    else:
        print("write failed" + str(ct.get_last_error()))

def main():
    init = input("Please input the init number: ") 
    h = get_handle()
    scan(h)
    result = filter(scan(h))
    buffer_list = save_in_list(result,h)
    matched_list = pattern_match(buffer_list, int(init),result)
    while True: 
        num = input("Please input the new value : ")
        if (num == "break"): 
            break
        matched_list = select(matched_list, int(num), h)
        print("remain: " + str(len(matched_list)))
        for item in matched_list:
            print(hex(item))
    for i in range (len(matched_list)): 
        print(str(i) + " : " + hex(matched_list[i]))
    choice = input("Please input the address you want to change: ")
    value = input("Please input the new value: ")
    write(h, matched_list[int(choice)], int(value))
main()
