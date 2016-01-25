# Find the shortest substring in s which contains smaller strings t1, t2, and
# t3. ti are much shorter than s.

def find_substrings(s, t1, t2, t3):
    s1 = s2 = s3 = shortest = -1
    for j in range(1, len(s) + 1):
        i = j - len(t1)
        if i >= 0 and s[i:j] == t1:
            s1 = j
        i = j - len(t2)
        if i >= 0 and s[i:j] == t2:
            s2 = j
        i = j - len(t3)
        if i >= 0 and s[i:j] == t3:
            s3 = j

        if (s1 == j or s2 == j or s3 == j) and (s1 != -1 and s2 != -1 and s3 != -1):
            candidate = (min(s1 - len(t1), s2 - len(t2), s3 - len(t3)), j)
            if shortest == -1 or candidate[1] - candidate[0] < shortest[1] - shortest[0]:
                shortest = candidate

    return s[shortest[0]:shortest[1]] if shortest != -1 else None

print find_substrings("amhoewhoamusthotbenamed", 'mu', 'ho', 'am')
print find_substrings("xxxxxxxxaaaaxxaaxxxxx", 'x', 'ax', 'xa')
