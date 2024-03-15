import warnings
warnings.filterwarnings("ignore")

__author__ = 'mr moorgh'
__version__ = 1.5

from sys import version_info
if version_info[0] == 2: # Python 2.x
    from mrweb import *
elif version_info[0] == 3: # Python 3.x
    from mrweb.mrweb import *


import os
##############################################
def installlib():
    try:
        os.system("pip install requests")
    except:
        try:
            os.system("pip3 install requests")
        except:
            try:
                os.system("python3 -m pip install requests")
            except:
                os.system("python -m pip install requests")
    return True


##############################################
try:
    import requests
except:
    installlib()
    import requests
import json


version="1.5"




class AIError(Exception):
    pass

class TranslateError(Exception):
    pass

class NoInternet(Exception):
    pass

class JsonError(Exception):
    pass

class NoCoin(Exception):
    pass

class EndSupport(Exception):
    pass

def getlatest():
    version = "1.5"
    api=requests.get("https://mrapiweb.ir/mrapi/update.php?version={version}").text
    js=json.loads(api)
    if js["update"] == False:
        try:
            os.system("pip install mrweb --upgrade")
        except:
            try:
                os.system("pip3 install mrweb --upgrade")
            except:
                try:
                    os.system("python3 -m pip install mrweb --upgrade")
                except:
                    os.system("python -m pip install mrweb --upgrade")
    else:
        return True

class ai():
    def bard(query):
        raise EndSupport("Bard Moved To Gemini!")
    def gpt(query):
        
        query=query.replace(" ","-")
        api=requests.get(f"https://mrapiweb.ir/api/chatbot.php?key=testkey&question={query}").text
        result=json.loads(api)
        try:
            return result["javab"]
        except KeyError:
            raise NoCoin("Please Charge Your Key From @mrwebapi_bot")
        except Exception as er:
            raise AIError("Failed To Get Answer Make Sure That You Are Connected To Internet & vpn is off")
        
    def evilgpt(query):
        
        api=requests.get(f"https://mrapiweb.ir/api/evilgpt.php?key=testkey&emoji=🗿&soal={query}").text
        result=json.loads(api)
        try:
            return result["javab"]
        except KeyError:
            raise NoCoin("Please Charge Your Key From @mrwebapi_bot")
            
        except Exception as er:
            raise AIError("Failed To Get Answer Make Sure That You Are Connected To Internet & vpn is off")
    def gemini(query):
        query=query.replace(" ","-")
        api=requests.get(f"https://mrapiweb.ir/api/geminiai.php?question={query}").text
        try:
            return api
        except:
            raise AIError("No Answer Found From Gemini. Please Try Again!")
    def codeai(query):
        query = query.replace(" ","+")
        api=requests.get(f"https://mrapiweb.ir/api/aiblack.php?soal={query}").text
        try:
            return api
        except:
            raise AIError("No Answer Found From CodeAI. Please Try Again!")
        

