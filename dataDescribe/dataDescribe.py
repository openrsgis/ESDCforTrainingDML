# -*- coding: utf-8 -*-
# @Time    : 2023/3/8 10:43

import os
import json
import jsonlines
from collections import defaultdict

SCIRecFormatDataFile = '/home/leehom/NLP/dataPreprocess/data/ESSD/MRC/OutputDoccanoFormat/doccano2SCIRecFormat_abbre.jsonl'
with jsonlines.open(SCIRecFormatDataFile) as reader:
    entitiesLabelNumDict = defaultdict(int)     
    entitiesLengthDict = defaultdict(int)
    sentencesNumDict = defaultdict(int)
    paperNum = 0      
    sentencesNum = 0 
    for obj in reader:
        paperNum += 1
        entities_list = obj['ner']
        for span_list in entities_list:
            for span in span_list:
                entitiesLabelNumDict[span[2]] += 1                          
                entitiesLengthDict[span[2]] += (span[1] - span[0] + 1)      

        sentences_list = obj['sentences']
        for span_list in entities_list:
            sentencesNum += 1
            # TODO
            pass


    label_avg_length_dict = {}
    # label_avg_length_dict = {}
    for k, v in entitiesLengthDict.items():
        label_avg_length_dict[k] = v / entitiesLabelNumDict[k]    
        # avg_length_dict[k] = v / entitiesLabelNumDict[k]         


    print(entitiesLabelNumDict)
    # print(avg_length_dict)



class SCIREcFormatDescribe:
    def __init__(self, SCIRecFormatDataFile):

        self.SCIRecFormatDataFile = SCIRecFormatDataFile   # 输入 SCIRecFormat文件 路径


        pass

    def entitiesNumberStatistics(self):
        all_raw_line_data = [json.loads(line) for line in open(self.SCIRecFormatDataFile)] # 每一行数据读取，并解析成JSON，将所有JSON对象保存到一个列表
        for raw_line_data in all_raw_line_data:
            context_mutilList = raw_line_data['sentences']  # SCIRec中原始的文本 [["English", "is", "shown"...






        pass

    # 
    def sentencesNumberStatistics(self):


        pass


    def mainDataDescribe(self):



        pass



