import sys

def group_numbers_in_radius(numbers, radius):
    """Group numbers into sublists with a given radius.

    This is used for deduping - we want to make sure that
"""
    results, before, after = [], [], []

    print('group_numbers_in_radius', numbers, radius)

    def emit():
        result = before + after
        if not results:
            results.append(result)
        else:
            s, r = set(results[-1]), set(result)
            if s < r:
                results[-1] = result
            elif not (r <= s):
                results.append(result)
        before.append(after.pop(0))

        while before and after and before[0] < after[0] - radius:
            before.pop(0)

    while numbers:
        print('while', before, after, results)
        end = numbers.pop(0)
        while after and after[0] < end - radius:
            emit()
        after.append(end)

    while after:
        emit()

    return results


if __name__ == '__main__':
    numbers = [int(a) for a in sys.argv[1:]]
    print(group_numbers_in_radius(numbers, numbers.pop(0)))
