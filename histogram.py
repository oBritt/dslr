import sys
import getdata
from histogram_display import Histogramm
from exception import MyCustomError

def main() -> None:
    if len(sys.argv) != 2:
        print(f"Wrong usage [Executable] [dataset]")
        return None
    d = None
    try:
        d = getdata.get_data(sys.argv[1])
    except MyCustomError as e:
        print(f"Some issues with {sys.argv[1]}")
    h = Histogramm(1920, 1080, d.get_information_histogramm())
    h.run()

if  __name__ == "__main__":
    main()