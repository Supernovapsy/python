"""Edit Distance problem
Given two strings x & y, computes the minimum number of "edits" which will be able to
turn one into the other and vice versa. This operation is reversible, so only
one way needs to be calculated.

Edits consist of
1. Insertion of a character.
2. Deletion of a character.
3. Replacement of a character.

Each of these operations is designated to have cost 1, and a solution
consists of an ordered list of such operations on a position in string b. After
these operations, x should become y.

1. Subproblem: x[i:] and y[j:] suffixes.
2. Guess: Each step attempts to answer the question: How do we operate on the
first character of x[i:] in order to make it the same as the first character of
y[j:]?
    1) insertion of y[j] at x[i:].
    2) Replacement of x[i] by y[j]
    3) Deletion of x[i] from the suffix x[i:]
3. Recurrence: Picks the best of the three choices by adding 1 to the cost of
the corresponding DP subproblem.

Base cases:
    1) if j == len(y), then return cost of deleting x[i:].
    2) if i == len(x), then return cost of adding y[j] to x.

One problem: How do you know that your way of solving this problem is "brute
force" enough? That is, it has enough coverage that all possible ways of
editing the document which can arrive at an optimal solution is considered?

Idea: First, find a method which solves the problem. Second, prove that at each
iteration of the subproblem, the algorithm considers all ways which might be
the optimal solution, or equivalently only throws away considerations which are
not optimal. See 5. for this step.

4. Topological order: matrix, going from top right to bottom left if Cartesian
coords are used.

5.
Proof for the above proposal for edit distance:
    Claim: The algorithm gives a solution which solves the edit distance problem.
        DP(x, i, y, j) returns inf if it does not solve the problem.
        However, there will be a branch of the recursion which adds all
        characters in b to a, and then deletes all remaining characters of a.
        Since this is correct, and will always work, this solution solves the
        problem.
    Claim: The algorithm gives an optimal solution.
        subclaim: The base cases are solved optimally.
            In each of the base cases, one of the suffixes is emtpy. In order
            for one to become the other, only deletion or insertion can make
            progress in each of the two possible cases of j == len(y) and i ==
            len(x) respectively. The other two do not make progress. Thus, the
            base cases are optimal.
        subclaim: All subproblems in the recursion tree from the root of the
        subproblem tree consider all optimal solutions, assuming that the
        children subproblems are solved optimally.
            Let DP(x, i, y, j) be an arbitrary subproblem.
            Assume DP(x, i + 1, y, j), DP(x, i + 1, y, j + 1) and DP(x, i, y, j
            + 1) are solved optimally, and let these three subproblems be
            called s1, s2, and s3.
            Trivially, the subproblem having the lowest cost combined with one
            of the three edits solves the problem.
            subsubclaim: No other possible sequence of edits solves the problem
            better than one of the three.
                Assume there is a different and better edit in this subproblem which produces
                a better edit distance.
                Such an edit must occur at the first character in x[i:] or a
                later character. If an edit occurs later than the first
                character, then this edit or an edit with an equivalent
                progress will be considered in a later subproblem. NOTE I don't
                think this is rigorous, but that's the best I can do for now.
"""
from sys import argv

def test_edit_distance(x, y):
    edit_list = DP(x, y)
    print x
    for edit in edit_list:
        if edit[0] == 0:
            x = x[:edit[1]] + edit[2] + x[edit[1]:]
        elif edit[0] == 1:
            x = x[:edit[1]] + edit[2] + x[edit[1] + 1:]
        elif edit[0] == 2:
            x = x[:edit[1]] + x[edit[1] + 1:]
        print x
    assert x == y, "%s does not equal %s after manipulation!" % (x, y)

def DP(x, y):
    """Implementation is easyish after problem formulation.
    Note that the offset is required in order to implement with linear space."""
    def DP_aux(x, i, y, j, offset):
        if (i, j) in mem:
            return mem[i, j]
        if i == len(x):
            mem[i, j] = [(0, len(x) + offset, y[k]) for k in range(j, len(y))]
#             print "returning %r from if" % mem[i, j]
        elif j == len(y):
            mem[i, j] = [(2, i + offset, None)] * (len(x) - i)
#             print "returning %r from elif" % mem[i, j]
        elif x[i] == y[j]:
            mem[i, j] = DP_aux(x, i + 1, y, j + 1, offset)
            return mem[i, j]
        else:
            insert = DP_aux(x, i, y, j + 1, offset + 1)[:]
            replace = DP_aux(x, i + 1, y, j + 1, offset)[:]
            delete = DP_aux(x, i + 1, y, j, offset - 1)[:]
            if len(insert) <= len(replace) and len(insert) <= len(delete):
                insert.append((0, i + offset, y[j]))
                mem[i, j] = insert
            elif len(replace) <= len(insert) and len(replace) <= len(delete):
                replace.append((1, i + offset, y[j]))
                mem[i, j] = replace
            else:
                delete.append((2, i + offset, None))
                mem[i, j] = delete
#             print "returning %r from else" % mem[i, j]
        return mem[i, j]

    # Each element is (i, j): (next edit id, index, character to insert or
    # replace with, index offset)
    # 0 is insert, 1 is replace, 2 is delete.
    mem = {}
    return list(reversed(DP_aux(x, 0, y, 0, 0)))

if __name__ == "__main__":
    test_edit_distance(argv[1], argv[2])
