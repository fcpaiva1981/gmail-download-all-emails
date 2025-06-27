import datetime
from src.dto.FileDTO import  FileDTO
from src.services.UtilsFunctions import UtilsFunctions



def main():
     current_time = datetime.datetime.now()
     files = FileDTO("1","2","3")
     utils = UtilsFunctions()
     print(utils.jsonDumps(files))

     date_time_sample = utils.formatDate(str(current_time))
     print(utils.jsonDumps(date_time_sample))


if __name__ == '__main__':
    main()
