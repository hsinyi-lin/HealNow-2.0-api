from flask import jsonify


def success_response(data=None, msg='成功', status_code=200):
    response_data = {'success': True}
    if data is not None:
        response_data['data'] = data
    if msg is not None:
        response_data['msg'] = msg
    return jsonify(response_data), status_code


def error_response(msg='缺少欄位', status_code=400):
    response_data = {'success': False}
    if msg is not None:
        response_data['msg'] = msg
    return jsonify(response_data), status_code
