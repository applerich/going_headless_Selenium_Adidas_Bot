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




URLlookup = "https://www.adidas.ch/de/"

sitekey = "6LdC0iQUAAAAAOYmRv34KSLDe-7DmQrUSYJH8eB_"

testing = False
instances = 5
sizecode = "620"
sku = ["BY9913","BY9913"]
hmacname = "geecs"
dir_path = os.path.dirname(os.path.realpath(__file__))



def startbot(instancenum, skuinstance):
    cookies_list = "Null"
    baypassed = False
    chrome_options = Options()
    if testing is False:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("Accept-Encoding=gzip, deflate")
    chrome_options.add_argument("Accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
    chrome_options.add_argument("Accept-Language=en-GB,en-US;q=0.9,en;q=0.8")
    chrome_options.add_argument("Upgrade-Insecure-Requests=1")
    if testing is True:
        chrome_options.add_extension('extensions/edit_this_cookie.crx')
    proxy = "127.0.0.1"
    #chrome_options.add_argument('--proxy-server=%s' % PROXY)

    chrome_options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36")
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=chrome_options)
    driver.get(URLlookup+skuinstance+".html")
    print(str(datetime.now())+" - ["+str(instancenum)+"]" + " Product page Loading. SKU: "+skuinstance+". " +str(threading.current_thread().name))

    while baypassed is False:
        
        cookies_list = driver.get_cookies()
        
        
        cookies_dict = {}
        for cookie in cookies_list:
            cookies_dict[cookie['name']] = cookie['value']
            
            if hmacname in cookie['name']:
                baypassed = True
                print(" ")
                print(str(datetime.now())+" - ["+str(instancenum)+"]" + "Hmac found..." )
                print ("Name: ")
                print (cookie['name'])
                print ("Value: ")
                print (cookie['value'])
        


        if "reCaptchaSiteKey" in driver.page_source:
            print(str(datetime.now())+" - ["+str(instancenum)+"]" + " SiteKey found..." )
            baypassed = True
        time.sleep(10)
    if baypassed is True:
        
        print(bcolors.OKBLUE + str(datetime.now())+" - ["+str(instancenum)+"] - " + "Splash Bypass/Ready to cart..." + bcolors.ENDC)
        
        
        
        
        openseission(skuinstance=skuinstance, instancenum=instancenum, proxy=proxy, cookies_list=cookies_list)
        driver.close()


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
                
                onlyfiles = next(os.walk("recaptcharesponse"))[2]
        except Exception:
            if responses != responsestemp: 
                print(str(datetime.now())+ " - " + "0 g-recaptcha-responses remaining")
                responsestemp = responses

    
        time.sleep(5)

def makeinject(skuinstance, instancenum):
    recentcaptcha = "null"
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

    #injectionkeypt1 =  '(function(){ var f = document.createElement("form"); f.setAttribute("id","destroyer"); f.setAttribute("method","post"); f.setAttribute("action","http://www.adidas.ch/on/demandware.store/Sites-adidas-CH-Site/default/Cart-MiniAddProduct?clientId=c1f3632f-6d3a-43f4-9987-9de920731dcb"); var masterPid = document.createElement("input"); masterPid.setAttribute("type","hidden"); masterPid.setAttribute("name","masterPid"); masterPid.setAttribute("value","'+skuinstance+'"); var pid = document.createElement("input"); pid.setAttribute("type","hidden"); pid.setAttribute("name","pid"); pid.setAttribute("value","'+skuinstance+"_"+sizecode+'"); var ajaxOption = document.createElement("input"); ajaxOption.setAttribute("type","hidden"); ajaxOption.setAttribute("name","ajax"); ajaxOption.setAttribute("value","true"); var responseOption = document.createElement("input"); responseOption.setAttribute("type","hidden"); responseOption.setAttribute("name","layer"); responseOption.setAttribu'
    #injectionkeypt15 ='te("value",'
    #injectionkeypt2 = '"Add To Bag overlay"); var quantity = document.createElement("input"); quantity.setAttribute("type","hidden"); quantity.setAttribute("name","Quantity"); quantity.setAttribute("value","1"); var sessionSelectedStoreID = document.createElement("input"); sessionSelectedStoreID.setAttribute("type","hidden"); sessionSelectedStoreID.setAttribute("name","sessionSelectedStoreID"); sessionSelectedStoreID.setAttribute("value","null"); var captchaToken = document.createElement("input"); captchaToken.setAttribute("type","hidden"); captchaToken.setAttribute("name","g-recaptcha-response"); captchaToken.setAttribute("value","'+recentcaptcha+'"); f.appendChild(captchaToken); var captchaDuplicate = document.createElement("input"); captchaDuplicate.setAttribute("type","hidden"); captchaDuplicate.setAttribute("name","x-PrdRt"); captchaDuplicate.setAttribute("value","'+recentcaptcha+'"); f.appendChild(captchaDuplicate); var s = document.createElement("input"); s.setAttribute("type",'

    #injectionkeypt3 = '"submit"); s.setAttribute("value","Submit"); f.appendChild(masterPid); f.appendChild(pid); f.appendChild(ajaxOption); f.appendChild(responseOption); f.appendChild(quantity); f.appendChild(sessionSelectedStoreID); f.appendChild(s); document.getElementsByTagName("body")[0].appendChild(f); })(); document.getElementById(document.querySelector("[id^='+"'destroyer'"+']").id).submit();'
    #injectionkey = injectionkeypt1 + injectionkeypt15 + injectionkeypt2 + injectionkeypt3
    #name = "injection/"+str(datetime.now())+".txt"
    #f = open(name,'w')
    #f.write(injectionkey)
    #f.close()
    return(recentcaptcha)

