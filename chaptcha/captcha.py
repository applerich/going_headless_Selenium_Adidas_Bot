# captchaTing.py

from datetime import datetime
import webbrowser
from flask import Flask, render_template, request
import _thread
import logging
from datetime import datetime

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
    sitekey = "6LdC0iQUAAAAAOYmRv34KSLDe-7DmQrUSYJH8eB_" # SITEKEY GOES HERE FAM
    if request.method == "POST":
            token = request.form.get('g-recaptcha-response', '')
            f = open(str(datetime.now())+".txt",'w')
            f.write(token)
            f.close()
            tokens.append(token)
            count = len(tokens)
            print("{} stored token | {} total stored".format(stamp(), count))

    return render_template('index.html', sitekey=sitekey)

def harvestTokens():
    _thread.start_new_thread(app.run, ())
    webbrowser.open("http://w.www.adidas.ch:5000/solve") # WEB ADDRESS FOR SOLVING CAPTCHA GOES HERE FAM
    return

def main():
	print("captcha ting we out here")
	print("this shit was made by the real chef, cos he the real chef\n\n")
	harvestTokens()
	input("")

if __name__ == '__main__':
	main()
