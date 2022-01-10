from typing import List, Tuple


def to_2d_index(index: int):
    """"
    Given an index representing the position in a list of 16 integers, return the 2D coordinates to which that index 
    translates on a 4x4 board, which has indices 0 <= x <= 3 for the rows and 0 <= y <= 3 for the columns.
    :param index int the index in a list of length 16
    :return Tuple(int, int) the 2D indices on a 4x4 board
    """
    assert 0 <= index < 16
    return index // 4, index % 4

def apply_transposition(configuration: List[int], transposition: Tuple[int, int]):
    """
    Given a list of integers, representing a configuration of the 15 puzzle, and a two-integer tuple, representing 
    a transposition to be made in the given configuration, check that the transposition is valid (in terms of the 
    rules of the 15 puzzle) and apply the transposition.
    :param configuration List[int] a configuration of the 15 puzzle, represented as a List with numbers 0 <= x <= 15.
    :param transposition Tuple[int, int] two positions on the board between which a transposition should be made 
    :return void, the function does not return anything, it just swaps the values at the two indices in the given list.
    """
    i, j = transposition
    assert i in range(16) and j in range(16)
    assert i != j
    i2d, j2d = to_2d_index(i), to_2d_index(j)
    # check that the cells are in swappable positions
    assert abs(i2d[0] - j2d[0]) + abs(i2d[1] - j2d[1]) == 1
    # check that one of the cells is the empty square
    assert configuration[i] == 0 or configuration[j] == 0
    configuration[i], configuration[j] = configuration[j], configuration[i]


def apply_transpositions(configuration: List[int], transpositions: List[Tuple[int, int]]):
    """
    Given a configuration and a list of transpositions (each of which is represented as a two-integer tuple), apply the
    transpositions sequentially
    :param configuration: List[int] a representation of a configuration of the 15-puzzle
    :param configuration List[Tuple[int, int]] a sequence of transpositions to be applied
    :return void, the function does not return anything, just applies the transpositions to the list.
    """
    for transposition in transpositions:
        apply_transposition(configuration, transposition)

# cycle which covers the whole board, and allows us to move any piece into top left corner
cycle1 = [0,4,8,12,13,14,15,11,7,3,2,6,10,9,5,1]

# cycle which allows us to move any piece into the square below the top left corner (1, 0); but does not involve
# position in bottom left corner (and also does not affect top left corner, since we want that piece to be fixed)
cycle2a = [1,5,4,8,9,13,14,15,11,10,6,7,3,2]

# another cycle which allows us to move any piece into the (1, 0) position, though this one misses the position in the
# top right corner (and also does not affect the top left corner)
cycle2b = [1,5,4,8,12,13,9,10,14,15,11,7,6,2]

# cycle which allows us to move any square into the square to the right of the top left corner (0,1). This cycle
# leaves the cell in the top left and the one below it unaffected
cycle3 = [1,5,9,8,12,13,14,15,11,10,6,7,3,2]

# this cycle allows us to move the hole into the (1,1) position
cycle4 = [2,6,5,9,8,12,13,14,15,11,7,3]



def cyclic_shift(configuration: List[int], path: List[int]) -> List[Tuple[int, int]]:
    """
    Given a configuration and a cycle existing within the 15-puzzle, perform a single cyclic shift along the given cycle/path, 
    and return a list of the performed transpositions.
    :param configuration: List[int] the given initial configuration of the 15-puzzle
    :param path: List[int] one of the several cycles which exist in the 15-puzzle, and can be used to get any piece
    into the top left corner, or an adjacent position.
    :return List[Tuple[int, int]] a list of transpositions 
    """
    start = 0
    while configuration[path[start]] != 0:
        start += 1
    rotated = path[start:] + path[:start]
    transpositions = []
    for i in range(len(rotated) - 1):
        transpositions += [(rotated[i], rotated[i+1])]
    apply_transpositions(configuration, transpositions)
    return (transpositions)


