import time,platform
import os,sys,subprocess
import datetime,math
import argparse
from colorama import Fore, Style

target = []
alreadyTarget = []
path = os.path.dirname(os.path.realpath(sys.argv[0])) + "/result"
osType = platform.system()


banner = '''
__  __       _         _      __  __                
\ \/ /      /_\  _   _| |_ ___\ \/ /_ __ __ _ _   _ 
 \  /_____ //_\\| | | | __/ _ \\  /| '__/ _` | | | |
 /  \_____/  _  \ |_| | || (_) /  \| | | (_| | |_| |
/_/\_\    \_/ \_/\__,_|\__\___/_/\_\_|  \__,_|\__, |
                                              |___/ 

                                    by 斯文
'''

def scan(url):

    global alreadyTarget
    nowTime = str(time.strftime('%H:%M:%S',time.localtime(time.time())))
    print(Fore.GREEN + "[{}] ".format(nowTime),end="")
    print(Style.RESET_ALL,end="")
    print("开始扫描目标 " + Fore.GREEN + "=>" + Style.RESET_ALL + " {}".format(url) + "\r")

    if 'http://' in url:
        name = url.replace('http://','')
    else:
        name = url.replace('https://','')

    result = name.split(':')
    result = result[0]
    result = result.replace('/','')
    try:
        if osType == "Windows":
            p = subprocess.check_output("15_xray webscan --browser-crawler {} --html-output {}/{}.html".format(url, path, result), shell=True, stdout=subprocess.PIPE) 
        else:
            p = subprocess.Popen("./15_xray webscan --browser-crawler {} --html-output {}/{}.html".format(url, path, result), shell=True, stdout=subprocess.PIPE) 
            # print('1')
        out, err = p.communicate()


    except KeyboardInterrupt:
        stop(target)
        return False

    alreadyTarget.append(url)
    

def stop(target):

    global alreadyTarget

    print("[+ 开始结算扫描进度" )

    with  open('已扫描.txt','w',encoding='utf-8') as w:
        for i in alreadyTarget:
            w.write( i + '\n')

    if len(target) != 0:
        with  open('未扫描.txt','w',encoding='utf-8') as w:
            for i in target:
                w.write( i + '\n')

        print("[+ scan success ! 请查看当前目录生成的txt了解扫描进度")


def main(file):

    global target
    global path
    
    if osType == "Windows":
        path.replace('\\','/')
    else:
        pass

    if not os.path.exists(path):
        os.makedirs(path)

    try:
        with open(file ,'r') as f:

            data = f.readlines()
            for i in data:
                url = i.strip('\n')
                target.append(url)

            print("[+ Hi, Wish you good luck!  本次扫描目标共{}个".format(len(target)) + '\n')

            for i in target.copy():
                speed = scan(i)
                if speed == False:
                    break
                target.remove(i)
            
    except KeyboardInterrupt:
        stop(target)

if __name__ == '__main__':

    if len(sys.argv) == 2:
        print(banner)
        main(sys.argv[1])
    else:
        print(banner + '''
Usage: 在Xray同目录下运行 python3 xxx.py xxxx.txt''')
