# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@version
@author: ms
@contact: masai@bat100.net
@software: python
@file: brat_process.py
@time: 2019/10/08 16:00
@description: 本模块的作用是将brat中标注的产品实体文档转换为模型数据集BIO格式
"""

import re
import os
import sys

rootPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(rootPath)

brat_path = '../../business_scopes'

def brat2BIO(ann_filename, txt_filename, bio_file):
    """
    读取brat中标注的ann文件和txt文件，并按其中的index将源文件txt转换为BIO格式的数据集
    :param filename:
    :return:
    """
    # 读取brat中标注的ann文件
    ann = open(os.path.join(brat_path, ann_filename), 'r', encoding='utf-8')
    ann_lines = ann.readlines()
    # 读取brat中的txt源文件
    txt = open(os.path.join(brat_path, txt_filename), 'r', encoding='utf-8')
    txt_file = re.sub('\n', '。\n', txt.read()) # 每行末尾加入一个句号，以便与ann标注文件计算的index对齐

    # 将ann文件中标注的实体的index按顺序写入列表备用
    entity_index_list = []
    for i in range(len(ann_lines)):  # 遍历ann标注文件的每一行，即每一个产品实体
        try:
            ann_line = re.split(r'[\s]', ann_lines[i])
            entity_index_start = int(ann_line[2])
            entity_index_end = int(ann_line[3])
            entity_index_list.extend([entity_index_start, entity_index_end])
        except:
            print('跳过格式有误的行：', ann_line)
    entity_index_list.sort()
    # 有些相邻实体的前一实体结尾index等于后一实体的开始index，将该index筛选出来，以便在生成标签时将这两个实体合并，同时防止index混乱
    entity_index_list_check = list(zip(entity_index_list[1::2], entity_index_list[2::2]))
    check_list = []
    for i in range(len(entity_index_list_check)):
        if entity_index_list_check[i][1]-entity_index_list_check[i][0] == 0:
            check_list.append(entity_index_list_check[i][0])

    # 带BIO标签数据集生成
    file = open(os.path.join(brat_path, bio_file), 'w', encoding='utf-8')

    start_flag = False

    for k in range(len(txt_file)):

        if k in entity_index_list:
            if not start_flag:
                file.write(txt_file[k]+' '+'B-PROD'+'\n')
                start_flag = True
            elif start_flag:
                if k in check_list: # 如果碰到相邻实体，则将它们连起来
                    file.write(txt_file[k] + ' ' + 'I-PROD' + '\n')
                    start_flag = True
                else:
                    file.write(txt_file[k]+' '+'O'+'\n')
                    start_flag = False
        elif start_flag:
            file.write(txt_file[k]+' '+'I-PROD'+'\n')
        else:
            file.write(txt_file[k] + ' ' + 'O' + '\n')
    file.close()

    # 重新读取file，去除每行开始的' O'（笨办法，待优化）
    final_txt = open(os.path.join(brat_path, bio_file), 'r', encoding='utf-8')
    final_txt_line = final_txt.read()
    final_txt_line = re.sub('\n O\n','\n', final_txt_line)
    final_bio_file = open(os.path.join(brat_path, bio_file), 'w', encoding='utf-8')
    final_bio_file.write(final_txt_line)

def bioGenerate():
    """
    生成带BIO标签的单个txt文件
    :return:
    """
    # 在每个文件夹内生成单个bio文件, 7和10代表含标注文件的7个文件夹下的10个文件
    for i in range(7):
        for k in range(10):
            brat2BIO('scopes_dir_{}/file_{}.ann'.format(i,k), 'scopes_dir_{}/file_{}.txt'.format(i,k), 'scopes_dir_{}/bio_file_{}.txt'.format(i,k))


def bio2Train():
    """
    将生成的单个bio文件整合成训练、验证和测试集
    :return:
    """
    data_path = r'E:\NER-Product-brat\BERT-BiLSTM-CRF-NER-master\data'
    train = open(os.path.join(data_path, 'train.txt'), 'w', encoding='utf-8')
    dev = open(os.path.join(data_path, 'dev.txt'), 'w', encoding='utf-8')
    test = open(os.path.join(data_path, 'test.txt'), 'w', encoding='utf-8')
    for i in range(5):
        for k in range(10):
            bio_file = open(os.path.join(brat_path, 'scopes_dir_{}/bio_file_{}.txt'.format(i,k)), encoding='utf-8')
            for line in bio_file:
                train.writelines(line)
    for i in range(5,6):
        for k in range(10):
            bio_file = open(os.path.join(brat_path, 'scopes_dir_{}/bio_file_{}.txt'.format(i,k)), encoding='utf-8')
            for line in bio_file:
                dev.writelines(line)
    for i in range(6,7):
        for k in range(10):
            bio_file = open(os.path.join(brat_path, 'scopes_dir_{}/bio_file_{}.txt'.format(i,k)), encoding='utf-8')
            for line in bio_file:
                test.writelines(line)


if __name__ == '__main__':
    bio2Train()