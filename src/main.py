from src.dto.FileDTO import  FileDTO
from src.services.UtilsFunctions import UtilsFunctions


def main():
     files = FileDTO("1","2","3")
     utils = UtilsFunctions()
     print(utils.jsonDumps(files))


if __name__ == '__main__':
    main()
