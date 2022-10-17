import os

from flask import Flask, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.route("/perform_query", methods=['GET'])
def perform_query():
    list_of_new = request.args
    try:
        file_name = list_of_new['file_name']
        func_list = [list_of_new['cmd1'], list_of_new['cmd2']]
        value_list = [list_of_new['value1'], list_of_new['value2']]
        req_dict = dict(zip(func_list, value_list))
    except:
        return 'Передан неверный параметр', 400

    try:
        open(DATA_DIR + "/" + file_name).readlines()
    except FileNotFoundError as e:
        return 'Передан неверный файл'

    with open(DATA_DIR + "/" + file_name) as f:
        file_data = f.read()
        file_data = [item for item in file_data.split('\n')]
        del file_data[-1]
        if 'filter' in req_dict.keys():
            file_data = [item for item in file_data if req_dict.get('filter') in item]
        if 'map' in req_dict.keys():
            boo = list(map(lambda v: v.split(), file_data))
            file_data = [i[int(req_dict.get('map'))] for i in boo]
        if 'unique' in req_dict.keys():
            file_data = list(set(file_data))
        if 'sort' in req_dict.keys():
            if req_dict.get('sort') == 'asc':
                file_data = sorted(file_data)
            else:
                file_data = sorted(file_data, reverse=True)
        if 'limit' in req_dict.keys():
            file_data = file_data[:int(req_dict.get('limit'))]
        return file_data


if __name__ == "__main__":
    app.run()