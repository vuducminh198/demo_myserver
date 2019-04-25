from flask import Flask, json
from ev import _get_json, has_json, _json, SECRET_KEY, _no_data, _error_system
import jwt
from flask_cors import CORS
import hashlib, urllib, requests
import os

os.system('title TOMATO - connect!')
app = Flask(__name__)
CORS(app)


def get_facebook_token(username, password):
    secret_key = '62f8ce9f74b12f84c123cc23437a4a32'
    post_data = {
        'api_key': '882a8490361da98702bf97a021ddc14d',
        'email': username,
        'format': 'JSON',
        'locale': 'vi_vn',
        'method': 'auth.login',
        'password': password,
        'return_ssl_resources': '0',
        'v': '1.0'
    }
    s_data = ''
    for key in post_data.keys():
        s_data += '{}={}'.format(key, post_data[key])
    s_data += secret_key
    sig = hashlib.md5(str(s_data).encode('utf-8')).hexdigest()

    url_string = 'https://api.facebook.com/restserver.php?'

    post_data = {
        'api_key': '882a8490361da98702bf97a021ddc14d',
        'email': urllib.parse.quote_plus(username),
        'format': 'JSON',
        'locale': 'vi_vn',
        'method': 'auth.login',
        'password': urllib.parse.quote_plus(password),
        'return_ssl_resources': '0',
        'v': '1.0',
        'sig': sig
    }
    for key in post_data.keys():
        url_string += '&{}={}'.format(key, post_data[key])
    try:
        req = requests.get(url_string, headers={})
        return req.json()
    except Exception as error:
        return None


@app.route('/get-fb-token', methods=['POST'])
def get_token():
    try:
        if has_json('var_code'):
            var_code = _get_json('var_code')
            try:
                value = jwt.decode(var_code, SECRET_KEY, algorithms=['HS256'])
                data_json = dict(value)
                resp_data = get_facebook_token(data_json['username'], data_json['password'])
                return _json(code=200, data={
                    'error': 0,
                    'message': 'Connect done!',
                    'data': resp_data
                })
            except Exception as error:
                return _json(code=400, data={
                    'error': 1,
                    'message': 'Lỗi dữ liệu'
                })
        else:
            return _no_data()
    except Exception as error:
        return _error_system()


app.run(debug=True, host='0.0.0.0', port='1168')
