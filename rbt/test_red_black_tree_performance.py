import cProfile
import pstats
import random
import io
import matplotlib.pyplot as plt
import numpy as np
from pstats import SortKey
from pympler import tracker, asizeof
from scipy.optimize import curve_fit
#from sortedcontainers import SortedDict
from rbt.red_black_tree import RedBlackTree

def profile_rbt_insert(size):
    rbt = RedBlackTree()
    #rbt = SortedDict()
    data = random.sample(range(1, size * 10), size)
    
    pr = cProfile.Profile()
    pr.enable()
    
    for num in random.sample(data, size):
        rbt.insert(num)
        #rbt[num] = num
    
    pr.disable()
    
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats(SortKey.CUMULATIVE)
    ps.print_stats()
    
    stats_str = s.getvalue()
    time_line = [line for line in stats_str.split('\n') if 'function calls' in line][0]
    total_time = float(time_line.split('in')[1].split('seconds')[0].strip())
    
    return total_time

def profile_rbt_find(size):
    rbt = RedBlackTree()
    #rbt = SortedDict()
    data = random.sample(range(1, size * 10), size)

    sample = random.sample(data, size)

    for num in sample:
        rbt.insert(num)
    
    pr = cProfile.Profile()
    pr.enable()
    
    for num in sample:
        rbt.find(num)
    
    pr.disable()
    
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats(SortKey.CUMULATIVE)
    ps.print_stats()
    
    stats_str = s.getvalue()
    time_line = [line for line in stats_str.split('\n') if 'function calls' in line][0]
    total_time = float(time_line.split('in')[1].split('seconds')[0].strip())
    
    return total_time

def linear_func(x, a, b):
    return a * np.array(x) + b

def nlogn_func(x, a, b):
    return a * np.array(x) * np.log(np.array(x)) + b

def logn_func(x, a, b):
    return a * np.log(np.array(x)) + b

def test_insert_time():
    sizes = [2560, 5120, 10240, 20480, 40960, 81280]
    #sizes = [256000, 512000, 1024000, 2048000, 4096000, 8128000]
    times = []

    for size in sizes:
        print(f"Testing with size {size}")
        time_taken = profile_rbt_insert(size)
        times.append(time_taken)
        print(f"Time taken: {time_taken:.6f} seconds")

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times, 'o-', label='Measured time')
    plt.xlabel('Input Size (n)')
    plt.ylabel('Time (seconds)')
    plt.title('Red-Black Tree Insertion Time Complexity')
    plt.grid(True)

    params_linear, _ = curve_fit(linear_func, sizes, times)
    params_nlogn, _ = curve_fit(nlogn_func, sizes, times)
    
    x_fit = np.linspace(min(sizes), max(sizes), 100)
    y_linear = linear_func(x_fit, *params_linear)
    y_nlogn = nlogn_func(x_fit, *params_nlogn)
    
    plt.plot(x_fit, y_linear, '--', label=f'O(n)')
    plt.plot(x_fit, y_nlogn, ':', label=f'O(n log n)')        

    plt.legend()
    plt.savefig('rbt_insert_time_complexity.png')
    plt.show()

    print("Analysis complete! Check 'rbt_insert_time_complexity.png' for the visualization.")


def test_find_time():
    #sizes = [25600, 51200, 102400, 204800, 409600, 812800]
    sizes = [256000, 512000, 1024000, 2048000]
    times = []

    for size in sizes:
        print(f"Testing with size {size}")
        time_taken = profile_rbt_find(size)
        times.append(time_taken)
        print(f"Time taken: {time_taken:.6f} seconds")

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times, 'o-', label='Measured time')
    plt.xlabel('Input Size (n)')
    plt.ylabel('Time (seconds)')
    plt.title('Red-Black Tree Find Time Complexity')
    plt.grid(True)

    params_linear, _ = curve_fit(linear_func, sizes, times)
    params_logn, _ = curve_fit(logn_func, sizes, times)
    
    x_fit = np.linspace(min(sizes), max(sizes), 100)
    y_linear = linear_func(x_fit, *params_linear)
    y_logn = logn_func(x_fit, *params_logn)
    
    plt.plot(x_fit, y_linear, '--', label=f'O(n)')
    plt.plot(x_fit, y_logn, ':', label=f'O(log n)')        

    plt.legend()
    plt.savefig('rbt_find_time_complexity.png')
    plt.show()

    print("Analysis complete! Check 'rbt_find_time_complexity.png' for the visualization.")
    

#test_time()
#test_memory()