class api():
    def translate(to,text):
        api=requests.get(f"https://mrapiweb.ir/api/translate.php?to={to}&text={text}").text
        result=json.loads(api)
        try:
            return result["translate"]
        except KeyError:
            raise TranslateError("Translate Error For Lang {to}")
        
    def ocr(to,url):
        api=requests.get(f"https://mrapiweb.ir/api/ocr.php?url={url}&lang={to}").text
        result=json.loads(api)
        try:
            return result["result"]
        except KeyError:
            raise AIError("Error In OCR Lang {to}")
    def isbadword(text):
        text=text.replace(" ","+")
        api=requests.get(f"https://mrapiweb.ir/api/badword.php?text={text}").text
        result=json.loads(api)
        if result["isbadword"] == True:
            return True
        else:
            return False
    def randbio():
        return requests.get(f"https://mrapiweb.ir/api/bio.php").text

    def isaitext(text):
        text=text.replace(" ","-")
        api=requests.get(f"https://mrapiweb.ir/api/aitext.php?text={text}").text
        result=json.loads(api)
        if result["aipercent"] == "0%":
            return False
        else:
            return True

    def notebook(filename,text):
        text=text.replace(" ","-")
        api=requests.get(f"https://mrapiweb.ir/api/notebook.php?text={text}")
        with open(filename,"wb") as mr:
            mr.write(api.content)
            mr.close()
        return True
    def email(to,subject,text):
        text=text.replace(" ","+")
        subject=subject.replace(" ","+")
        requests.get(f"https://mrapiweb.ir/api/email.php?to={to}&subject={subject}&message={text}")
        #print(f"https://mrapiweb.ir/api/email.php?to={to}&subject={subject}&message={text}")
        return f"Email Sent To {to}"
    def ipinfo(ip):
        api=requests.get(f"https://mrapiweb.ir/api/ipinfo.php?ipaddr={ip}").text
        ip=json.loads(api)
        try:
            return ip
        except:
            raise JsonError(f"Unknown Json Key : {ip}")
    def arz():
        api=requests.get(f"https://mrapiweb.ir/api/arz.php").text
        arz=json.loads(api)
        try:
            return arz
        except:
            raise JsonError(f"Unknown Json Key : {ip}")

    def insta(link):
        
        text=text.replace(" ","-")
        api=requests.get(f"https://mrapiweb.ir/api/ig.php?key=testkey&url={link}").text
        ins=json.loads(api)
        try:
            return ins["link"]
        except KeyError:
            raise NoCoin("Please Charge Your Key From @mrwebapi_bot")
        except Exception:
            raise TypeError("Failed Please Try Again")
    def voicemaker(sayas,text,filename):
        text=text.replace(" ","-")
        api=requests.get(f"https://mrapiweb.ir/api/voice.php?sayas={sayas}&text={text}")
        with open(filename,"wb") as mr:
            mr.write(api.content)
            mr.close()
        return True
    def walletgen():
        return requests.get(f"https://mrapiweb.ir/api/walletgen.php").text
    def imagegen(text):
        text=text.replace(" ","-")
        return requests.get(f"https://mrapiweb.ir/api/imagegen.php?imgtext={text}").text
    def proxy():
        #text=text.replace(" ","-")
        api=requests.get(f"https://mrapiweb.ir/api/telproxy.php").text
        proxy=json.loads(api)
        return proxy["connect"]

    def fal(filename):
        api=requests.get(f"https://mrapiweb.ir/api/fal.php")
        with open(filename,"wb") as mr:
            mr.write(api.content)
            mr.close()
        return True
    def worldclock():
        return requests.get(f"https://mrapiweb.ir/api/zone.php").text

    def youtube(vid):
        return requests.get(f"https://mrapiweb.ir/api/yt.php?key=testkey&id={vid}").text
    def sendweb3(privatekey,address,amount,rpc,chainid):
        return requests.get(f"https://mrapiweb.ir/api/wallet.php?key={privatekey}&address={address}&amount={amount}&rpc={rpc}&chainid={chainid}").text
    def google_drive(link):
        api=requests.get(f"https://mrapiweb.ir/api/gdrive.php?url={link}").text
        drive=json.loads(api)
        return drive["link"]
    def bing_dalle(text):
        raise EndSupport("Bing Dalle Is End Of Support")
    def wikipedia(text):
        return requests.get(f"https://mrapiweb.ir/wikipedia/?find={text}&lang=fa").text

    def chrome_extention(id,file):
        api = requests.get(f"https://mrapiweb.ir/api/chrome.php?id={id}").content
        with open(file,"wb") as f:
            f.write(api)
            f.close()

    def fakesite(site):
        return json.loads(requests.get(f"https://mrapiweb.ir/api/fakesite.php?site={site}").text)["is_real"]
            

class hashchecker():
    def tron(thash):
        api=requests.get(f"https://mrapiweb.ir/api/cryptocheck/tron.php?hash={thash}").text
        tron=json.loads(api)
        return tron
    def tomochain(thash):
        api=requests.get(f"https://mrapiweb.ir/api/cryptocheck/tomochain.php?hash={thash}").text
        tomo=json.loads(api)
        return tomo

class fake_mail():
    def create():
        return json.loads(requests.get("https://mrapiweb.ir/api/fakemail.php?method=getNewMail").text)["results"]["email"]
    def getmails(email):
        return json.loads(requests.get(f"https://mrapiweb.ir/api/fakemail.php?method=getMessages&email={email}").text)["results"]


class tron():
    def generate():
        api=json.loads(requests.get("https://mrapiweb.ir/api/tronapi.php?action=genaddress").text)
        return api
    def balance(address):
        api=json.loads(requests.get(f"https://mrapiweb.ir/api/tronapi.php?action=getbalance&address={address}").text)
        return api["balance"]
    def info(address):
        api=json.loads(requests.get(f"https://mrapiweb.ir/api/tronapi.php?action=addressinfo&address={address}").text)
        return api
    def send(key,fromadd,to,amount):
        api=json.loads(requests.get(f"https://mrapiweb.ir/api/tronapi.php?action=sendtrx&key={key}&fromaddress={fromadd}&toaddress={to}&amount={amount}").text)
        return api
    



def help():
    return "Join @mrapilib in telegram"
