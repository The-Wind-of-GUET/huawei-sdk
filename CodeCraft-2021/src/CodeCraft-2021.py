import sys
import numpy as np
from collections import defaultdict


server_info = dict()
def generate_server(server_type, cpu_cores, memory_size, server_cost, power_cost):
    """
    创建服务器
    """
    ab_cpu_cores = int(cpu_cores) / 2
    ab_memory_size = int(memory_size) / 2
    server_cpu_memory_A = np.array([ab_cpu_cores, ab_memory_size])
    server_cpu_memory_B = np.array([ab_cpu_cores, ab_memory_size])
    server_info[server_type] = {'cpu_cores': int(cpu_cores), 'memory_size': int(memory_size),
                                'server_cost': int(server_cost), 'power_cost': int(power_cost),
                                'server_cpu_memory_A': server_cpu_memory_A,
                                'server_cpu_memory_B': server_cpu_memory_B,
                                'cpu_per_hc': float(server_cost) / float(cpu_cores),
                                'cpu_per_rc': float(power_cost) / float(cpu_cores),
                                'mem_per_hc': float(server_cost) / float(memory_size),
                                'mem_per_rc': float(power_cost) / float(memory_size)
                                }

vm_info = dict()


def generate_vm(vm_type, vm_cpu_cores, vm_memory_size, single_or_double):
    """
    创建虚拟机
    """
    vm_info[vm_type] = {'vm_cpu_cores': int(vm_cpu_cores), 'vm_memory_size': int(vm_memory_size),
                        'single_or_double': int(single_or_double)}


op_list = defaultdict(list)


def operation_read(day, op, **kwargs):
    """
    将操作添加到请求列表
    """
    vm_type = kwargs.get('vm_type')
    vm_id = kwargs['vm_id']
    if vm_type:
        op_list[day + 1].append([op, vm_type.strip(), int(vm_id)])
    else:
        op_list[day + 1].append([op, int(vm_id)])


survival_vm = dict()


def add_vm_operation(vm_type, vm_id):
    """
    增加虚拟机操作
    """
    survival_vm[int(vm_id)] = vm_type


def del_vm_operation(vm_id):
    """
    删除虚拟机操作
    """
    survival_vm.pop(int(vm_id))


need_cpu = need_memory = 0


def calculate_capacity(day, op_list, vm_info, survival_vm):
    global need_cpu, need_memory

    yesterday_req = op_list[day]
    for req in yesterday_req:
        if req[0] == 'add':
            add_vm_operation(req[1], req[2])
            need_cpu += vm_info[req[1]]['vm_cpu_cores']
            need_memory += vm_info[req[1]]['vm_memory_size']
        elif req[0] == 'del':
            need_cpu -= vm_info[survival_vm[req[1]]]['vm_cpu_cores']
            need_memory -= vm_info[survival_vm[req[1]]]['vm_memory_size']
            del_vm_operation(req[1])
    return need_cpu, need_memory


def performance(server_info):
    s_cpu_per_hc_list = sorted(server_info.items(), key=lambda s: s[1]['cpu_per_hc'])
    s_cpu_per_rc_list = sorted(server_info.items(), key=lambda s: s[1]['cpu_per_rc'])
    s_mem_per_hc_list = sorted(server_info.items(), key=lambda s: s[1]['mem_per_hc'])
    s_mem_per_rc_list = sorted(server_info.items(), key=lambda s: s[1]['mem_per_rc'])
    return s_cpu_per_hc_list, s_cpu_per_rc_list, s_mem_per_hc_list, s_mem_per_rc_list


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
        need_cpu, need_memory = calculate_capacity(day + 1, op_list, vm_info, survival_vm)
        # print('-day %d, -need_cpu: %d, -need_mem: %d'% (day+1, need_cpu, need_memory))
    s_cpu_per_hc_list, s_cpu_per_rc_list, s_mem_per_hc_list, s_mem_per_rc_list = performance(server_info)
    # to write standard output
    # sys.stdout.flush()
    f.close()
    print('hello')
    print('world')



if __name__ == "__main__":
    main()
