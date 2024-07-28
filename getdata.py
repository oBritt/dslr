
from exception import MyCustomError
from utils import *

class Data:
    def __init__(self, headers: str) -> None:
        header = headers.split(',')
        for h in headers:
            h = h.strip()
        self.amount: int = my_count_chars(headers, ',')
        self.data: list[list[str]] = [[] for _ in range(self.amount + 1)]
        for i in range(self.amount + 1):
            self.data[i].append(header[i])
        return None

    def add_line(self, line: str) -> None:
        if my_count_chars(line, ',') != self.amount:
            raise MyCustomError("") 
        args = line.split(',')
        for i in range(self.amount + 1):
            args[i] = args[i].strip()
            self.data[i].append(args[i])
        return None

    def fill_firs_colomn(self, des: list[str])->None:
        des.append("        ")
        des.append("Count   ")
        des.append("Mean    ")
        des.append("Std     ")
        des.append("Min     ")
        des.append("25%     ")
        des.append("50%     ")
        des.append("75%     ")
        des.append("Max     ")

    def fill_other_colomn(self, colomn: list[str], ind: int)->int:
        colomn.append(self.data[ind][0])
        counter:int = 0
        numbers:float = []
        for i in range(len(self.data[ind]) - 1):
            if self.data[ind][i + 1] != "":
                numbers.append(float(self.data[ind][i + 1]))
                counter += 1
        if counter == 0:
            return 0
        colomn.append(str("%.6f" % float(counter)))
        numbers.sort()
        mean:float = get_mean(numbers)
        colomn.append(str("%.6f" % mean))
        colomn.append(str("%.6f" % get_std(numbers, mean)))
        colomn.append(str("%.6f" % get_percentile(numbers, 0)))
        colomn.append(str("%.6f" % get_percentile(numbers, 25)))
        colomn.append(str("%.6f" % get_percentile(numbers, 50)))
        colomn.append(str("%.6f" % get_percentile(numbers, 75)))
        colomn.append(str("%.6f" % get_percentile(numbers, 100)))
        return 1

    def describe(self)->None:
        amount = 0
        valid = []
        for l in self.data:
            valid.append(check_if_numeric(l))
            amount += valid[-1]
        described:list[list[str]] = [[] for _ in range(amount + 1)]
        self.fill_firs_colomn(described[0])
        counter = 1
        for i in range(len(valid)):
            if valid[i]:
                if self.fill_other_colomn(described[counter], i) == 1:
                    counter += 1
                else:
                    described.pop(counter)
        output(described)


    def print_data(self)->None:
        output(self.data)

def get_data(path: str) -> Data:
    d = None
    with open(path, "r") as f:
        counter = 0
        for line in f:
            line = line.strip()
            if counter == 0:
                d = Data(line)
            else:
                d.add_line(line)
            counter += 1
    return d


