import UserDefineFun
from sys import *


def main():
    print("Process Monitoring Automation with periodic Mail Sender....")
    print("Application name:" + argv[0])

    if (len(argv) != 3):
        print("Invalid number of argumnets")
        exit()

    if (argv[1] == "-h") or (argv[1] == "-H"):
        print("This Script is used log record of running processess")
        exit()

    if (argv[1] == "-u") or (argv[1] == "-U"):
        print("usage : ApplicationName AbsolutePath_of_Directory")
        exit()
    #Processinfor(argv[1],argv[2])

    arr = UserDefineFun.findDup(home.drive)

if __name__ == "__main__":
    main()
