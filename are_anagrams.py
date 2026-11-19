def are_anagrams(a, b):
    s1 = a.lower()
    s2 = b.lower()
    if s1 == s2:
        return False
    return sorted(s1) == sorted(s2)