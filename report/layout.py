import numpy as np
import xlrd
from docx import Document
import re

# csv文件读取
def CSVfileread(file):
    file.seek(0)  # https://www.jianshu.com/p/0d15ed85df2b
    file_data = file.read().decode('utf-8')
    lines = file_data.split('\r\n')
    for i in range(len(lines)):
        if len(lines[i]) != 0:
            # 以逗号分隔字符串,但忽略双引号内的逗号
            lines[i] = re.split(r',\s*(?![^"]*\"\,)', lines[i])
            # lines[i]=lines[i].split(',') # 按逗号分隔后把每一行都变成一个列表
        else:
            lines[i] = re.split(r',\s*(?![^"]*\"\,)', lines[i])
            del lines[i]  # 最后一行如为空行，则删除该元素

    # 从第一行确定化合物名称(含有"-Q Results"),并添加进入化合物列表
    norm = []  # 化合物列表
    for j in range(len(lines[0])):  # 从第一行开始
        if "-Q Results" in lines[0][j]:
            # 若原始字符串中含有','，切割完后首位会多出一个'"',需去除
            if lines[0][j].split("-Q")[0][0] != '"':
                norm.append(lines[0][j].split("-Q")[0])
            else:
                norm.append(lines[0][j].split("-Q")[0][1:])

    return norm