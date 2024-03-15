import sys,os,platform
import getpass
import firebase_admin
import datetime
import subprocess
from firebase_admin import credentials, storage , firestore
from datetime import date
from colorama import Fore
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
color = True
machine=sys.platform
checkplatform=platform.platform()
if machine.lower().startswith(('os', 'win', 'darwin', 'ios')):
    color=False
if checkplatform.startswith("Windows-10") and int(platform.version().split(".")[2]) >= 10586:
    color = True
    os.system('')
if not color:
    c_white   = Fore.WHITE
    c_green   = Fore.GREEN
    c_red     = Fore.RED
    c_yellow  = Fore.YELLOW
    c_blue    = Fore.BLUE
    purple    = Fore.GREEN
    cyan      = Fore.CYAN 
    violate   = Fore.YELLOW
    nc        = Fore.YELLOW
else:
    c_white, c_green, c_red, c_yellow, c_blue,purple , cyan, violate,nc = '\033[97m', '\033[92m', '\033[91m', '\033[93m', '\033[94m' ,'\033[1;35m' ,'\033[1;36m' ,'\033[1;37m' ,'nc="\033[00m"'
jsondata = {
    "type": "service_account",
    "project_id": "spacex-server-fb",
    "private_key_id": "8b6fa68d96fd81d0c8e48119499116a34728c362",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCja+tNfDoo7wD0\nEQcPAynyMW/XlHFXFVoFtVSEqSF6Kp4g7aKBk/Yx/eGzAMKo6eMm92rXd0lVNFR2\n/WUPCGw4EImSLckOmOSM4n7IfW+PzM+KPC8vUvD6gQqsalaSa+5AH4SX0mKpk+sS\nMMRg1LR304/qPjKKNOC3lUTdnjj7ObZZnkHxtRLUNS/VuJ6rs58/4X27ofbYJmXu\ndLNu8qUMnyaX3oK6hRdEMdFHudhxJAUTHq5S4VxRUS6PU5TSdpdamltYsG5nK2zh\nx8FpV0iUz/bEYnWWU2YICx+bzrU/xZi/4AeF6hNYP3jIpS78+OtddXuOo6pvY6Fh\n/i+AeMDjAgMBAAECggEAILQJC6GPlf92RmFd80Aj1cbU5eRb5hxsvnWyKzYZb/Q1\nXsuPWLT+cLSoxQSi7+CWR4b9x46kizuEp6c/4QlDdtjAXxNwh85K9nKhAogvmixX\nYAd5PdQwS0ElnKlPF9AnhoeIJkXA3sSuJx7BPctzLgOVaj/2Jzg7vCFP/bWbG5L4\nJLzo6v7I6GFcbeSZFcJMzRTgqIkumy9Am4KAmNTydo0Ooe+QDzxhq8sURleYPuet\nw3gzAinGDTWgCUvN/mPzBoKuNse0Xx00kzcZafD4s/X2uIFjVscRT2yPGw4J3AOF\nCyl3b1jxwYjNZ+ImXt8Slr/wdUWMZlqoh0bVuQ+42QKBgQDTkugCQF3YDev0/alj\n6X+AYy4nXt6LQdfzytI5uHEvAnwQjD5B6BkynF8oyq9hYRkqB4yeUYGnQ3+95wFG\nVkt6mXd3a9/Ez9de3c0oL9J5BEPbKVm6tJz8OPyGwfnn6xOp/3S1NqRT6axVrCmh\nibqMQNKOrymX59kJkGJqw0tJnwKBgQDFvJmFyiLwOdFJEZ9S6r0FNLOJoeKwHQig\n0LaPHpLi6Q+GG5bYR1rftrOj36MY3uS4gxcKW2wUGGxw0LDzngk81fMwkdXuB88I\n1apIUKRciWjckUqrnTXQ9eJV8fRn8eEXR9YkDT/ozeDTkyuxWKs0Ow6mbCebvCBK\nmbJ4SFgKPQKBgQCS2+9F2M4LMaauuQDChIrnYHDiDT0mpr6yz/9a54dRHUVm6yIv\n916+PcLj+sUAMDkaboESR/taUkUyWU4ON8pOwIYnk+6Qm8Cgbg+BLKjJLce4MhzB\nt6scfKX1GGJStF9C6jplqxcn1BS2pzmCkqq1vi0ps7aIZfvGYr2d5A+3ewKBgQCQ\ndmGTJUKxTwxf3cgQw/6ktwQUIXmEQTH0i4dUuHmH3c3BpJZoHHl/x/MmXlTB7tYb\nF2rV3kTvyYgwQ8eDtIn7MDQj3+fzpzDSu4dUndX25Uz/GAb9qjWPHJTnRYXSCxzv\n7UO9wxBV/VOsP3FEeAtcdWkWnR2y4ZaV6gRBbFkl4QKBgAffdtZp7gRE9QyLie5z\ntf17Qba3g+PqxA7mjA1k+bITQGQYUCvSAicIyGXtTzHgWXd1loAHka5YHjAswYzD\nwUuDZORyAlwruMhtVqLQLeSQke1ugZPlh+xehEj+xS5aA1hqsOD3uLFbO1NeXMLb\nAi8gIlqQO+MS8FV4vuTtQl5b\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-l7eug@spacex-server-fb.iam.gserviceaccount.com",
    "client_id": "115754266220757424537",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-l7eug%40spacex-server-fb.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}
