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


def is_connected():
    try:
        urllib3.connectionpool.connection_from_url('http://216.58.192.142 ', timeout=1)
        # urllib3.connection_from_url('https://www.google.com/ ',timeout=1)   #https://www.google.com/   #http://216.58.192.142
        return True
    except urllib3.URLError as err:
        return False


def MailSender(filname, stime, icnt, dicnt, toaddr):
    #MailSender(log_path, time, icnt, dicnt, toaddr)
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
                       Starting time of scanning = %s
                       Total number of files scanned = %s
                       Total number of duplicate files found = %s

                       This is auto generated mail.

                Thanks and Regards,
                Gauri Botre
                """ % (toaddr, time, stime, icnt, dicnt)

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


def findDup(dir, toaddr):
    sttime=time.time()
    icnt=0
    dicnt=0
    flag = os.path.isabs(dir)

    if flag == False:
        dir = os.path.abspath(dir)
    exits = os.path.isdir(dir)
    dups = {}
    if exits:
        for dirName, subDirs, fileList in os.walk(dir):
            print("Current folder is:" + dirName)
            for filen in fileList:
                dir = os.path.join(dirName, filen)
                file_hash = hashfile(dir)
                icnt=icnt+1
                if file_hash in dups:
                    dicnt=dicnt+1
                    dups[file_hash].append(dir)
                    #print("Append")
                else:
                    dups[file_hash] = [dir]
                    #print("ADDDD")
        DeleteFiles(dups, sttime, icnt, dicnt, toaddr)
        # return dups
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

def DeleteFiles(dict1,sttime, ficnt, dicnt, toaddr):
    #DeleteFiles(dups, sttime, icnt, dicnt, toaddr)
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    icnt = 0
    file="log"
    if len(results) > 0:
        log_path = os.path.join(file, " file %s.log" % (time.time()))
        f = open(log_path, 'w')

        for result in results:
            #print("$$$result:::",result)
            for subresult in result:
                f.write(subresult + "\n")
                f.write("\n")
                icnt += 1
                if icnt >= 2:
                    os.remove(subresult)
            icnt = 0
        f.close()
    else:
        print("No duplicates files found.")




    connected = is_connected()

    if connected:
        starttime = time.time()
        MailSender(log_path,sttime, ficnt, dicnt, toaddr)
        endtime = time.time()

        print('Took %s seconds to send mail' % (endtime - starttime))
