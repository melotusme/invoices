#!/usr/bin/env python
# encoding: utf-8

import sys
import importlib
importlib.reload(sys)

from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.invocies
collection = db.invocies

'''
 解析pdf 文本，保存到txt文件中
'''
pdf_path = r't.pdf'
txt_path = '1.txt'
def parse():
    fp = open(pdf_path, 'rb') # 以二进制读模式打开
    #用文件对象来创建一个pdf文档分析器
    parser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)

    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一个page的内容
        for page in doc.get_pages(): # doc.get_pages() 获取page列表
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            with open(txt_path, 'w') as f:
                for x in layout:
                    if (isinstance(x, LTTextBoxHorizontal)):
                        results = x.get_text()
                        f.write(results)

if __name__ == '__main__':
    parse()
    file = open(txt_path, "r")
    lines = file.readlines()
    lines = [l.strip() for l in lines]
    pre = ""
    invoice = {}
    price = ""
    for l in lines:
        if l.endswith(":"):
            pre = l
        else:
            if pre != "":
                invoice[pre]=l
                pre = ""
        if l.startswith("(小写)"):
            invoice["价格"]= price
        price = l

    collection.insert_one(invoice)
    file.close()
