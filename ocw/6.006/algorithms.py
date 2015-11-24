#!/usr/bin/python
# Algorithm writing practice from CLRS.

from sys import argv

def swap(a, i, b, j):
    c = a[i]
    a[i] = b[j]
    b[j] = c

def insertion_sort(a):
    """2.1-2 Insertion sort in non-increasing order."""

    for i in range(1, len(a)):
        # Invariant: a[:i] is a sorted subarray of a.
        key = a[i]
        for j in reversed(range(i)):
            if a[j] > key:
                # If the next element to the left is less than the key, then shift it to the right.
                a[j + 1] = a [j]
            else:
                # If the next element to the left is not less to the key, then the key belongs to the right of it.
                a[j + 1] = key
                # Break to finish the insertion of this element into the sorted subarray.
                break
        else:
            # If a break did not occur, then the key must belong to where j was last, which actually must be the 0th element.
            assert(j == 0)
            a[j] = key

def quick_sort(a):
    quick_sort_aux(a, 0, len(a))

def quick_sort_aux(a, begin, end):
    """In-place sort of array a.

    Quick sort chooses a random pivot element and in each iteration makes sure that all elements to the left and right of it are smaller and greater than it respectively."""

    # We are finished if the array length is 1 or 0.
    length = end - begin
    if length < 2:
        return

    pivot_index = length / 2 + begin
    pivot = a[pivot_index]
    
    # Truth: If the pivot element is in the right place in the array, then the elements greater than the pivot on the left of the pivot equals the number of
    # eleements less than the pivot on its right.

    elements_less_than_pivot = 0
    for i in range(begin, end):
        if i != pivot_index and a[i] < pivot:
            elements_less_than_pivot += 1

#    print
#    print a
#    print a[begin:end]
    swap(a, begin + elements_less_than_pivot, a, pivot_index)
#    print begin + elements_less_than_pivot, pivot
#    print a[begin:end]
    
    i = begin
    j = begin + elements_less_than_pivot + 1
    left_wrap = False
    right_wrap = False
    while True:
        while i != elements_less_than_pivot + begin and a[i] < pivot:
            i += 1
        while j != end and a[j] > pivot:
            j += 1
        if i == elements_less_than_pivot + begin and j == end:
            break
        # Need to wrap around due to the possibility of equal elements in the array.
        # If both left and right arrays are wrapped, then we're done.
        elif i == elements_less_than_pivot + begin and not right_wrap:
            left_wrap = True
            i = begin
            while i != elements_less_than_pivot + begin and a[i] != pivot:
                i += 1
        elif j == end and not left_wrap:
            right_wrap = True
            j = begin + elements_less_than_pivot + 1
            while j != end and a[j] != pivot:
                j += 1
        # If after wrapping around no element is found to be able to change, then we're done because the element that's waiting to be swapped must be equal to the pivot by the truth above.
        if i == elements_less_than_pivot + begin or j == end:
            break
        swap(a, i, a, j)
        #print a[begin:end]
        i += 1
        j += 1
    
    quick_sort_aux(a, begin, begin + elements_less_than_pivot)
    quick_sort_aux(a, begin + elements_less_than_pivot + 1, end)

def counting_sort(arr, M, m = 0, key = None):
    """O(n) sorting algorithm! M is the maximum element, m is the minimum element."""
    if key is not None:
        a = map(key, arr)
    else:
        a = arr

    print m, M
    k = M - m + 1
    storage = [0] * k
    for e in a:
        assert e < M and e > m, "error during counting sort. Every element must be less than parameter k."
        # Shift all integers to positive numbers.
        e -= m
        storage[e] += 1
    # Calculating the discrete integral, which helps to keep track of where each element goes.
    cumulative = [0] * k
    cumulative[0] = storage[0]
    for i in range(1, k):
        cumulative[i] = cumulative[i - 1] + storage[i]

    sorted_indices = [0] * len(a)
    for i in reversed(range(len(a))):
        # The value of the ith element of sorted_indices indicates where should the ith element of a[i] go.
        sorted_indices[i] = cumulative[a[i]]- 1 # invariant: there are cumulative[v] elements <= v.
        cumulative[a[i]] -= 1

    ret = [0] * len(a)
    for i, index in enumerate(sorted_indices): 
        # The value of the ith element of sorted_indices indicates where should the ith element of a[i] go.
        ret[index] = arr[i]

    return ret

        #storage = [0 for i in range(k)]
        #for e in a:
        #    assert key(e) < k, "error during counting sort. Every element must be less than parameter k."
        #    storage[key(e)] += 1

        #count = 0
        #for i, v in enumerate(storage):
        #    for j in range(v):
        #        a[count] = i
        #        count += 1

    #ret = list()
    #for i, n in enumerate(storage):
    #    ret.extend([i] * n)

    #return ret

def test_sorting():
    """Give 20000000 as input and disabling quick and insertion sort will show that counting sort is faster than builtin sort."""
    import random, sys

    k = 100

    if len(sys.argv) == 1:
        print "Need to give arguments for testing sort."
        exit()
    elif len(sys.argv) == 2:
        rand_array = [random.randrange(k) for i in xrange(int(sys.argv[1]))]
    else:
        rand_array = sys.argv[1:]

    rand_array1 = rand_array[:]
    rand_array2 = rand_array[:]
    rand_array3 = rand_array[:]

    #print "insertion sort beginning."
    #sys.stdout.flush()
    #insertion_sort(rand_array1)

    #print "quick sort beginning."
    #sys.stdout.flush()
    #quick_sort(rand_array2)

    print "counting sort beginning."
    sys.stdout.flush()
    rand_array3 = counting_sort(rand_array3, k)
    
    print "builtin sort beginning."
    sys.stdout.flush()
    sorted_array = sorted(rand_array)
    #assert rand_array1 == sorted_array, "Insertion sort has a bug!"
    #assert sorted_array == rand_array2, "Quick sort has a bug!"
    assert sorted_array == rand_array3, "Counting sort has a bug!"

if __name__ == "__main__":
    test_sorting()
