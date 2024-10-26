import json
import re
import numpy as np
import random
class entityClassFiltering:
    def __init__(self, output_file, filter_output_file, ifDeleteOtherSpatialAndOtherTime, ifDeleteNestedSpatial, ifDeleteOnlyDataProductsName, ifDeleteUnusedAbbreviation, ifDeleteotherLabel_selfDefined,ifDeleteSomeLabel,ifRandom):
        self.output_file = output_file
        self.output_data = open(self.output_file, 'r', encoding='utf-8')
        self.filter_output_file = filter_output_file
        self.ifDeleteOtherSpatialAndOtherTime = ifDeleteOtherSpatialAndOtherTime
        self.ifDeleteNestedSpatial = ifDeleteNestedSpatial
        self.ifDeleteOnlyDataProductsName = ifDeleteOnlyDataProductsName
        self.ifDeleteUnusedAbbreviation = ifDeleteUnusedAbbreviation
        self.ifDeleteotherLabel_selfDefined = ifDeleteotherLabel_selfDefined
        self.ifDeleteSomeLabel = ifDeleteSomeLabel
        self.ifRandom = ifRandom
        pass

    def multiple_delete(self, line):
        dic = json.loads(line) # 逐行转为json格式
        raw_ner = dic['ner'] # 提取出ner部分
        if self.ifDeleteOtherSpatialAndOtherTime:
            raw_ner = self.delete_spatial_and_time(raw_ner)
        if self.ifDeleteNestedSpatial:
            raw_ner = self.delete_nested_spatial(raw_ner)
        if self.ifDeleteOnlyDataProductsName:
            raw_ner = self.delete_data_products_name(raw_ner)
        if self.ifDeleteUnusedAbbreviation:
            raw_ner = self.delete_other_and_abbreviation(raw_ner)
        if self.ifDeleteotherLabel_selfDefined:
            raw_ner = self.delete_label_selfDefined(raw_ner)
        if self.ifDeleteSomeLabel:
            raw_ner = self.if_Delete_SomeLabel(raw_ner)
        return raw_ner



    def delete_spatial_and_time(self, raw_ner):
        judge = 0
        dic_to_delete = {}
        index_to_delete = []
        for i in range(len(raw_ner)):
            for j in range(len(raw_ner[i])):  
                if (len(raw_ner[i][j]) == 3 and (raw_ner[i][j][2] == 'data products name' or raw_ner[i][j][2] == 'method' or raw_ner[i][j][2] == 'sensor')) or (len(raw_ner[i][j]) == 5 and (raw_ner[i][j][4] == 'data products name' or raw_ner[i][j][4] == 'method' or raw_ner[i][j][4] == 'sensor')):
                    judge += 1
            if judge > 0:
                judge = 0
                continue
            if judge == 0 and raw_ner[i] != []:
                for index, var in enumerate(raw_ner[i]):
                    dic_to_delete[index] = var
                for j in range(len(raw_ner[i])):
                    if len(raw_ner[i][j]) == 3 and (raw_ner[i][j][2] == 'other_spatial' or raw_ner[i][j][2] == 'other_time'):
                        index_to_delete.append(j)
                for k in index_to_delete:
                    dic_to_delete.pop(k)
                raw_ner[i] = list(dic_to_delete.values())
                index_to_delete.clear()
                dic_to_delete.clear()
        return raw_ner

    def delete_nested_spatial(self, raw_ner):
        dic_to_delete = {}
        index_to_delete = []
        for i in range(len(raw_ner)):
            for index, var in enumerate(raw_ner[i]):
                dic_to_delete[index] = var
            for j in range(len(raw_ner[i])):
                if len(raw_ner[i][j]) == 3 and raw_ner[i][j][2] == 'spatial' and len(raw_ner[i][j - 1]) == 3 and raw_ner[i][j - 1][2] == 'spatial' and raw_ner[i][j][0] >= raw_ner[i][j - 1][0] and raw_ner[i][j][1] <= raw_ner[i][j - 1][1]:
                    index_to_delete.append(j)
            for k in index_to_delete:
                dic_to_delete.pop(k)
            raw_ner[i] = list(dic_to_delete.values())
            index_to_delete.clear()
            dic_to_delete.clear()
        return raw_ner

    def delete_data_products_name(self, raw_ner):
        judge = 0
        index = 0
        for i in range(len(raw_ner)):
             if raw_ner[i] == []:
                 continue
             for j in range(len(raw_ner[i])):
                index = j
                if raw_ner[i][j] != [] and raw_ner[i][j][2] == 'data products name':
                    continue
                if raw_ner[i][j] != [] and raw_ner[i][j][2] != 'data products name':
                    judge += 1
                    continue
             if judge == 0:
                del raw_ner[i][index]
             judge = 0
        return raw_ner

    def delete_other_and_abbreviation(self, raw_ner):
        dic_to_delete = {}
        index_to_delete = []
        for i in range(len(raw_ner)):
            for index, var in enumerate(raw_ner[i]):
                dic_to_delete[index] = var
            for j in range(len(raw_ner[i])):
                if (len(raw_ner[i][j]) == 3 and (raw_ner[i][j][2] == 'other' or raw_ner[i][j][2] == 'abbreviation')) or (len(raw_ner[i][j]) == 5 and (raw_ner[i][j][4] == 'other' or raw_ner[i][j][4] == 'abbreviation')):
                    index_to_delete.append(j)
            for k in index_to_delete:
                dic_to_delete.pop(k)
            raw_ner[i] = list(dic_to_delete.values())
            index_to_delete.clear()
            dic_to_delete.clear()
        return raw_ner

    def delete_label_selfDefined(self, raw_ner):
        dic_to_delete = {}
        index_to_delete = []
        for i in range(len(raw_ner)):
            for index, var in enumerate(raw_ner[i]):
                dic_to_delete[index] = var
            for j in range(len(raw_ner[i])):
                if (len(raw_ner[i][j]) == 3 and (raw_ner[i][j][2] == 'Time resolution' or
                                                 raw_ner[i][j][2] == 'spatial resolution'or
                                                 raw_ner[i][j][2] == 'repository'or
                                                 raw_ner[i][j][2] == 'organization')) or \
                        (len(raw_ner[i][j]) == 5 and (raw_ner[i][j][4] == 'Time resolution' or
                                                 raw_ner[i][j][4] == 'spatial resolution'or
                                                 raw_ner[i][j][4] == 'repository'or
                                                 raw_ner[i][j][4] == 'organization')):
                    index_to_delete.append(j)
            for k in index_to_delete:
                dic_to_delete.pop(k)
            raw_ner[i] = list(dic_to_delete.values())
            index_to_delete.clear()
            dic_to_delete.clear()
        return raw_ner

    def if_Delete_SomeLabel(self, raw_ner):
        dic_to_delete = {}
        index_to_delete = []
        for i in range(len(raw_ner)):
            for index, var in enumerate(raw_ner[i]):
                dic_to_delete[index] = var
            for j in range(len(raw_ner[i])):
                if (len(raw_ner[i][j]) == 3 and (raw_ner[i][j][2] == 'sensor' or
                                                 raw_ner[i][j][2] == 'method'or
                                                 raw_ner[i][j][2] == 'other_spatial'or
                                                 raw_ner[i][j][2] == 'other_time'or
                                                 raw_ner[i][j][2] == 'raw data name')) or \
                        (len(raw_ner[i][j]) == 5 and (raw_ner[i][j][4] == 'sensor' or
                                                 raw_ner[i][j][4] == 'method'or
                                                 raw_ner[i][j][4] == 'other_spatial'or
                                                 raw_ner[i][j][4] == 'other_time'or
                                                 raw_ner[i][j][4] == 'raw data name')):
                    index_to_delete.append(j)
            for k in index_to_delete:
                dic_to_delete.pop(k)
            raw_ner[i] = list(dic_to_delete.values())
            index_to_delete.clear()
            dic_to_delete.clear()
        return raw_ner

    def shuffle_jsonl_file(self):
        with open(self.filter_output_file, 'r') as f:
            data_lines = f.readlines()

        random.shuffle(data_lines)

        with open(self.filter_output_file, 'w') as f:
            f.writelines(data_lines)

    def mainFiltering(self):
        with open(self.filter_output_file, 'w') as f_out:
            for line in self.output_data.readlines():
                generateDic = {"clusters": [], "sentences": [], "ner": [], "relations": [], "doc_key": ""}
                processed_ner = self.multiple_delete(line)
                dic = json.loads(line)
                generateDic['ner'] = processed_ner
                generateDic['sentences'] = dic['sentences']
                f_out.write(json.dumps(generateDic) + '\n')
        #

        if self.ifRandom:
            self.shuffle_jsonl_file()