cred = credentials.Certificate(jsondata)
firebase_admin.initialize_app(cred, {'storageBucket': 'spacex-server-fb.appspot.com'})
def Script_insurance(FSName):
    db   = firestore.client()
    uuid = str(subprocess.check_output('wmic csproduct get uuid'))
    uuid = uuid[uuid.find("\\n")+2:-15]
    myusername = str(getpass.getuser())
    MySerialNumber = f"{uuid}|{myusername}"
    #input(MySerialNumber)
    today = date.today() 
    day_name = today.strftime("%d/%m/%Y")
    timex = datetime.datetime.now()
    time_nowF = timex.strftime("%I:%M %p")
    active = False
    ex_client = False
    collection , document = str(FSName).replace('.py','').replace('.pyc','').replace('.exe','').split('_')
    collection = u''+str(collection)
    document = u''+str(document)
    usersref = db.collection(collection).document(document)
    users = usersref.get().to_dict()
    if users == None:
        users = {}
        num = 0
    else:
        for user in users:
            data = users[user]
            user_active = data['active']
            user_SerialNumber = data['SerialNumber']
            username = data['username']
            if MySerialNumber == user_SerialNumber and myusername == username:
                ex_client = True
                if user_active == 1:
                    name = data['name']
                    active = True
                    break
                else:      
                    active = False 
                    break   
            else:
                active = False
        num = 0
        for user in users: 
            num = num + 1
    if ex_client == False or num == 0:
        id_n = u'id_'+str(num+1)
        print("")
        print(Fore.YELLOW+"====="+Fore.BLUE+">>"+Fore.GREEN+f" Welcom To Script{c_blue}(SpaceX_RM){c_white}...... :")
        print("")
        namei = input(f' {c_blue}[+] {c_green}Enter your real {c_yellow}Name{c_white}: ')
        name = u''+str(namei) 
        username = u''+str(getpass.getuser())
        if '@RX' in str(namei):
            active = int(1)
        else:
            active = int(0)
        # القيم اللي بدك تبعتها
        users[id_n] = {'name':name,'username':username,'SerialNumber':MySerialNumber,'active':active,'day':day_name,'time':time_nowF}
        usersref.set(users)
        print(f''' 
            {c_red}Warning, {c_yellow}After pressing the Enter button,
            do not run the script until after you activate your device 
            by contacting us, or it will be self-delete{c_white}
        ''')
        print()
        input(f' {c_blue}[*] {c_green}Now you must contact us to {c_yellow}Activate {c_green}your device{c_white}: ')
        quit()
    if active == True:
        FSName    = f"Server_{FSName}"
        bucket    = storage.bucket()
        blob      = bucket.blob(FSName)
        code = blob.download_as_string()
        code = code.decode()
        if getattr(sys, 'frozen', False):
            code = code.replace('from playwright.sync_api import sync_playwright','#').replace('from SpaceXRM.MySelenium import SpaceXSelenium','#').replace('from SpaceXRM.MyRequests import SpaceXRequests','#').replace('from SpaceXRM.MySettings import *','#')
        code = str.encode(code)
        return code 
    else:
        print(11111111111111)
        quit()

# def getScriptFromServer(FSName):
#     FSName = f"Server_{FSName}"
#     bucket    = storage.bucket()
#     blob      = bucket.blob(FSName)
#     reqText = blob.download_as_text()
#     return reqText
# try:
#     #exec(getScriptFromServer(FSName))
# except:
#     pass