def openseission(skuinstance, instancenum, cookies_list, proxy):
    recentcaptcha = str(makeinject(skuinstance=skuinstance, instancenum=instancenum))

    chrome_optionsaccount = Options()
    chrome_optionsaccount.add_argument("Accept-Encoding=gzip, deflate, br")
    chrome_optionsaccount.add_argument("Referer=https://www.adidas.ch/on/demandware.store/Sites-adidas-CH-Site/de_CH/Account-Show")
    chrome_optionsaccount.add_argument("Accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
    chrome_optionsaccount.add_argument("Accept-Language=en-GB,en-US;q=0.9,en;q=0.8")
    chrome_optionsaccount.add_argument("Upgrade-Insecure-Requests=1")
    chrome_optionsaccount.add_argument("Content-Type=application/x-www-form-urlencoded")
    chrome_optionsaccount.add_argument("Origin=null")
            #chrome_optionsopen.add_extension('extensions/edit_this_cookie.crx')
    chrome_optionsaccount.add_argument('--ignore-certificate-errors')
    PROXY = "127.0.0.1:80"
            #chrome_options.add_argument('--proxy-server=%s' % PROXY)
    chrome_optionsaccount.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
    chrome_optionsaccount.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36")
    driverload = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=chrome_optionsaccount)
    driverload.delete_all_cookies()
    
    driverload.get("https://www.adidas.ch/on/demandware.store/Sites-adidas-CH-Site/de_CH/Account-Show") 
    for cookie in reversed(cookies_list):
        if hmacname in cookie['name']:
            driverload.add_cookie(cookie)

    driverload.get("https://www.adidas.ch/on/demandware.store/Sites-adidas-CH-Site/de_CH/Account-Show")
    
    try:
        driverload.execute_script('$("h2").append(" <h2><strong>CARTING: '+skuinstance+' SIZE: '+sizecode+'</strong></h2>"); $("ul").remove();')
    except Exception:
        x = 1
    
        
    currenturl = driverload.current_url
   
    currenturltemp = driverload.current_url
   
    signingin = True 
    while signingin:
        if currenturl in currenturltemp:
            currenturltemp = driverload.current_url
           
        else:
            signingin = False
    
    
    
    
     
       
    driverload.get("file://"+dir_path+"/injector.html?"+skuinstance+"?"+skuinstance+"_"+sizecode+"?"+recentcaptcha)
    
    
       
            
    
   
    if "INVALID_CAPTCHA" in driverload.page_source:
        print(bcolors.FAIL + str(datetime.now())+" - ["+str(instancenum)+"] - " +"Captcha error. Could not cart..." + bcolors.ENDC)
    elif "minicart_overlay" in driverload.page_source:
        print(bcolors.GREENHL + str(datetime.now())+" - ["+str(instancenum)+"] - " +"Item has been carted..." + bcolors.ENDC)
        

    #driverload.execute_script( 'javascript:(function(){ var code=prompt("Enter the injection Code","Code"); eval(code); })();')
    #process = subprocess.Popen(
        #'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    #process.communicate(toinject.encode('utf-8'))
    #from selenium.webdriver.common.by import By
    #from selenium.webdriver.support.ui import WebDriverWait
    #from selenium.webdriver.support import expected_conditions as EC
    #wait = WebDriverWait(driverload, 10)
    #wait.until(EC.title_contains("adidas"))
    #blankt = "null"
    #process.communicate(blankt.encode('utf-8'))
    
 
    
    

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

skulenth = len(sku)
sku = sku * instances 
if __name__ == '__main__':
    Thread(target = recaptchacheck).start()
    harvestTokens()
    x = 0
    while x < instances * skulenth:
            
        Thread(target = startbot, args=(x,sku[x])).start()
        x = x + 1
print(str(datetime.now())+" - " + "Starting carting process for " + str(len(sku)) + " items")
if testing is True:
    print("Dev mode is: " + str(testing))
