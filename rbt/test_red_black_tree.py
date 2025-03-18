import pytest
import random
from rbt.red_black_tree import RedBlackTree

def test_insertion():
    rbt = RedBlackTree()
    rbt.insert(20)

    assert str(rbt) == "20(BLACK),NIL,NIL"

    rbt.insert(15)

    assert str(rbt) == "20(BLACK),15(RED),NIL,NIL,NIL"

    rbt.insert(17)

    assert str(rbt) == "17(BLACK),15(RED),NIL,NIL,20(RED),NIL,NIL"

    rbt.insert(10)
    rbt.insert(25)
    rbt.insert(35)

    expected = "17(BLACK),15(BLACK),10(RED),NIL,NIL,NIL,25(BLACK),20(RED),NIL,NIL,35(RED),NIL,NIL"
    assert str(rbt) == expected

def test_find():
    rbt = RedBlackTree()
    rbt.insert(50)
    rbt.insert(30)
    rbt.insert(70)

    assert rbt.find(50) is not None
    assert rbt.find(30) is not None
    assert rbt.find(70) is not None
    assert rbt.find(100) is None

def test_deletion():
    rbt = RedBlackTree()
    rbt.insert(20)
    rbt.insert(15)
    rbt.insert(30)
    rbt.insert(10)
    rbt.insert(25)
    rbt.insert(35)

    expected1 = "20(BLACK),15(BLACK),10(RED),NIL,NIL,NIL,30(BLACK),25(RED),NIL,NIL,35(RED),NIL,NIL"
    assert str(rbt) == expected1

    assert rbt.find(30) is not None
    assert rbt.find(10) is not None
    rbt.delete(10)

    assert rbt.find(30) is not None
    assert rbt.find(10) is None
    expected2 = "20(BLACK),15(BLACK),NIL,NIL,30(BLACK),25(RED),NIL,NIL,35(RED),NIL,NIL"
    assert str(rbt) == expected2

    rbt.delete(20)

    assert rbt.find(20) is None
    expected2 = "25(BLACK),15(BLACK),NIL,NIL,30(BLACK),NIL,35(RED),NIL,NIL"
    assert str(rbt) == expected2

    rbt.delete(25)

    assert rbt.find(25) is None
    expected2 = "30(BLACK),15(BLACK),NIL,NIL,35(BLACK),NIL,NIL"
    assert str(rbt) == expected2

    rbt.delete(35)

    assert rbt.find(35) is None
    expected2 = "30(BLACK),15(RED),NIL,NIL,NIL"
    assert str(rbt) == expected2

    rbt.delete(30)

    assert rbt.find(30) is None
    expected2 = "15(BLACK),NIL,NIL"
    assert str(rbt) == expected2

    rbt.delete(15)

    assert rbt.find(15) is None
    assert str(rbt) == "NIL"


def test_validate():
    random.seed(42)

    # Test Case 1: Small tree with 10 elements
    test_data_1 = [42, 23, 87, 65, 12, 57, 31, 99, 8, 76]

    # Test Case 2: Medium tree with 20 elements in ascending order (worst case for many BSTs)
    test_data_2 = list(range(1, 21))

    # Test Case 3: Medium tree with 20 elements in random order
    test_data_3 = random.sample(range(1, 100), 20)

    test_data_4 = random.sample(range(1, 1000), 100)

    test_data_5 = random.sample(range(1, 10000), 1000)

    # Function to test a Red-Black Tree with a dataset
    def test_rbt(data, case_name):
        print(f"\n===== Testing {case_name} =====")
        print(f"Input data: {data}")
        
        # Create tree and insert data
        rbt = RedBlackTree()
        for item in data:
            rbt.insert(item)
        
        # Check tree properties
        height = rbt.height()
        log2n = import_math().log2(len(data))
        print(f"Tree size: {len(data)}")
        print(f"Tree height: {height}")
        print(f"log2(n): {log2n:.2f}")
        print(f"2*log2(n): {2*log2n:.2f}")
        
        # For a Red-Black Tree, height should be <= 2*log2(n)
        assert height <= 2*log2n + 1  # +1 for rounding
        
        black_height = rbt.black_height()
        print(f"Black height: {black_height}")
        
        # Allow for a margin on either side
        min_expected = import_math().floor(len(data) / 2 + 1 - 1.5)
        max_expected = import_math().ceil(len(data) / 2 + 1 + 1.5)
        # Expected black height is approximately log2(n)
        assert black_height >= min_expected
        assert black_height <= max_expected
        
        assert rbt.validate()
        print(f"Tree is valid Red-Black tree is valid")
        
        for item in data:
            found = rbt.find(item)
            assert found is not None
        print(f"All elements can be found")
        
        return rbt

    # Helper function for log2 (to make code more readable)
    def import_math():
        import math
        return math

    # Run tests
    test_rbt(test_data_1, "Small Tree (10 random elements)")
    test_rbt(test_data_2, "Medium Tree (20 ascending elements)")
    test_rbt(test_data_3, "Medium Tree (20 random elements)")
    test_rbt(test_data_4, "Big Tree (100 random elements)")
    test_rbt(test_data_5, "Big Tree (1000 random elements)")
