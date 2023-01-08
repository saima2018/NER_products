from flask import Flask, url_for
from flask import request
from bert_base.client import BertClient
import re

app = Flask(__name__)

@app.route('/')
def hello():
    # show the user profile for that user
    return 'hello mundo'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<path:scope>')
def extractProduct(scope):
    """
    使用服务器上的BERT服务，给经营范围文本标注产品标签
    :param scope: 经营范围文本
    :return:
    """
    # 指定服务器的IP
    with BertClient(ip='192.168.3.3', show_server_config=False,
                    check_version=False, check_length=False, mode='NER', port=5555, port_out=5556) as bc:
        scope = re.sub(u'\\（.*?\\）|\\（.*$', '', scope)
        rst = bc.encode([scope])
        rst = rst[0]

    # 从标注好的经营范围文本中提取产品
    start_index = 0
    start_flag = False
    end_index = 0
    out_list = []

    for i in range(len(rst)):
        if rst[i] in ['B-PROD', 'I-PROD']:
            if not start_flag:
                start_index = i
                start_flag = True
        elif start_flag:
            end_index = i
            term = scope[start_index: end_index]
            product = ''.join(term)
            out_list.append(product)
            start_flag = False
    products = ';'.join(out_list)
    print(products)
    return products


if __name__ == '__main__':
    app.debug = True
    app.run(host='192.168.3.3')

