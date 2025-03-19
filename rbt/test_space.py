import random
import matplotlib.pyplot as plt
from pympler import asizeof
from scipy.optimize import curve_fit
from rbt.red_black_tree import RedBlackTree

def profile_rbt_insert(size):
    rbt = RedBlackTree()
    data = random.sample(range(1, size * 10), size)
    sample = random.sample(data, size)
    random.shuffle(sample)
    
    for num in sample:
        rbt.insert(num)
    
    memory_used = asizeof.asizeof(rbt)
    return memory_used

def test_insert_space():
    sizes = [8000, 16000, 32000, 64000, 128000, 256000, 512000, 1024000]
    spaces = []

    for size in sizes:
        print(f"Testing with size {size}")
        space_taken = profile_rbt_insert(size)
        space_taken_mb = space_taken / (1024 * 1024)
        spaces.append(space_taken_mb)
        print(f"Memory used: {space_taken_mb:.2f} MB")

    plt.figure(figsize=(6, 6))
    plt.plot(sizes, spaces, 'o-', label='Measured space')
    plt.xlabel('Input Size (n)')
    plt.ylabel('Space (MB)')
    plt.title('Red-Black Tree Space Complexity')
    plt.grid(True)
    plt.legend()
    plt.savefig('rbt_space_complexity.png')
    plt.show()

    print("Analysis complete! Check 'rbt_space_complexity.png' for the visualization.")
