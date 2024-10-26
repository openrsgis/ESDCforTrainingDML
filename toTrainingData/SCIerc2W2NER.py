# -*- coding: utf-8 -*-
# @Time    : 2023/8/8 11:35

import json

class SCIerc2W2NERClass:
    def __init__(self, input_file, train_file, dev_file, test_file):
        self.input_file = input_file
        self.input_data2 = open(input_file, 'r', encoding='utf-8')
        self.train_file = train_file
        self.dev_file = dev_file
        self.test_file = test_file
        self.target_data_train = []
        self.target_data_dev = []
        self.target_data_test = []

    # 为了4:1:1划分，计算一下总行数
    def getNumberOfArticles(self):
        line_count = 0
        for line in self.input_data2.readlines():
            line_count += 1
        return line_count

    def constructTarget_data(self, line, target_data):

        data = json.loads(line.strip())  # 
        sentences = data["sentences"]
        ner_info_list = data["ner"]  # 
        for i in range(len(sentences)):
            sentence_tokens = sentences[i]
            sentence_ner_list = ner_info_list[i]  # 获取ner_info的内部列表

            target_ner = []  

            for item in sentence_ner_list:
                if not isinstance(item, list) or len(item) < 3:
                    continue

                indexes = []  # 用于保存包含所有涉及到的token下标的列表

                if len(item) == 3:
                    start_index = item[0]
                    end_index = item[1] + 1  # 结束下标要加1，因为切片时结束下标是不包含的
                    indexes = list(range(start_index, end_index))
                else:
                    for j in range(0, len(item) - 1, 2):
                        if j + 1 < len(item):
                            start_index = item[j]
                            end_index = item[j + 1] + 1  # 结束下标要加1
                            indexes.extend(list(range(start_index, end_index)))

                ner_type = item[-1]  # 获取实体类型字段
                target_ner.append({"index": indexes, "type": ner_type})

            target_item = {
                "sentence": sentence_tokens,
                "ner": target_ner
            }
            target_data.append(target_item)  # 将目标数据项添加到目标数据列表



    def SCIec2W2NERfunction(self):
        with open(self.input_file, 'r', encoding='utf-8') as f:
            n = 1
            line_count = self.getNumberOfArticles()
            for line in f:
                print(n)
                if n >= 1 and n <= 0.8 * line_count:
                    self.constructTarget_data(line, self.target_data_train)
                if n > 0.8 * line_count and n <= 0.9 * line_count:
                    self.constructTarget_data(line, self.target_data_dev)
                if n > 0.9 * line_count and n <= line_count:
                    self.constructTarget_data(line, self.target_data_test)
                n+=1



        with open(self.train_file, 'w', encoding='utf-8') as f:
            json.dump(self.target_data_train, f, ensure_ascii=False, separators=(',', ':'), indent=None)
        with open(self.dev_file, 'w', encoding='utf-8') as f:
            json.dump(self.target_data_dev, f, ensure_ascii=False, separators=(',', ':'), indent=None)
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(self.target_data_test, f, ensure_ascii=False, separators=(',', ':'), indent=None)












