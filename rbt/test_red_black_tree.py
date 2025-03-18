import pytest
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
