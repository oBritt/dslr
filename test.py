import sys
import getdata
from exception import MyCustomError

def main() -> None:
    if len(sys.argv) != 2:
        print(f"Wrong usage [Executable] [dataset]")
        return None
    try:
        getdata.get_data(sys.argv[1])
    except MyCustomError as e:
        print(f"Some issues with {sys.argv[1]}")


if  __name__ == "__main__":
    main()