def do_3_cycle(cfg: List[int], a: int, b:int, c:int) -> List[Tuple[int, int]]:
    """
    Given a configuration, and three squares on the board, represented as a, b and c, which we would like to cycle 
    (a -> b -> c -> a), perform the transpositions necessary to do the 3-cycle, and return a list with all the 
    transpositions performed.
    The general strategy is to use cycles to get a, b, c and the empty square to the top left corner, then do the 3-cycle
    there and then return a to where b was, b to where c was and c to where a was. 
    :param cfg: List[int] the current configuration of the 15-puzzle
    :param a: int one of the numbers involved in the 3-cycle, which will be moved to b's position
    :param b: int one of the numbers involved in the 3-cycle, which will be moved to c's position
    :param c: int one of the numbers involbed in the 3-cycle, which will be moved to a's position
    :return List[Tuple[int, int]] a list of all the transpositions which were done (those needed to get a, b, and the
    blank square into the top left corner, plus those for the 3-cycle, plus those to move a, b, c back)
    """
    assert a in range(16) and b in range(16) and c in range(16)
    assert a != b and a != c and b != c
    assert a != 0 and b != 0 and c != 0
    transpositions = []
    # move a to top left corner
    while cfg[0] != a:
        transpositions += cyclic_shift(cfg, cycle1)
    # move c below a
    # if c is not in bottom left corner, use cycle2a
    if cfg[12] != c:
        # make sure empty square is not in bottom left corner, if it is, move it out (left bottom corner is excluded from cycle) 
        if cfg[12] == 0:
            transposition = (12, 8 if cfg[8] != c else 13)
            transpositions += [transposition]
            apply_transposition(cfg, transposition)
        while cfg[4] != c:
            transpositions += cyclic_shift(cfg, cycle2a)
    # if c is in the bottom corner, then use cycle2b
    else:
        assert cfg[12] == c
        # make sure empty square is not in top right corner, if it is, move it out (top right corner is excluded from cycle)
        if cfg[3] == 0:
            transposition = (3, 7)
            transpositions += [transposition]
            apply_transposition(cfg, transposition)
        while cfg[4] != c:
            transpositions += cyclic_shift(cfg, cycle2b)
    # move b to the right of a  
    while cfg[1] != b:
        transpositions += cyclic_shift(cfg, cycle3)
    # move empty cell to (1, 1)
    if cfg[10] == 0:
        transposition = (10, 11)
        transpositions += [transposition]
        apply_transposition(cfg, transposition)
    while cfg[5] != 0:
        transpositions += cyclic_shift(cfg, cycle4)
    # now everything is ready for conjugation
    assert cfg[0] == a and cfg[1] == b and cfg[4] == c and cfg[5] == 0
    abccycle_and_reverse = [(1,5), (0,1), (0,4), (4,5)]+list(reversed(transpositions))
    apply_transpositions(cfg, abccycle_and_reverse)
    return transpositions + abccycle_and_reverse

def transpositions_solution(configuration: List[int]) -> List[Tuple[int, int]]:
    """
    Given an initial configuration of the 15-puzzle, this function will find the 3-cycles by which the initial
    permutation can be transformed into the final permutation. For each 3-cycle it will call do_3_cycle() to 
    perform the transpositions, and also collect all the transpositions that were done and return them.
    Note that the transpositions are done on a copy of the list that's passed, so the list that is passed remains unchanged.

    :param configuration: List[int] a list of 16 integers, 0 to 15, representing an initial configuration of the 15-puzzle
    :return List[Tuple[int, int]] a list of all transpositions made in arriving at The Final Solution.
    """
    standard = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
    transpositions = []
    current = list(configuration)
    for i in range(13):
        if current[i] != standard[i]:
            idx = current.index(standard[i])
            assert idx > i
            spare = i + 1 if i+1 != idx else i+2
            assert i != idx and i != spare and idx != spare
            a, b, c = current[idx], current[i], current[spare]
            cycle_transpositions = do_3_cycle(current,a,b,c)
            transpositions += cycle_transpositions
        assert current[i] == standard[i]

    return transpositions

def solution(configuration: List[int]) -> List[int]:
    """
    Convert the solution given by transpositions_solution() into the correct format - rather than a list of transpositions,
    we will only have a list of numbers, which suggest which of the tiles should be moved.

    :param configuration: List[int] the initial configuration of the 15-puzzle, as a list of 16 ints, 0 to 15
    :return List[int] a list of integers, representing the moves that need to be made to solve the puzzle. 
    """
    transpositions = transpositions_solution(configuration)
    answer = []
    current = list(configuration)
    for trans in transpositions:
        i, j = trans
        label = current[i] if current[i] != 0 else current[j]
        answer.append(label)
        apply_transposition(current, trans)
    return (answer)




def main() -> None:
    # print(transpositions_solution([2,3,7,4,5,15,12,8,1,13,0,9,14,6,10,11]))
    # print(transpositions_solution([5,1,4,8,9,6,3,11,10,2,15,7,13,14,12,0]))
    trial = [1,9,6,2,10,5,11,4,3,14,8,7,13,15,12,0]
    print(transpositions_solution(trial))
    #print(trial)
    answer = solution(trial)
    print(answer)
    print(len(answer))



if __name__ == '__main__':
    main() 
    
    