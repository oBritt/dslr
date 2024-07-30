import sys
import getdata
from pair_plot_display import Pair_plot
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
    s = Pair_plot(d.get_information_histogramm(), d.get_information_scatter())
    s.run()

if  __name__ == "__main__":
    main()