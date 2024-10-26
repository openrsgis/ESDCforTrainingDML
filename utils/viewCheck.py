# -*- coding: utf-8 -*-
# @Time    : 2023/7/20 9:38
import json

class viewCheck:
    def __init__(self, input_file,eachnumber2View):
        self.input_file = input_file
        self.eachnumber2View = eachnumber2View

    def view(self):
        output_data = open(self.input_file, 'r', encoding='utf-8')
        n = 1
        for line in output_data.readlines():
            dic = json.loads(line)
            n += 1
            if n % self.eachnumber2View == 0:  
                print("第", str(n), "篇")
                for i in range(len(dic['ner'])):
                    for j in range(len(dic['ner'][i])):
                        entity_span = ''
                        entity_type = ''
                        if len(dic['ner'][i][j]) == 3:
                            entity_index = dic['ner'][i][j]
                            sub_sentence = dic['sentences'][i]
                            entity_span = sub_sentence[int(entity_index[0]):int(entity_index[1]) + 1]
                            entity_type = entity_index[2]
                        elif len(dic['ner'][i][j]) == 5:
                            entity_index = dic['ner'][i][j]
                            sub_sentence = dic['sentences'][i]
                            entity_span_1 = sub_sentence[int(entity_index[0]):int(entity_index[1]) + 1]
                            entity_span_2 = sub_sentence[int(entity_index[2]):int(entity_index[3]) + 1]
                            entity_span = entity_span_1 + entity_span_2
                            entity_type = entity_index[4]
                        else:
                            print("ner输出list有误")

                        print(entity_span, entity_type)






