def my_atoi(str):
    s = str.strip()
    ret = ''
    if s[0] in ('-', '+'):
        ret = s[0]
        s = s[1:]

    for char in s:
        if char.isdigit():
            ret += char
        else:
            break
    return ret


print(my_atoi("0words and 987"))
import importlib

from imp import reload