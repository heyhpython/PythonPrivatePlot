# coding=utf-8
# builtins
# third party package
# self built


def main(date_str):
    import datetime
    try:
        year, month, day = date_str.split('-')
        year, month, day = int(year), int(month), int(day)
        if year < 1990:
            print("Invalid Input")
            return
        input_date = datetime.date(year, month, day)
    except Exception:
        print("Invalid Input")
        return

    origin = datetime.date(1989, 12, 31)
    date_delta: datetime.timedelta = input_date - origin
    days = date_delta.days
    days = days % 5
    # print(days)
    if 0 < days <= 3:
        print("He is working")
    elif days in (0, 4):
        print("He is having a rest")


if __name__ == "__main__":
    import sys

    while 1:
        # 读取每一行
        line = sys.stdin.readline().strip()
        # 把每一行的数字分隔后转化成int列表
        date = line
        if date != "":
            main(date)
        else:
            break

    # print(main("2014-12-22"))  # working
    # # print(main("2014-12-23"))  # working
    # print(main("2014-12-24"))  # rest
    # print(main("2014-12-32"))  # invalid
