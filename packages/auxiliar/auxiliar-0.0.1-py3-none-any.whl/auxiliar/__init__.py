from collections import Counter


def are_all_the_same(a_list: list) -> bool:
    return 1 == len(Counter(a_list).values())


if __name__ == '__main__':
    a = [0, 1]
    b = [0, 0]
    print(f"a are {'' if are_all_the_same(a) else 'NOT '}all the same")
    print(f"a are {'' if are_all_the_same(b) else 'NOT '}all the same")
