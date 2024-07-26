
from exception import MyCustomError

class Data:
    def __init__(self, headers: str) -> None:
        self.headers = headers
        self.amount = 
        return None

    def add_line(self, line: str) -> None:

        return None

def my_count_chars(line: str, chararacter: str) -> int:
    counter:int = 0
    for c in line:
        if c == chararacter:
            counter += 1
    return counter

def get_data(path: str) -> None:

    d = None
    t = "asdas, asd, asdasd, a"
    a = t.split(',')
    print(a)
    # with open(path, "r") as f:
    #     counter = 0
    #     for line in f:
    #         line = line.strip()
    #         if counter == 0:
    #             d = Data(line)
    #         else:
    #             d.ad


