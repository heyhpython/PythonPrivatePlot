# unsolved

def isMatch(s: 'str', p: 'str') -> 'bool':
    if s == p:
        return True

    tongPeifu = '.'

    def checkEqual(s1, s2):
        if s1 == s2:
            return True
        elif s1 == tongPeifu or s2 == tongPeifu:
            return True

        else:
            False