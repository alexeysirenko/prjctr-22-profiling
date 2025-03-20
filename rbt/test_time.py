import cProfile
import pstats
import random
import io
import matplotlib.pyplot as plt
from pstats import SortKey

from rbt.red_black_tree import RedBlackTree

def create_tree(nums):
    rbt = RedBlackTree()

    for num in nums:
        rbt.insert(num)

    return rbt

def get_profile_time(pr):
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats(SortKey.CUMULATIVE)
    ps.print_stats()
    
    stats_str = s.getvalue()
    print(stats_str)
    time_line = [line for line in stats_str.split('\n') if 'function calls' in line][0]
    total_time = float(time_line.split('in')[1].split('seconds')[0].strip())

    return total_time


def profile_rbt_insert(size):
    data = random.sample(range(1, size * 10), size)
    sample = random.sample(data, size)

    rbt = create_tree(sample)

    #times = []
    n_tests = 1000
    pr = cProfile.Profile()
    pr.enable()
    for _ in range(0, n_tests):
        rbt.insert(random.randint(1, size * 10))
    pr.disable()
    #times.append(get_profile_time(pr))
    
    return get_profile_time(pr) / n_tests

def profile_rbt_find(size):
    data = random.sample(range(1, size * 10), size)
    sample = random.sample(data, size)

    rbt = create_tree(sample)
    n_tests = 1000
    # rbt.find(random.choice(sample))
    # rbt.find(random.randint(1, size * 10))
    times = []
    pr = cProfile.Profile()
    pr.enable()
    for _ in range(0, n_tests):
        rbt.find(random.choice(sample))
    pr.disable()
    times.append(get_profile_time(pr) / n_tests)

    pr = cProfile.Profile()
    pr.enable()
    for _ in range(0, n_tests):
        rbt.find(random.randint(1, size * 10))
    pr.disable()
    times.append(get_profile_time(pr) / n_tests)

    return sum(times) / len(times)

def test_insert_time():
    sizes = [100000 * i for i in range(1, 10)]
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

    plt.legend()
    plt.savefig('rbt_insert_time_complexity.png')
    plt.show()

    print("Analysis complete! Check 'rbt_insert_time_complexity.png' for the visualization.")


def test_find_time():
    sizes = [100000 * i for i in range(1, 10)]
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

    plt.legend()
    plt.savefig('rbt_find_time_complexity.png')
    plt.show()

    print("Analysis complete! Check 'rbt_find_time_complexity.png' for the visualization.")
