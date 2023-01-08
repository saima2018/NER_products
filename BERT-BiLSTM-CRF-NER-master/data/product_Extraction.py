# !/usr/bin/python3
# -*- coding: utf-8 -*-
import time
from bert_base.client import BertClient
import re

def extractProduct(scope):
    """
    使用服务器上的BERT服务，给经营范围文本标注产品标签
    :param scope: 经营范围文本
    :return:
    """


    # 指定服务器的IP
    with BertClient(ip='58.56.131.11', show_server_config=False,
                    check_version=False, check_length=False, mode='NER', port=5557, port_out=5558) as bc:
        scope = re.sub(u'\\（.*?\\）|\\（.*$|[0-9]', '', scope)
        scope = re.sub(' ','，', scope)
        # 将句子分为长度不超过128的片段分别处理，因为目前模型设定最大句长为128
        sections = len(scope)//121 +1
        product_list = []
        for n in range(sections):
            scope_section = scope[121*n:121*(n+1)]
            rst = bc.encode([scope_section])
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
                    term = scope_section[start_index: end_index]
                    product = ''.join(term)
                    out_list.append(product)
                    start_flag = False
            products = ';'.join(out_list)
            product_list.append(products)
    extracted_products = ';'.join(product_list)
    # print(rst)
    print(extracted_products)
    return extracted_products

if __name__ == '__main__':
    extractProduct('许可经营项目:无 一般经营项目:科学仪器、实验仪器、化玻仪器、水分分析仪器、气体分析仪器、油品分析仪器、化工原料及化学试剂（专营、危险品除外）、五金工具、实验室耗材及实验室家俱、办公用品的销售')