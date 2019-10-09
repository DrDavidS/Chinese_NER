import os
import re

def str2ner_train_data(s, save_path):
    """
    快速识别标记数据，保存为训练用格式
    
    数据标记：
    
    原始数据：
    '我来到1999年的上海的东华大学'
    
    标记形式：
    '我来到{{1999年#YEAR}}的{{上海#LOC}}的{{东华大学#ORG}}'
    
    param:
    s：'我来到{{1999年#YEAR*}}的{{上海#LOC}}的{{东华大学#ORG}}'
    save_path：保存路径
    """
    ner_data = []
    result_1 = re.finditer(r'\{\{', s)
    result_2 = re.finditer(r'\}\}', s)
    begin = []
    end = []
    
    for each in result_1:
        begin.append(each.start())
    for each in result_2:
        end.append(each.end())
    assert len(begin) == len(end)  # 确保前后对称
    # 列表 begin 和 end 记录了位置
    
    i = 0
    j = 0
    while i < len(s):
        if i not in begin:
            # 将所有 O 汉字放入 ner_data
            # 我/来/到/的
            ner_data.append([s[i], 'O'])  # other
            i = i + 1
        else:
            # 选择标记对象
            # 1999年#YEAR
            # 拆分储存在 entity 和 ner 中
            # entity：1999
            # ner：YEAR
            ann = s[i + 2:end[j] - 2]
            entity, ner = ann.rsplit('#')
            
            if (len(entity) == 1):
                # 如果实体只有一个字符
                ner_data.append([entity, 'S-' + ner])
            elif (len(entity) == 2):
                # 如果实体有两个字符
                ner_data.append([entity[0], 'B-' + ner])
                ner_data.append([entity[1], 'E-' + ner])
            else:
                # 如果实体有三个及以上字符
                ner_data.append([entity[0], 'B-' + ner])
                for n in range(1, len(entity) - 1):
                    ner_data.append([entity[n], 'I-' + ner])
                ner_data.append([entity[-1], 'E-' + ner])
            # 直到末尾
            i = end[j]
            j = j + 1
    
    # 现在标注信息都在 ner_data 中，这是一个二维列表 
    f = open(save_path, 'w', encoding='utf-8')
    # print(ner_data)
    for each in ner_data:
        if each == ['\n', 'O']:
            each = ['', '']
        print(each)
        # 格式：
        # 我 O
        # 来 0
        # 到 O
        # 1 B-YEAR
        # 9 I-YEAR
        # 9 I-YEAR
        # 9 I-YEAR
        # 年 E-YEAR
        # 的 O
        # ...
        f.write(each[0] + ' ' + each[1])
        f.write('\n')
    f.close()

def txt2ner_train_data(file_path, save_path):
    """
    读取文本标记好的文本文件，进行分词
    
    param：
    file_path：人工标记好的文本文件路径
    save_path：训练用格式的文件路径
    """
    fr = open(file_path, 'r', encoding='utf-8')
    lines = fr.readlines()
    s = ''
    for line in lines:
        # line = line.replace('\n', '')
        line = line.replace(' ', '')
        s = s + line
    fr.close()
    str2ner_train_data(s, save_path)

if __name__=='__main__':
    # s = '我来到{{1999年#YEAR}}的{{上海#LOC}}的{{东华大学#ORG}}'
    # print(len(s))
    # save_path = 's.txt'
    # str2ner_train_data(s, save_path)
    file_path = os.getcwd()
    txt2ner_train_data(file_path+'\\raw.txt', 'splited.txt')