import re
import time
from hyperloglog import HyperLogLog

def load_ip_addresses(file_path):
    ip_addresses = set() 
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', line)
            if match:
                ip_addresses.add(match.group(0)) 
    return ip_addresses

def count_unique_ips_exact(ip_addresses):
    return len(ip_addresses)

def count_unique_ips_hyperloglog(file_path, error_rate=0.01):
    hll = HyperLogLog(error_rate)
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', line)
            if match:
                hll.add(match.group(0)) 
    return len(hll)

def compare_methods(file_path):

    start_time = time.time()
    ip_addresses = load_ip_addresses(file_path)
    exact_count = count_unique_ips_exact(ip_addresses)
    exact_time = time.time() - start_time

    start_time = time.time()
    hll_count = count_unique_ips_hyperloglog(file_path)
    hll_time = time.time() - start_time

    print(f"Результати порівняння:")
    print(f"                       Точний підрахунок   HyperLogLog")
    print(f"Унікальні елементи              {exact_count}      {hll_count}")
    print(f"Час виконання (сек.)                {exact_time:.2f}          {hll_time:.2f}")

if __name__ == "__main__":
    file_path = 'lms-stage-access.log' 
    compare_methods(file_path)