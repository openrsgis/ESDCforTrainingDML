import json
import re
import numpy as np
import datetime
import os

class SCIRec2bartnerClass:
    def __init__(self, input_file, output_path, train_file, dev_file, test_file):
        self.input_data1 = open(input_file, 'r', encoding='utf-8')
        self.input_data2 = open(input_file, 'r', encoding='utf-8')
        self.train_file = train_file
        self.dev_file = dev_file
        self.test_file = test_file

    def getNumberOfArticles(self):
        line_count = 0
        for line in self.input_data2.readlines():
            line_count += 1
        return line_count

    def SCIRec2bartner(self):
        n = 1
        line_count = self.getNumberOfArticles()
        with open(self.train_file, "w", encoding='utf-8') as f1:
            with open(self.dev_file, "w", encoding='utf-8') as f2:
                with open(self.test_file, "w", encoding='utf-8') as f3:
                    for line in self.input_data1.readlines():
                        dic = json.loads(line)  # 逐行转为json格式
                        sentences = dic['sentences']  # 提取出文献的文本内容
                        processed_ner = dic['ner']  # 提取出ner部分
                        if n >= 1 and n <= 0.8 * line_count:
                            for i in range(len(sentences)):
                                joined_ner = ''
                                joined_sentences = ' '.join(sentences[i])
                                joined_sentences += '\n'
                                f1.write(joined_sentences)
                                if processed_ner[i] != []:
                                    for j in range(len(processed_ner[i])):
                                        if len(processed_ner[i][j]) == 3:
                                            processed_ner[i][j].insert(1, ',')
                                            processed_ner[i][j].insert(3, ' ')
                                        else:
                                            processed_ner[i][j].insert(1, ',')
                                            processed_ner[i][j].insert(3, ',')
                                            processed_ner[i][j].insert(5, ',')
                                            processed_ner[i][j].insert(7, ' ')
                                        ner_str = [str(item) for item in processed_ner[i][j]]
                                        joined_ner += ''.join(ner_str)
                                        if j != len(processed_ner[i]) - 1:
                                            joined_ner += '|'
                                    joined_ner += '\n'
                                    f1.write(joined_ner)
                                    f1.write('\n')
                                if processed_ner[i] == []:
                                    f1.write('\n')
                                    f1.write('\n')
                        if n > 0.8 * line_count and n <= 0.9 * line_count:
                                for i in range(len(sentences)):
                                    joined_ner = ''
                                    joined_sentences = ' '.join(sentences[i])
                                    joined_sentences += '\n'
                                    f2.write(joined_sentences)
                                    if processed_ner[i] != []:
                                        for j in range(len(processed_ner[i])):
                                            if len(processed_ner[i][j]) == 3:
                                                processed_ner[i][j].insert(1, ',')
                                                processed_ner[i][j].insert(3, ' ')
                                            else:
                                                processed_ner[i][j].insert(1, ',')
                                                processed_ner[i][j].insert(3, ',')
                                                processed_ner[i][j].insert(5, ',')
                                                processed_ner[i][j].insert(7, ' ')
                                            ner_str = [str(item) for item in processed_ner[i][j]]
                                            joined_ner += ''.join(ner_str)
                                            if j != len(processed_ner[i]) - 1:
                                                joined_ner += '|'
                                        joined_ner += '\n'
                                        f2.write(joined_ner)
                                        f2.write('\n')
                                    if processed_ner[i] == []:
                                        f2.write('\n')
                                        f2.write('\n')
                        if n > 0.9 * line_count and n <= line_count:
                                for i in range(len(sentences)):
                                    joined_ner = ''
                                    joined_sentences = ' '.join(sentences[i])
                                    joined_sentences += '\n'
                                    f3.write(joined_sentences)
                                    if processed_ner[i] != []:
                                        for j in range(len(processed_ner[i])):
                                            if len(processed_ner[i][j]) == 3:
                                                processed_ner[i][j].insert(1, ',')
                                                processed_ner[i][j].insert(3, ' ')
                                            else:
                                                processed_ner[i][j].insert(1, ',')
                                                processed_ner[i][j].insert(3, ',')
                                                processed_ner[i][j].insert(5, ',')
                                                processed_ner[i][j].insert(7, ' ')
                                            ner_str = [str(item) for item in processed_ner[i][j]]
                                            joined_ner += ''.join(ner_str)
                                            if j != len(processed_ner[i]) - 1:
                                                joined_ner += '|'
                                        joined_ner += '\n'
                                        f3.write(joined_ner)
                                        f3.write('\n')
                                    if processed_ner[i] == []:
                                        f3.write('\n')
                                        f3.write('\n')
                        n += 1



if __name__ == '__main__':
    # input_file = '../result/dataSCIRecFormat/data_doccano2SCIRecFormat.jsonl'
    # train_file = '../result/bartner/train.txt'
    # valid_file = '../result/bartner/valid.txt'
    # test_file  = '../result/bartner/test.txt'
    # d = SCIRec2bartner(input_file, train_file)
    # d.SCIRec2bartner()


    pass