import random

def my_count_chars(line: str, chararacter: str) -> int:
    counter:int = 0
    for c in line:
        if c == chararacter:
            counter += 1
    return counter

def is_float(s:str)->bool:
    if s == "":
        return True
    try:
        float(s)
        return True
    except ValueError:
        return False

def check_if_numeric(arr:list[str])->bool:
    i = 1
    while (i < len(arr)):
        if is_float(arr[i]) == False:
            return False
        i += 1
    return True

def get_mean(arr:list[float])->float:
    total:float = 0
    for i in arr:
        total += i
    return total / len(arr)

def get_percentile(arr: list[float], percentile: float) -> float:
    if not arr:
        return 0
    N = len(arr)
    if percentile <= 0:
        return arr[0]
    if percentile >= 100:
        return arr[-1]
    R = percentile / 100.0 * (N - 1)
    lower_index = int(R)
    upper_index = lower_index + 1
    
    if upper_index >= N:
        return arr[lower_index]
    fraction = R - lower_index
    return arr[lower_index] + fraction * (arr[upper_index] - arr[lower_index])

def get_std(arr:list[float], mean:float)->float:
    total:float = 0
    for n in arr:
        total += ((n - mean) ** 2)
    return (total / (len(arr) - 1)) ** 0.5

def output(data: list[list[str]]) ->None:
    max_len = [0 for _ in range(len(data))]
    for i in range(len(data)):
        for e in range(len(data[i])):
            if len(data[i][e]) > max_len[i]:
                max_len[i] = len(data[i][e])
    for i in range(len(data[0])):
        for e in range(len(data)):
            if max_len[e] > len(data[e][i]):
                print(' ' * (max_len[e] - len(data[e][i])), sep='', end='')
                print(data[e][i], end='')
                if e != len(data) - 1:
                    print('  ', end='')
            else:
                print(data[e][i], end='')
                if e != len(data) - 1:
                    print('  ', end='')
        print('\n', end='')

def split_range(start: float, end: float, n: int) -> list[list[float, float]]:
    if n <= 0:
        raise ValueError("Number of parts must be greater than zero")
    
    step = (end - start) / n
    ranges = [[start + step * i, start + step * (i + 1)] for i in range(n)]
    return ranges

def split_range_scatter(start: float, end: float, n: int) -> list[list[float, float]]:
    if n <= 0:
        raise ValueError("Number of parts must be greater than zero")
    
    step = (end - start) / (n - 2)
    start -= step
    ranges = [[start + step * i, start + step * (i + 1)] for i in range(n)]
    return ranges

def generate_colors():
    counter = 0
    colors = [(0, 51, 204), (204, 0, 0), (0, 102, 0), (102, 0, 102)]
    while True:
        if (counter <= 3):
            yield colors[counter]
        else:
            yield (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        counter += 1

def map_number(value, from_min, from_max, to_min, to_max):
    if from_min == from_max:
        raise ValueError("The source range cannot have the same min and max values.")
    scale = (to_max - to_min) / (from_max - from_min)
    return to_min + (value - from_min) * scale

# if __name__ == "__main__":
#     colors = generate_colors()
#     for i in range(5):
#         print(next(colors))

