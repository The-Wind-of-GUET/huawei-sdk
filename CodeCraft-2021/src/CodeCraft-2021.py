import sys
import numpy as np
from collections import defaultdict


SERVER_INFO = dict()  # 服务器信息字典 {服务器名:{CPU核数: ,内存大小: ,硬件成本: ,运行成本: ,综合性价比: }}
A_CPU = 0.15 # 硬件性价比系数
A_MEM = 0.15 # 硬件性价比系数
B_CPU = 0.35 # 运行性价比系数
B_MEM = 0.35 # 运行性价比系数
def generate_server(server_type: str, cpu_cores: str, memory_size: str, server_cost: str, power_cost: str):
    """
    创建服务器信息
    :param server_type: 服务器种类名
    :param cpu_cores: 服务器CPU核数
    :param memory_size: 服务器MEMORY大小
    :param server_cost: 服务器硬件成本
    :param power_cost: 服务器运行成本
    :return: 无
    """
    global SERVER_INFO
    ab_cpu_cores = int(cpu_cores) / 2
    ab_memory_size = int(memory_size) / 2
    server_cpu_memory_a = np.array([ab_cpu_cores, ab_memory_size])
    server_cpu_memory_b = np.array([ab_cpu_cores, ab_memory_size])
    cpu_per_hc = float(server_cost) / float(cpu_cores)  # cpu硬件性价比
    cpu_per_rc = float(power_cost) / float(cpu_cores)   # cpu运行性价比
    mem_per_hc = float(server_cost) / float(memory_size)    # memory硬件性价比
    mem_per_rc = float(power_cost) / float(memory_size)     # memory运行性价比
    com_per = A_CPU * cpu_per_hc + B_CPU * cpu_per_rc + A_MEM * mem_per_hc + B_MEM * mem_per_rc # 综合性价比
    SERVER_INFO[server_type] = {'cpu_cores': int(cpu_cores), 'memory_size': int(memory_size),
                                'server_cost': int(server_cost), 'power_cost': int(power_cost),
                                'server_cpu_memory_a': server_cpu_memory_a,
                                'server_cpu_memory_b': server_cpu_memory_b,
                                'com_per': com_per
                                }


VM_INFO = dict()    # 虚拟机信息字典{虚拟机名:{核数: ,内存大小: ,单/双节点: }}
def generate_vm(vm_type: str, vm_cpu_cores: str, vm_memory_size: str, single_or_double: str):
    """
    创建虚拟机信息
    :param vm_type: 虚拟机种类名
    :param vm_cpu_cores: 虚拟机CPU核数
    :param vm_memory_size: 虚拟机MEMORY大小
    :param single_or_double: 单节点还是双节点
    :return: 无
    """
    global VM_INFO
    VM_INFO[vm_type] = {'vm_cpu_cores': int(vm_cpu_cores), 'vm_memory_size': int(vm_memory_size),
                        'single_or_double': int(single_or_double)}


OP_LIST = defaultdict(list)  # 每天的操作字典 {day:[每天的操作]}
def operation_read(day: int, op: str, **kwargs):
    """
    将操作添加到请求列表
    :param day: 第day天
    :param op: 操作指令 'add' or 'del'
    :param kwargs: 接受关键字参数，'vm_type'
    :return: 无
    """
    global OP_LIST
    vm_type = kwargs.get('vm_type')  # 不是add操作则没有vm_type
    vm_id = kwargs['vm_id']
    if vm_type:
        OP_LIST[day + 1].append([op, vm_type.strip(), int(vm_id)])
    else:
        OP_LIST[day + 1].append([op, int(vm_id)])


SURVIVAL_VM = dict()  # 存活虚拟机字典{虚拟机ID:虚拟机种类}
def add_vm_operation(vm_type: str, vm_id: int):
    """
    增加虚拟机操作
    :param vm_type: 虚拟机种类名
    :param vm_id: 虚拟机ID
    :return: 无
    """
    SURVIVAL_VM[int(vm_id)] = vm_type


def del_vm_operation(vm_id):
    """
    删除虚拟机操作
    :param vm_id: 虚拟机ID
    :return: 无
    """
    SURVIVAL_VM.pop(int(vm_id))


need_cpu = need_memory = 0  # 每天请求需要的CPU和内存数
def calculate_capacity(day: int, OP_LIST: dict, VM_INFO: dict, SURVIVAL_VM: dict) -> (int,int):
    global need_cpu, need_memory
    yesterday_req = OP_LIST[day]
    for req in yesterday_req:
        if req[0] == 'add':
            add_vm_operation(req[1], req[2])
            need_cpu += VM_INFO[req[1]]['vm_cpu_cores']
            need_memory += VM_INFO[req[1]]['vm_memory_size']
        elif req[0] == 'del':
            need_cpu -= VM_INFO[SURVIVAL_VM[req[1]]]['vm_cpu_cores']
            need_memory -= VM_INFO[SURVIVAL_VM[req[1]]]['vm_memory_size']
            del_vm_operation(req[1])
    return need_cpu, need_memory


def sort_performance(SERVER_INFO:dict) -> list:
    """
    根据综合性价比排序
    :param SERVER_INFO: 服务器信息字典
    :return: com_per_list排好的列表
    """
    com_per_list = sorted(SERVER_INFO.items(), key=lambda s: s[1]['com_per'])
    return com_per_list


def expansion():
    pass


def migration():
    pass


def main():
    # to read standard input
    f = open('training-1.txt', 'r')
    sys.stdin = f
    server_num = sys.stdin.readline()[:-1]  # ("-采购服务器类型的数量:")
    for i in range(int(server_num)):
        server_temp = sys.stdin.readline()[:-1]  # ("-输入(型号, CPU 核数, 内存大小, 硬件成本, 每日能耗成本)：")
        server_type, cpu_cores, memory_size, server_cost, power_cost = server_temp[1:-1].split(',')
        generate_server(server_type, cpu_cores, memory_size, server_cost, power_cost)

    vm_num = sys.stdin.readline()[:-1]  # ("-售卖的虚拟机类型数量:")
    for i in range(int(vm_num)):
        vm_temp = sys.stdin.readline()[:-1]  # ("-输入(型号, CPU 核数, 内存大小, 是否双节点部署)：")
        vm_type, vm_cpu_cores, vm_memory_size, single_or_double = vm_temp[1:-1].split(',')
        generate_vm(vm_type, vm_cpu_cores, vm_memory_size, single_or_double)

    request_days = sys.stdin.readline()[:-1]  # ("-T天的用户请求：")
    for day in range(int(request_days)):
        request_num = sys.stdin.readline()[:-1]  # ("-R条请求：")
        for j in range(int(request_num)):
            request_content = sys.stdin.readline()[:-1]  # ("-请求内容(add, 虚拟机型号, 虚拟机 ID)或(del, 虚拟机 ID)：")
            if request_content[1] == 'a':
                add_op, vm_type, vm_id = request_content[1:-1].split(',')
                operation_read(day, add_op, vm_type=vm_type, vm_id=int(vm_id))
            else:
                del_op, vm_id = request_content[1:-1].split(',')
                operation_read(day, del_op, vm_id=int(vm_id))

    # process
    for day in range(int(request_days)):
        need_cpu, need_memory = calculate_capacity(day + 1, OP_LIST, VM_INFO, SURVIVAL_VM)
        # print('-day %d, -need_cpu: %d, -need_mem: %d'% (day+1, need_cpu, need_memory))
    com_per_list = sort_performance(SERVER_INFO)
    # to write standard output
    # sys.stdout.flush()
    f.close()
    print('hello')
    print('world')



if __name__ == "__main__":
    main()
