

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
    sum:float = 0
    for i in arr:
        sum += i
    return sum / len(arr)

def get_percentile(arr:list[float], percentile:float)->float:
    if not arr:
        return 0
    if percentile <= 0:
        return arr[0]
    if percentile >= 100:
        return arr[-1]
    
    N = len(arr)
    R = percentile / 100.0 * (N + 1)
    
    if R.is_integer():
        return arr[int(R) - 1]
    else:
        # Linear interpolation
        lower_index = int(R) - 1
        upper_index = lower_index + 1
        if upper_index >= N:
            return arr[lower_index]
        
        fraction = R - lower_index - 1
        return arr[lower_index] + fraction * (arr[upper_index] - arr[lower_index])

def get_std(arr:list[float], mean:float)->float:
    sum:float = 0
    for n in arr:
        sum += (n - mean) ** 2
    return (sum / len(arr)) ** 0.5

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