def commonChars(A: []):
    if not A:
        return []
    A = sorted(A, key=lambda a: len(a))
    c = {}
    for i in A[0]:
        if i in c:
            c[i] += 1
        else:
            c[i] = 1

    for key in c:
        count = c[key]
        for chars in A[1:]:
            pass



print(commonChars(["bella", "label", "roller"]))
