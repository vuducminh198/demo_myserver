from datetime import datetime
from functools import wraps
import os
import time
import jwt
from flask import request, Response, json
from datetime import timedelta
import platform

if str(platform.system()).lower().__ne__('windows'):
    try:
        os.environ['TZ'] = 'Asia/Ho_Chi_Minh'
        time.tzset()
    except Exception as error:
        pass

# mongoengine.connect(db='mipee', host='mongodb://localhost:27017/')


SECRET_KEY = 'TOMATO_!@#axn'

evaluation_day = 1


def toUTC(time):
    return datetime.strftime(time, "%Y-%m-%d %H:%M:%S")


def decorator_function_with_arguments(arg1):
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            f(*args, **kwargs)

        return wrapped_f

    return wrap


def _json(code: object, data: object) -> object:
    return Response(status=code, mimetype='application/json', response=json.dumps(data))


def _no_data_p(param: str):
    return _json(code=400, data={
        'error': 1,
        'message': 'Thiếu tham số {}, vui lòng kiểm tra và thử lại sau!'.format(param)
    })


def _no_data():
    return _json(code=400, data={
        'error': 1,
        'message': 'Thiếu tham số cần thiết, vui lòng kiểm tra và thử lại sau!'
    })


def _result_exists(string_data):
    return _json(code=400, data={
        'error': 1,
        'message': '{} đã tồn tại vui lòng kiểm tra và thử lại sau'.format(string_data)
    })


def _result_no_exists(string_data):
    return _json(code=400, data={
        'error': 1,
        'message': '{} không tồn tại vui lòng kiểm tra và thử lại sau'.format(string_data)
    })


def _error_system():
    return _json(code=400, data={
        'error': 1,
        'message': 'Tham số định dạng không đúng, vui lòng kiểm tra và thử lại sau!'
    })


def _get_param(property_x: object) -> object:
    return request.form.get(property_x)


def _get_json(property_x):
    if not (request.json is None):
        return request.json.get(property_x)
    else:
        return request.form.get(property_x)


def _get_json_list(property_x):
    property_name = '{}[]'.format(property_x)
    if not (request.json is None) and property_name in request.json:
        return request.json.getlist(property_name)
    else:
        return request.form.getlist(property_name)


def _get_args(property_x):
    return request.args.get(property_x)


def has_args(property_x):
    return property_x in request.args and len(request.args.get(property_x)) > 0


def has_json_list(property_x):
    if not (request.form is None):
        return property_x + '[]' in request.form and len(str(request.form.get(property_x + '[]'))) > 0
    if not (request.json is None):
        return property_x + '[]' in request.json and len(str(request.json.get(property_x + '[]'))) > 0
    return False


def has_json(propertyx):
    if not (request.json is None) and propertyx in request.json:
        return len(str(request.json.get(propertyx))) > 0
    if not (request.form is None) and propertyx in request.form:
        return len(str(request.form.get(propertyx))) > 0
    return False


def has_param(property):
    return property in request.form and len(request.form.get(property)) > 0


def len_param(property, length):
    return property in request.form and len(request.form.get(property)) >= length


def user_id_from_token():
    token_string = request.headers.get('Authorization')
    try:
        token_decode = jwt.decode(token_string, SECRET_KEY, algorithms=['HS256'])
        return token_decode['id']
    except Exception as error:
        return None


def _vietnam_time(time):
    return time + timedelta(hours=7)




# def admin_require(func):
#     @wraps(func)
#     def check_token(*args, **kwargs):
#         if 'Authorization' not in request.headers:
#             return _json(code=401, data={
#                 'error': 1,
#                 'message': 'Yêu cầu quyền hạn truy cập'
#             })
#         token_string = request.headers.get('Authorization')
#         try:
#             token_decode = jwt.decode(token_string, SECRET_KEY, algorithms=['HS256'])
#             admin_cols = AdminAccount.objects(username=token_decode['username'])
#             if len(admin_cols) is 0:
#                 return _json(code=401, data={
#                     'error': 1,
#                     'message': 'Tài khoản {} không tồn tại'.format(token_decode['username'])
#                 })
#             else:
#                 admin_current = admin_cols[0]
#                 if admin_current['password_at'].isoformat() != token_decode['password_at']:
#                     return _json(code=401, data={
#                         'error': 1,
#                         'message': 'Mật khẩu đã được thay đổi trước đó, vui lòng kiểm tra và thử lại sau!'
#                     })
#                 if str(admin_current['blocked']) == '1':
#                     return _json(code=401, data={
#                         'error': 1,
#                         'message': 'Tài khoản {} đang bị khóa, vui lòng kiểm tra và thử lại sau!'.format(
#                             token_decode['username'])
#                     })
#                 return func(*args, **kwargs)
#         except Exception as error:
#             print(error)
#             return _json(code=401, data={
#                 'error': 1,
#                 'message': 'Mã truy cập không hợp lệ, vui lòng kiểm tra lại'
#             })
#
#     return check_token


def timestamp(dt):
    return (dt - datetime(1970, 1, 1)).total_seconds()


def decode_token():
    token_string = request.headers.get('Authorization')
    try:
        token_decode = jwt.decode(token_string, SECRET_KEY, algorithms=['HS256'])
        return token_decode
    except Exception as error:
        return False


def get_token():
    return request.headers.get('Authorization')


msg = {
    "username_short": "Tên đăng nhập quá ngắn",
    "username_long": "Tên đăng nhập quá dài",
    "password_short": "Mật khẩu quá ngắn",
    "password_long": "Mật khẩu quá dài",
    "account_not_active": "Tài khoản chưa được kích hoạt",
    "account_blocked": "Tài khoản đang bị bị khóa",
    "name_short": "Tên người dùng quá ngắn",
    "name_long": "Tên người dùng quá ngắn"
}
