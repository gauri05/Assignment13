import schedule
import time
import os
import psutil
import urllib3
# C:\Users\Gauri\AppData\Local\Programs\Python\Python37\Lib\site-packages\psutil\__init__.py
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib


def Processinfor(dir,toaddr):
    listprocess = []

    if not os.path.exists(dir):
        try:
            os.mkdir(dir)
        except:
            pass  # is same as continue

    separator = "-" * 80
    log_path = os.path.join(dir, " file %s.log" % (time.time()))
    f = open(log_path, 'w')
    f.write(separator + "\n")
    f.write("Process Logger:""\n")
    f.write(separator + "\n")
    f.write("\n")

    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])

            listprocess.append(pinfo)

        except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    for element in listprocess:
        f.write("%s\n" % element)

    print("Log file is successfully generated at location %s" % (log_path))

    connected = is_connected()

    if connected:
        starttime = time.time()
        MailSender(log_path, toaddr)
        endtime = time.time()

        print('Took %s seconds to send mail' % (endtime - starttime))


def is_connected():
    try:
        urllib3.connectionpool.connection_from_url('http://216.58.192.142 ', timeout=1)
        # urllib3.connection_from_url('https://www.google.com/ ',timeout=1)   #https://www.google.com/   #http://216.58.192.142
        return True
    except urllib3.URLError as err:
        return False


def MailSender(filname, toaddr):
    try:
        fromaddr = "botregauri@gmail.com"

        #print (toaddr)
        msg = MIMEMultipart()

        msg['From'] = fromaddr
        msg['To'] = toaddr

        body = """
                Hello %s,
                       Welcome to XYZ company.
                       Please find attached document which contains Log of Running Process.
                       Log file is created at : %s

                       This is auto generated mail.

                Thanks and Regards,
                Gauri Botre
                """ % (toaddr, time)

        subject = """Process log generted at : %s""" % time

        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        attachment = open(filname, "rb")

        p = MIMEBase('application', 'octet-stream')

        p.set_payload((attachment).read())

        encoders.encode_base64(p)

        p.add_header('Content-Disposition', "attachment; filename=%s" % filname)

        msg.attach(p)

        s = smtplib.SMTP('smtp.gmail.com', 587)

        s.starttls()

        s.login(fromaddr, "3796gouri")

        text = msg.as_string()

        s.sendmail(fromaddr, toaddr, text)

        s.quit()

        print("Log file successfully sent throught Mail")
    except Exception as E:
        print("Unable to send mail", E)


def findDup(path, file="Log"):
    icnt=0
    dicnt=0
    flag = os.path.isabs(path)

    if flag == False:
        path = os.path.abspath(path)

    exits = os.path.isdir(path)
    #print(exits)
    dups = {}

    if not os.path.exists(file):
        try:
            os.mkdir(file)
        except:
            pass

    separator = "-" * 80
    log_path = os.path.join(file, " file %s.log" % (time.time()))
    f = open(log_path, 'w')

    if exits:
        for dirName, subDirs, fileList in os.walk(path):
            print("Current folder is:" + dirName)
            for filen in fileList:
                path = os.path.join(dirName, filen)
                file_hash = hashfile(path)
                icnt=icnt+1
                if file_hash in dups:
                    dicnt=dicnt+1
                    dups[file_hash].append(path)
                    #print("Append")
                else:
                    dups[file_hash] = [path]
                    #print("ADDDD")

        f.write(dups+"\n")
        f.write("\n")
        f.close()
        return dups
    else:
        print("Invalid Path")


def hashfile(path, blocksize=1024):
    try:
        afile = open(path, 'rb')
        # print("PATH HH::::",path)
        hasher = hashlib.md5()

        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
        # print("BUF   " + )
        afile.close()
        return hasher.hexdigest()
    except PermissionError as E:
        print(E)
    except Exception as EX:
        print(EX)

def DeleteFiles(dict1):
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    icnt = 0
    if len(results) > 0:
        for result in results:
            #print("$$$result:::",result)
            for subresult in result:

                icnt += 1
                if icnt >= 2:
                    os.remove(subresult)
            icnt = 0
    else:
        print("No duplicates files found.")

    connected = is_connected()

    if connected:
        starttime = time.time()
        MailSender(log_path, toaddr)
        endtime = time.time()

        print('Took %s seconds to send mail' % (endtime - starttime))
