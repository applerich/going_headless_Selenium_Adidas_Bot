import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import threading
import calendar
import subprocess
from threading import Thread
import glob
import os
from datetime import datetime
import webbrowser
from flask import Flask, render_template, request
import _thread
import logging
from datetime import datetime
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

baseurl = "https://www.adidas.ch/de/"
splashpage = "https://www.adidas.ch/de/BY9913.html"
Clientid = ""
sitekey = "6LdC0iQUAAAAAOYmRv34KSLDe-7DmQrUSYJH8eB_"
testing = False
instances = 2
sizecode = "620"
sku = ["BY9913", "BY9913", "BY9913"]
hmacname = "geecs"
dir_path = os.path.dirname(os.path.realpath(__file__))





chrome_options = Options()
chrome_options.add_argument("Accept-Encoding=gzip, deflate, br")
chrome_options.add_argument("Referer=https://www.adidas.ch/on/demandware.store/Sites-adidas-CH-Site/de_CH/Account-Show")
chrome_options.add_argument("Accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
chrome_options.add_argument("Accept-Language=en-GB,en-US;q=0.9,en;q=0.8")
chrome_options.add_argument("Upgrade-Insecure-Requests=1")
chrome_options.add_argument("Content-Type=application/x-www-form-urlencoded")
chrome_options.add_argument("Origin=null")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36")

def yeezysplash(instancenum, sku, proxy):
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=chrome_options)
    driver.get(splashpage)
    print(str(datetime.now())+" - ["+str(instancenum)+"]" + " - Product page Loading. SKU: "+str(sku)+". " +str(threading.current_thread().name))
    hmac = {
        "name" : "test",
        "value" : "test"
            }
    baypassed = False
    while baypassed is False:
        cookies_list = driver.get_cookies()
        cookies_dict = {}
        for cookie in cookies_list:
            cookies_dict[cookie['name']] = cookie['value']
            if hmacname in cookie['name']:
                baypassed = True
                hmac = cookie
                print (cookie)
        if "reCaptchaSiteKey" in driver.page_source:
            baypassed = True
        time.sleep(10)
    if baypassed is True:
        print(bcolors.OKBLUE + str(datetime.now())+" - ["+str(instancenum)+"] - " + "Splash Bypass/Ready to cart..." + bcolors.ENDC)
        cart(instancenum=instancenum, sku=sku, proxy=proxy, hmac=hmac)
        driver.close()
        
def cart(instancenum, sku, proxy, hmac):
    
    recentcaptcha = getcaptcha(instancenum=instancenum)
    chrome_options.arguments.remove("--headless")
    drivercart = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=chrome_options)
    drivercart.get("https://www.adidas.ch/on/demandware.store/Sites-adidas-CH-Site/de_CH/Account-Show")
    drivercart.add_cookie(hmac)
    drivercart.get("https://www.adidas.ch/on/demandware.store/Sites-adidas-CH-Site/de_CH/Account-Show")
    try:
        drivercart.execute_script('$("h2").append(" <h2><strong>CARTING: '+sku+' SIZE: '+sizecode+'</strong></h2>"); $("ul").remove();')
    except Exception:
        injected = True
    currenturl = drivercart.current_url
    currenturltemp = drivercart.current_url
    signingin = True 
    while signingin:
        if currenturl in currenturltemp:
            currenturltemp = drivercart.current_url
        else:
            signingin = False
    drivercart.get("file://"+dir_path+"/injector.html?"+str(sku)+"?"+str(sku)+"_"+str(sizecode)+"?"+str(recentcaptcha))
    if "INVALID_CAPTCHA" in drivercart.page_source:
        print(bcolors.FAIL + str(datetime.now())+" - ["+str(instancenum)+"] - " +"Captcha error. Could not cart..." + bcolors.ENDC)
    elif "minicart_overlay" in drivercart.page_source:
        print(bcolors.GREENHL + str(datetime.now())+" - ["+str(instancenum)+"] - " +"Item has been carted..." + bcolors.ENDC)

def getcaptcha(instancenum):
    failedinject = 0
    failedinjecttemp = 1
    t = True
    while t :
        try:
            files_path = os.path.join("recaptcharesponse", '*')
            files = sorted(
            glob.iglob(files_path), key=os.path.getctime, reverse=True)
            count = len(files)
            getresponse = open(str(files[count-1]), "r")
            recentcaptcha = getresponse.read()
            os.remove(files[count-1])
            print(bcolors.HEADER + str(datetime.now())+" - ["+str(instancenum)+"] - " +"Captcha token found, used to inject..."+bcolors.ENDC)
            print(str(datetime.now())+ " - " + str(count-1)+" g-recaptcha-responses remaining")
            t = False  
        except Exception:
            if failedinject != failedinjecttemp:
                print(bcolors.FAIL + str(datetime.now())+" - ["+str(instancenum)+"] - " +"No captcha Token, can not inject..." + bcolors.ENDC)
                failedinjecttemp = failedinject        
        time.sleep(5)
    return recentcaptcha

def recaptchacheck():
    responses = 0
    responsestemp = 0
    time.sleep(5)
    t = True
    while t :
        try:
            files_path = os.path.join("recaptcharesponse", '*')
            files = sorted(
                glob.iglob(files_path), key=os.path.getctime, reverse=True)
            count = len(files)
            secondssincecreated = calendar.timegm(time.gmtime()) - os.path.getmtime(str(files[count-1]))
            if secondssincecreated > 120:
                responses = responses - 1
                os.remove(files[count-1])
                print(str(datetime.now())+ " - " + str(len(onlyfiles)-1)+" g-recaptcha-responses remaining")
                print(files[count-1])
                onlyfiles = next(os.walk("recaptcharesponse"))[2]
        except Exception:
            if responses != responsestemp: 
                print(str(datetime.now())+ " - " + "0 g-recaptcha-responses remaining")
                responsestemp = responses    
        time.sleep(5)
        
tokens = []

def stamp():
    timestamp = str("["+datetime.utcnow().strftime("%H:%M:%S")+"]")
    return timestamp

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
@app.route('/', methods=['GET', 'POST'])
@app.route('/solve', methods=['GET', 'POST'])

def solve():
    if request.method == "POST":
            token = request.form.get('g-recaptcha-response', '')
            f = open("recaptcharesponse/"+str(datetime.now())+".txt",'w')
            f.write(token)
            f.close()
            tokens.append(token)
            count = len(tokens)
            onlyfiles = next(os.walk("recaptcharesponse"))[2]
            print(str(datetime.now())+ " - " + str(len(onlyfiles)-1)+ " g-recaptcha-responses have been harvested")
    return render_template('index.html', sitekey=sitekey)

def harvestTokens():
    _thread.start_new_thread(app.run, ())
    webbrowser.open("http://w.www.adidas.ch:5000/solve") # WEB ADDRESS FOR SOLVING CAPTCHA GOES HERE FAM
    return       
    

class bcolors:
    HEADER = '\033[95m'
    GREENHL = '\u001b[42m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    

if __name__ == '__main__':
    sku = sku * instances
    print(sku)
    Thread(target = recaptchacheck).start()
    harvestTokens()
    x = 0
    while x < instances * len(sku): 
        print (x)
        Thread(target = yeezysplash, args=(x,sku[x],"proxy")).start()
        x = x + 1
print(str(datetime.now())+" - " + "Starting carting process for " + str(len(sku)) + " items")


