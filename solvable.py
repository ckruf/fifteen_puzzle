import unittest
from typing import List

def is_fifteen_solvable(p: List[int]) -> bool:
    """
    A function which determines whether a given initial configuration of the fifteen puzzle is solvable. Done by checking
    parity of permutation using a bubble sort.
    :param p: List[int] the initial configuration of the 15 puzzle. The blank square is represented by 0.
    :return bool True if solvable, False otherwise
    """
    assert(len(p) == 16)
    print(f"Initial configuration: {p}")
    steps = 0
    for i in range(len(p)):
        changed = False
        for j in range(len(p) - i - 1):
            if p[j] > p [j+1]:
                tmp = p[j]
                p[j] = p[j+1]
                p[j+1] = tmp
                steps +=1
                changed = True
            #print(p)
        if not changed:
            break
    if steps % 2 == 0:
        print("It is not solvable")
        return False
    else:
        print("It is in fact solvable")
        return True


class FifteenSolvableTests(unittest.TestCase):
    def test1(self):
        self.assertTrue(is_fifteen_solvable([5, 1, 4, 8, 9, 6, 3, 11, 10, 2, 15, 7, 13, 14, 12, 0]))
    
    def test2(self):
        self.assertFalse(is_fifteen_solvable([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 14, 0]))
    
    def test3(self):
        self.assertTrue(is_fifteen_solvable([2, 6, 3, 4, 9, 11, 7, 8, 1, 13, 14, 12, 5, 10, 15, 0]))

    def test4(self):
        self.assertFalse(is_fifteen_solvable([5, 1, 8, 4, 9, 6, 3, 11, 10, 2, 15, 7, 13, 14, 12, 0]))

    def test5(self):
        self.assertFalse(is_fifteen_solvable([2, 6, 4, 3, 9, 11, 7, 8, 1, 13, 14, 12, 5, 10, 15, 0]))

    def test6(self):
        self.assertTrue(is_fifteen_solvable([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 13, 0]))

    def test7(self):
        self.assertFalse(is_fifteen_solvable([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 14, 13, 0]))

if __name__ == "__main__":
    unittest.main()