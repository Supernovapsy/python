import sys

'''15 - 4: Longest Common Subsequence problem
x, y
1. subproblem x[i:], y[j:], the LCS between x[i:] and y[j:]
# of subproblems: |x||y|, quadratic in the size of the strings.
2. guess: is x[i] part of LCS?
3. connect between subproblems: If yes, then can look at x[i+1:], y[k:], where
k is the index of the character after the first character in y[j:] which is
equal to x[i]. If no, then simply disard x[i]. This is correct because if x[i]
is in LCS, then lcs(x, i + 1, y, k) contains the lcs which will form the lcs of
x[i:] and y[j:]. If x[i] is not a part of lcs, then the subsequence as said
above also contains the lcs for this case.
Time for each subproblem: time to search for the next element in j.
So, it might look like it's |x||y| * O(|y|), but since in total, only have to
search |y|, it's actually O(|x|+|y|) in total over all subproblems?
Well, at most it is O(|x||y|^2).
4. Topological order: from x[|x|] to x[0], until either string is empty for
top-down, at which time there are no longer subsequences to compare.
5. Solve the original problem?
Yes. It exhausively searches whether each character in x belongs to the LCS.
'''

def lcs(x, y):
    '''Returns one longest common subsequence between strings x and y.'''
    mem = {}

    def lcs_aux(x, i, y, j):
        if (i, j) in mem:
            return mem[(i, j)]
        if i == len(x) or j == len(y):
            mem[(i, j)] = ""
            return ""

        lcs1 = lcs_aux(x, i + 1, y, j)

        k = y.find(x[i], j)
        lcs2 = x[i] + lcs_aux(x, i + 1, y, k + 1) if k != -1 else ''

        mem[(i, j)] = lcs1 if len(lcs1) > len(lcs2) else lcs2
        return mem[(i, j)]

    return lcs_aux(x, 0, y, 0)

if __name__ == "__main__":
    print lcs(sys.argv[1], sys.argv[2])
