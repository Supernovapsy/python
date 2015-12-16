'''
1. Subproblem: solution for suffix words[i:]
Number of subproblems: n
2. Guess: All words as long as there is space to contain both the words and the
spaces between them.
3. Relate subproblem solutions: Take the minimum of the badness function from
guessing all valid guesses (hence brute force).
4. recurse & memoize: Use i as the idenfication for each subproblem, and can
store the badness metric in an array.
5. This will solve the original problem because it follows the optimal
subproblem structure:
Claim that it follows:
    Assume that the subproblem i for the final solution is not optimal. Then, there
    exists a better way of structuring the words of the suffix words[i:], thus,
    the original solution is not optimal. Contradiction!
    Therefore, the optimal subproblems structure exists for this problem
    definition.

Now, augment this algorithm by storing not only the value of the badness
function, but also the i for the best guess for each subproblem solved. This
will tell the printer how many words to skip before going to a new line.

Finished.
'''
'''
input: l (list of integers), M
'''
def badness(i, j, l, M):
    """i and j are the words at which two cutoff points occur which form the
    current line on the computer screen. i represents the ith word at which the
    current line starts, and j represents the jth word, which means the word at
    which the next line starts. The word indices go from 0 to n - 1."""
    return (M - (j - i + 1 + reduce(lambda x, y: x + y, l[i-1:j]))**3 if j != len(l) else 0

# Want to compute DP(0, l, M)
# GVIM: how to make indents permanent when nothing is written?
# GVIM: how to always comment at the end of the indents?
# GVIM: cursor always goes to the end of the line after edit?
def DP_td(l, M):
    mem = {0:0}
    return DP_td_aux(0, l, M)

def DP_td_aux(i, l, M):
    """Top-down DP algorithm"""
    if i in mem:
        return mem[i][0] # The first element is the score.

    spaces_left = M - l[i]
    if spaces_left < 0:
        raise Exception("word %d is longer than the width of the screen." % i)
    badness_score = float('inf')
    for j in range(i + 1, len(l) + 1):
        if spaces_left >= 0:
            new_badness_score = badness(i, j, l, M) + DP_td_aux(j, l, M)
            if new_badness_score < badness_score:
                best_j = j
                badness_score = new_badness_score
            # Subtract from it the length of the next
            # word and the space between the current and the next word.
            spaces_left -= l[j] + 1

    # Need to remember which word to cut off next.
    mem[i] = list(badness_score, best_j)
    return badness_score

def DP_bu(l, M):
    """Bottom-up algorithm. Notice the similarity of this to Dijkstra's
    relaxation algorithm."""
    mem = list([0, float('inf')] for i in range(len(l)))
    for i in reversed(range(len(l))):
        # Badness calculates the badness score from word i upto and excluding j.
        spaces_left = M - l[i]
        if spaces_left < 0:
            raise Exception("word %d is longer than the width of the screen." % i)
        for j in range(i + 1, len(l) + 1):
            if spaces_left >= 0:
                badness_score = mem[j][0] + badness(i, j, l, M)
                if badness_score < mem[i][0]:
                    mem[i] = [new_badness_score, j]
            # Subtract from it the length of the next
            # word and the space between the current and the next word.
            spaces_left -= l[j] + 1

def DP(l, M):
    # NOTE: this is not tested.
    # run either DP_td or DP_bu, then...
    newline_words = [mem[0][1]]
    while mem[newline_words[-1]][1] <= len(l) - newline_words[-1]:
        newline_words.append(mem[newline_words[-1]][1])
    return newline_words

