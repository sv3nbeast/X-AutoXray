import time,platform,requests
import os,sys,subprocess
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor,as_completed

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
    global target
    # init(autoreset=True)
    nowTime = str(time.strftime('%H:%M:%S',time.localtime(time.time())))
    print(Fore.GREEN + "[{}] ".format(nowTime),end="")
    print(Style.RESET_ALL,end="")
    print("开始扫描目标 " + Fore.GREEN + "=>" + Style.RESET_ALL + " {}".format(url) + "\r")

    url = getHTTP(url)

    if 'http://' in url:
        name = url.replace('http://','')
    else:
        name = url.replace('https://','')

    result = name.split(':')
    result = result[0]
    result = result.replace('/','')
    
    # print(url)
    fileName = checkFileName(result,nowTime)
    try:
        if osType == "Windows":
            p = subprocess.check_output("xray webscan --browser-crawler {} --html-output {}".format(url, fileName), shell=True) 
        else:
            p = subprocess.Popen("./xray webscan --browser-crawler {} --html-output {}".format(url, fileName), shell=True, stdout=subprocess.PIPE) 
            # out, err = p.communicate()

            pid = str(p.pid)
            starttime = time.time()
            nowtime = starttime
            while True:
                try:
                    #一直在循环里面运行 ret==None 的意思就是在运行。
                    ret = subprocess.Popen.poll(p)
                    # ret==0 代表程序正常结束。
                    if ret == 0:
                        break
                    #扫描超过15分钟就超时(这个后期多次实验后可以继续调优)
                    if(nowtime > starttime + 900):
                        os.system("pkill -TERM -P " + pid)
                        print(Fore.GREEN + "[{}] ".format(nowTime),end="")
                        print(" 目标 {} 扫描超过15分钟,已自行终结扫描进程".format(url))
                        break
                    nowtime = time.time()
                except Exception as e:
                    break
            target.remove(url)

    except KeyboardInterrupt:
        stop(target)
        return False

    alreadyTarget.append(url)

def getHTTP(url): #在给出的目标没有http前缀时，获得目标究竟是https还是http

    if 'http' not in url:
        try:
            lenHttp = len(requests.get('http://' + url,timeout=10).content)
        except:
            lenHttp = 0
            url = "https://" + url
        try:
            lenHttps = len(requests.get('https://' + url,timeout=10).content)
        except:
            lenHttps = 0
            url = "http://" + url

        if lenHttp == lenHttps or lenHttps > lenHttp:
            url = "https://" + url
        else:
            url = "http://" + url

    return url

def checkFileName(result,nowTime):

    if osType == 'Windows':
        nowTime = nowTime.replace(':','-')
        fileName = '{}\{}.html'.format(path,result)
    else:
        fileName = '{}/{}.html'.format(path,result)

    if not os.path.exists(fileName):
        pass
    else:
        if osType == 'Windows':
            fileName = '{}\{}.html'.format(path,'[' + nowTime + ']' + result)
        else:
             fileName = '{}/{}.html'.format(path,'[' + nowTime + ']' + result)
        print(Fore.GREEN + "[{}] ".format(nowTime),end="")
        print(Style.RESET_ALL,end="")
        print("检测到已存在{}.html文件 ".format(result) + Fore.GREEN + "=>" + Style.RESET_ALL + " 更改文件名为{}.html".format('[' + nowTime + ']' + result) + "\r")
    
    return fileName

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
        path = path.replace('/','\\')
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
            executor = ThreadPoolExecutor(max_workers=6)  # 设置线程池并发数量
            all_task = [executor.submit(scan, x.strip()) for x in data]
            for future in as_completed(all_task):
                data = future.result()

            # for i in target.copy():

            #     speed = scan(i)
            #     if speed == False:
            #         break
            #     target.remove(i)
            
    except KeyboardInterrupt:
        stop(target)

if __name__ == '__main__':

    if len(sys.argv) == 2:
        print(banner)
        main(sys.argv[1])
    else:
        print(banner + '''
Usage: 在Xray同目录下运行 python3 xxx.py xxxx.txt''')
