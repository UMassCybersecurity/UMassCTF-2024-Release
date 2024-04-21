from flask import Flask, render_template, url_for, request, make_response, jsonify
import json, base64
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    headers = request.headers
    user_agent = True if headers.get('User-Agent') == 'Bikini Bottom' else False
    language = False
    date = False
    cookie = False
    log = False

    resp = make_response(render_template('cookie.html'))
    resp.set_cookie('Login', 'eyJsb2dnZWRpbiI6IGZhbHNlfQ==')
    if (request.cookies.get('Login')):
        temp = base64.b64decode(request.cookies.get('Login'))
        dn = json.loads(temp)
        if (dn['loggedin']) :
            log = True if dn['loggedin'] == True else False

    if (headers.get('Accept-Language')):
        language = True if 'fr' in headers.get('Accept-Language') else False
    if (headers.get('Date')):
        try:
            temp = datetime.strptime(headers.get('Date'), '%a, %d %b %Y %H:%M:%S %Z').strftime('%b/%d/%Y')
            print(temp, flush=True)
            date = True if "Jul/14/2024" in temp else False
        except Exception as e:
            return make_response("Make sure your format is correct (இ﹏இ`｡)")
    if (request.cookies.get('flavor')):
        cookie = True if request.cookies.get('flavor') == 'chocolate_chip' else False


    if user_agent and language and date and cookie and log:
        return render_template('flag.html')
    elif user_agent and language and date and cookie:
        return resp
    elif user_agent and language and date:
        return render_template('fourth.html')
    elif user_agent and date:
        return render_template('third.html')
    elif user_agent:
        return render_template('second.html')
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
