# -*- coding: utf-8 -*-
# @Time    : 2023/6/15 15:28


import json
import re
import numpy as np


class doccanoTransform:
    def __init__(self,doccano_file, output_path, ifDeleteHttpLine, ifReplaceAbbrev):
        self.doccano_file = doccano_file
        self.output_path = output_path
        self.doccano_data = open(self.doccano_file, 'r', encoding='utf-8')
        self.ifDeleteHttpLine = ifDeleteHttpLine
        self.ifReplaceAbbrev = ifReplaceAbbrev
        pass

    def extractFromDoccano(self, line):

        dic_text = [[]]         
        dic = json.loads(line)  
        text1 = dic['text']     
        start_abbr = []
        end_abbr = []
        len_add = []
        if self.ifReplaceAbbrev:
            dic, start_abbr, end_abbr, len_add, text1 = self.abbre2Fullwrite(dic, text1)
        line_break_idx = [i for i, x in enumerate(text1) if x == '\n']  
        if self.ifDeleteHttpLine:
            start_url = []; end_url = []; length_url = []

            start_url, end_url, length_url = self.delete_url(dic, text1, start_url, end_url, length_url)
            if len(start_url)>= 1:
                for i in range(len(start_url)-1):
                    start_url[i+1] = start_url[i+1]+sum(length_url[:i+1])
                    end_url[i+1] = end_url[i+1]+sum(length_url[:i+1])
            # dic["text"] = re.sub(r'\s+http.*?(?=\s)', "", dic["text"])
            dic["text"] = re.sub(r'http.*?(?=\s)', " ", dic["text"])
            for_http = [line_break_idx, start_url, length_url]
            # dic = self.updateOffset(dic, 0, for_http)
        else:
            start_url = []; end_url = []; length_url=[]  
            # dic = self.updateOffset(dic, 0, for_http)


        dic["text"] = dic["text"].split("\n")
        for i in range(len(dic["text"])):
            dic_text.append([])
            if '\u200b' in dic["text"][i]:
                dic["text"][i] = dic["text"][i].replace('\u200b', '.')   
                dic_text[i].append(str(dic["text"][i]))
            else:
                dic_text[i].append(str(dic["text"][i]))


        sentenceTxt_Split_List = dic_text[:-2]

        for_abbr = [start_abbr, len_add, line_break_idx, start_url, end_abbr, length_url]
        dic = self.updataOffset(dic, 1, for_abbr)

        entities_WordIndex_list, sentenceTxt_SplitEachWord_List = self.charOffset2WordIndex(dic, sentenceTxt_Split_List)


        self.object_connect(entities_WordIndex_list, dic)

        return entities_WordIndex_list, sentenceTxt_SplitEachWord_List

    def object_connect(self, entities_WordIndex_list, dic):
        ifFinish = 0
        for i in range(len(dic['relations'])):
            from_id = dic['relations'][i]['from_id']
            to_id = dic['relations'][i]['to_id']
            for j in range(len(entities_WordIndex_list)):
                if ifFinish > 0:
                    ifFinish = 0
                    break
                if len(entities_WordIndex_list[j]) > 0:
                    for k in range(len(entities_WordIndex_list[j])):
                        if len(entities_WordIndex_list[j][k]) == 4 and entities_WordIndex_list[j][k][3] == from_id:
                            start1 = entities_WordIndex_list[j][k][0]
                            end1 = entities_WordIndex_list[j][k][1]
                            for l in range(len(entities_WordIndex_list[j])):
                                if len(entities_WordIndex_list[j][l]) == 4 and entities_WordIndex_list[j][l][3] == to_id:
                                    start2 = entities_WordIndex_list[j][l][0]
                                    end2 = entities_WordIndex_list[j][l][1]
                                    if len(entities_WordIndex_list[j][l]) == 4:
                                        entities_WordIndex_list[j][l].insert(0, start1)
                                        entities_WordIndex_list[j][l].insert(1, end1)
                                    if len(entities_WordIndex_list[j][k]) == 4:
                                        entities_WordIndex_list[j][k].insert(2, start2)
                                        entities_WordIndex_list[j][k].insert(3, end2)
                                    ifFinish += 1
                                    break
                                if len(entities_WordIndex_list[j][l]) == 6 and entities_WordIndex_list[j][l][5] == to_id:
                                    start2 = entities_WordIndex_list[j][l][2]
                                    end2 = entities_WordIndex_list[j][l][3]
                                    if len(entities_WordIndex_list[j][l]) == 4:
                                        entities_WordIndex_list[j][l].insert(0, start1)
                                        entities_WordIndex_list[j][l].insert(1, end1)
                                    if len(entities_WordIndex_list[j][k]) == 4:
                                        entities_WordIndex_list[j][k].insert(2, start2)
                                        entities_WordIndex_list[j][k].insert(3, end2)
                                    ifFinish +=1
                                    break
                        if ifFinish > 0:
                            break
                        if len(entities_WordIndex_list[j][k]) == 6 and entities_WordIndex_list[j][k][5] == from_id:
                            start1 = entities_WordIndex_list[j][k][0]
                            end1 = entities_WordIndex_list[j][k][1]
                            for l in range(len(entities_WordIndex_list[j])):
                                if len(entities_WordIndex_list[j][l]) == 4 and entities_WordIndex_list[j][l][3] == to_id:
                                    start2 = entities_WordIndex_list[j][l][0]
                                    end2 = entities_WordIndex_list[j][l][1]
                                    if len(entities_WordIndex_list[j][l]) == 4:
                                        entities_WordIndex_list[j][l].insert(0, start1)
                                        entities_WordIndex_list[j][l].insert(1, end1)
                                    if len(entities_WordIndex_list[j][k]) == 4:
                                        entities_WordIndex_list[j][k].insert(2, start2)
                                        entities_WordIndex_list[j][k].insert(3, end2)
                                    ifFinish += 1
                                    break
                                if len(entities_WordIndex_list[j][l]) == 6 and entities_WordIndex_list[j][l][5] == to_id:
                                    start2 = entities_WordIndex_list[j][l][2]
                                    end2 = entities_WordIndex_list[j][l][3]
                                    if len(entities_WordIndex_list[j][l]) == 4:
                                        entities_WordIndex_list[j][l].insert(0, start1)
                                        entities_WordIndex_list[j][l].insert(1, end1)
                                    if len(entities_WordIndex_list[j][k]) == 4:
                                        entities_WordIndex_list[j][k].insert(2, start2)
                                        entities_WordIndex_list[j][k].insert(3, end2)
                                    ifFinish +=1
                                    break
                        if ifFinish > 0:
                            break

        dic_to_delete = {}
        for x in range(len(entities_WordIndex_list)):
            if entities_WordIndex_list[x] != []:
                for index, var in enumerate(entities_WordIndex_list[x]):
                    dic_to_delete[index] = var
                filtered_dict = {}
                seen = set()
                for key, value in dic_to_delete.items():
                    key_tuple = tuple(value[:4])
                    if key_tuple not in seen:
                        filtered_dict[key] = value
                        seen.add(key_tuple)
                entities_WordIndex_list[x] = list(filtered_dict.values())
                seen.clear()
                dic_to_delete.clear()
                filtered_dict.clear()

        for m in range(len(entities_WordIndex_list)):
            if len(entities_WordIndex_list[m]) > 0:
                for n in range(len(entities_WordIndex_list[m])):
                    if len(entities_WordIndex_list[m][n]) == 4:
                        del entities_WordIndex_list[m][n][3]
                    if len(entities_WordIndex_list[m][n]) == 6:
                        del entities_WordIndex_list[m][n][5]



    def delete_url(self, dic, text1, start_url, end_url, length_url):

        text2 = text1
        while bool(re.search(r'http.*?(?=\s)', dic['text'], re.IGNORECASE)) == True:
            start_u = re.search(r'http.*?(?=\s)', text2, re.IGNORECASE).span()[0] + sum(length_url)
            end_u = re.search(r'http.*?(?=\s)', text2, re.IGNORECASE).span()[1] + sum(length_url)
            text2 = text2[0:start_u - sum(length_url)] + text2[end_u - sum(length_url):]
            start_u_dic = re.search(r'http.*?(?=\s)', dic['text'], re.IGNORECASE).span()[0]
            end_u_dic = re.search(r'http.*?(?=\s)', dic['text'], re.IGNORECASE).span()[1]
            length_u = end_u - start_u
            length_url.append(length_u)
            start_url.append(start_u)
            end_url.append(end_u)
            dic['text'] = dic['text'][0:start_u_dic] + dic['text'][end_u_dic:]

        return start_url, end_url, length_url

    def abbre2Fullwrite(self, dic, text1):

        def find_full_write(dic, j):
            full_write_start = entity_sorted_start[j]['start_offset']
            full_write_end = entity_sorted_start[j]['end_offset']
            full_write = dic['text'][full_write_start:full_write_end]
            return full_write

        abbr = []
        full = []
        entity_sorted_start = dic['entities']  ## entity 重排序
        entity_sorted_start.sort(key=lambda x: (x['end_offset']))  ###如果abbreviation第一次出现，肯定在全程后面，所以查找距离最近的实体的尾部
        for i in range(len(entity_sorted_start)):
            if entity_sorted_start[i]['label'] == 'abbreviation':
                start_ab = entity_sorted_start[i]['start_offset']
                end_ab = entity_sorted_start[i]['end_offset']
                abbr_name = dic['text'][start_ab:end_ab]
                abbr.append(abbr_name)
                if dic['text'][end_ab:end_ab + 2] == ' (':  # 第一种情况：前面是abbreviation，后面是（全称）
                    full_write = find_full_write(dic, i + 1)
                    full.append(full_write)
                elif i - 1 >= 0 and entity_sorted_start[i - 1]['start_offset'] < entity_sorted_start[i][
                    'start_offset'] and entity_sorted_start[i - 1]['end_offset'] > entity_sorted_start[i]['end_offset']:
                    full_write = find_full_write(dic, i - 1)
                    full.append(full_write)
                elif i - 2 >= 0 and entity_sorted_start[i - 2]['start_offset'] < entity_sorted_start[i][
                    'start_offset'] and entity_sorted_start[i - 2]['end_offset'] > entity_sorted_start[i]['end_offset']:
                    full_write = find_full_write(dic, i - 2)
                    full.append(full_write)
                elif i - 3 >= 0 and entity_sorted_start[i - 3]['start_offset'] < entity_sorted_start[i][
                    'start_offset'] and entity_sorted_start[i - 3]['end_offset'] > entity_sorted_start[i]['end_offset']:
                    full_write = find_full_write(dic, i - 3)
                    full.append(full_write)

                elif i - 1 >= 0 and (entity_sorted_start[i - 1]['label'] == 'other' or entity_sorted_start[i - 1][
                    'label'] == 'other spatial'):
                    full_write = find_full_write(dic, i - 1)
                    full.append(full_write)
                elif i - 2 >= 0 and (entity_sorted_start[i - 2]['label'] == 'other' or entity_sorted_start[i - 2][
                    'label'] == 'other spatial'):
                    full_write = find_full_write(dic, i - 2)
                    full.append(full_write)
                elif i - 3 >= 0 and (entity_sorted_start[i - 3]['label'] == 'other' or entity_sorted_start[i - 3][
                    'label'] == 'other spatial'):
                    full_write = find_full_write(dic, i - 3)
                    full.append(full_write)
                elif i - 1 >= 0 and i - 2 <= 0:  
                    full_write = find_full_write(dic, i - 1)
                    full.append(full_write)
                elif i - 2 >= 0:  
                    full_write_start1 = entity_sorted_start[i - 1]['start_offset']
                    full_write_end1 = entity_sorted_start[i - 1]['end_offset']
                    full_write_len1 = full_write_end1 - full_write_start1
                    full_write_start2 = entity_sorted_start[i - 2]['start_offset']
                    full_write_end2 = entity_sorted_start[i - 2]['end_offset']
                    full_write_len2 = full_write_end2 - full_write_start2
                    if full_write_end1 >= full_write_end2:
                        full_write = find_full_write(dic, i - 1)
                        full.append(full_write)
                    elif full_write_end1 < full_write_end2:
                        full_write = find_full_write(dic, i - 2)
                        full.append(full_write)
                    else:
                        if full_write_len1 > full_write_len2:
                            full_write = find_full_write(dic, i - 1)
                            full.append(full_write)
                        elif full_write_len1 < full_write_len2:
                            full_write = find_full_write(dic, i - 2)
                            full.append(full_write)
                else:
                    full_write = abbr_name
                    full.append(full_write)

        # replace abbr to full write
        start_abbr = []
        end_abbr = []
        len_add = []
        start_len_partner = []
        len_sort = []
        for n in range(len(abbr)):  
            x = 0  
            abbrname = abbr[n]
            abbrlen = len(abbr[n])
            for m in range(len(text1) - abbrlen):
                if text1[m:m + abbrlen] == abbrname:
                    if x > 0:
                        start_abbr.append(m)
                        end_abbr.append(m + abbrlen)
                        len_add.append(len(full[n]) - abbrlen)
                        start_len_partner.append([m, len(full[n]) - abbrlen])
                        start_len_partner.sort()
                        idx_abbr = start_len_partner.index([m, len(full[n]) - abbrlen])
                        if idx_abbr == 0:
                            dic['text'] = dic['text'][:m] + full[n] + dic['text'][m + abbrlen:]
                        else:
                            for y in range(len(start_len_partner)):
                                len_sort.append(start_len_partner[y][1])
                            dic['text'] = dic['text'][:m + sum(len_sort[:idx_abbr])] + full[n] + dic['text'][m + abbrlen + sum(len_sort[:idx_abbr]):]
                    x += 1

        return dic, start_abbr, end_abbr, len_add, text1

    def updataOffset(self, dic, type_for_update, list_for_update):

        if type_for_update == 0:
            for j in range(len(dic['entities'])):
                start = dic['entities'][j]['start_offset']
                end = dic['entities'][j]['end_offset']
                list_for_update[0].append(start)
                list_for_update[0].append(end)
                list_for_update[0].sort()
                cnt_line_s = list_for_update[0].index(start)
                cnt_line_e = list_for_update[0].index(end)
                list_for_update[1].append(start)
                list_for_update[1].sort()
                cnt_url_s = list_for_update[1].index(start)
                dic['entities'][j]['start_offset'] = start - cnt_line_s - sum(list_for_update[2][:cnt_url_s])
                dic['entities'][j]['end_offset'] = end - cnt_line_e + 1 - sum(list_for_update[2][:cnt_url_s])
                list_for_update[0].remove(start)
                list_for_update[0].remove(end)
                list_for_update[1].remove(start)
        if type_for_update == 1:
            start_partner = []
            new_len_add = []
            for i in range(len(list_for_update[0])):
                start_partner.append([list_for_update[0][i], list_for_update[1][i]])
            start_partner.sort()
            for i in range(len(start_partner)):
                new_len_add.append(start_partner[i][1])

            ## new index of the entities
            for j in range(len(dic['entities'])):
                start = dic['entities'][j]['start_offset']
                end = dic['entities'][j]['end_offset']
                list_for_update[2].append(start)
                list_for_update[2].append(end)
                list_for_update[2].sort()
                cnt_line_s = list_for_update[2].index(start)
                cnt_line_e = list_for_update[2].index(end)
                list_for_update[3].append(start)
                list_for_update[3].sort()
                cnt_url_s = list_for_update[3].index(start)

                list_for_update[0].append(start)
                list_for_update[4].append(end)
                list_for_update[0].sort()
                list_for_update[4].sort()
                cnt_abbr_s = list_for_update[0].index(start)
                cnt_abbr_e = list_for_update[4].index(end)
                if cnt_abbr_e < len(list_for_update[4]) - 1 and list_for_update[4][cnt_abbr_e] == list_for_update[4][cnt_abbr_e + 1]:
                    cnt_abbr_e += 1

                # str = ''
                # for i in range(len(dic['text'])):
                #     str = str + dic['text'][i]
                str1 = ''
                for i in range(len(dic['text'])):
                    str1 = str1 + dic['text'][i]

                dic['entities'][j]['start_offset'] = start - cnt_line_s - sum(list_for_update[5][:cnt_url_s]) + sum(
                    new_len_add[:cnt_abbr_s])
                dic['entities'][j]['end_offset'] = end - cnt_line_e + 1 - sum(list_for_update[5][:cnt_url_s]) + sum(
                    new_len_add[:cnt_abbr_e])
                list_for_update[2].remove(start)
                list_for_update[2].remove(end)
                list_for_update[3].remove(start)
                list_for_update[0].remove(start)
                list_for_update[4].remove(end)
        return dic

    def generateDiscontinuousEntities(self):

        pass


    def charOffset2WordIndex(self, dic, sentenceTxt_Split_List):

        entities_json = dic['entities']

        labels = self.relabel(entities_json)
        text = sentenceTxt_Split_List
        id = dic['id']
        # print(id)
        len_text = [] 
        cnt1_sen = []
        text_new = []

        for j in range(len(text)):
            text_split = []
            cnt1 = []  #
            cnt2 = []  #
            count1 = 0
            count2 = -1
            word = ''
            text_sentence = text[j][0]
            len_text.append(len(text[j][0]))
            for n in range(len(text_sentence)):  ###sentence数量
                if n == len(text_sentence) - 1:
                    if word != '':
                        text_split.append(word)
                    text_split.append(str(text_sentence[n]))
                    count2 += 1
                    count1 += 1
                    cnt1.append(count1)
                    cnt2.append(count2)
                    word = ''
                    for m in cnt1:
                        cnt1_sen.append(m)

                elif text_sentence[n] == ' ':  # 是空格，则添加到word里
                    count2 += 1
                    if word != '':
                        text_split.append(word)
                        if text_sentence[n - 1 - len(word)] == '(' or text_sentence[n - 1 - len(word)] == '[' or \
                                text_sentence[n - 1 - len(word)] == '{':
                            li = [0] * (len(cnt1) - len(word)) + [1] * len(word)
                            count1 += 1
                            cnt1 = np.sum([cnt1, li], axis=0).tolist()
                    if n > 0 and text_sentence[n - 1] != ' ':
                        count1 += 1
                    cnt1.append(count1)
                    cnt2.append(count2)
                    word = ''

                elif text_sentence[n] == '(' or text_sentence[n] == '[' or text_sentence[n] == '{' or text_sentence[
                    n] == ')' or text_sentence[n] == ']' or text_sentence[n] == '}':
                    if word != '':
                        text_split.append(word)
                        if text_sentence[n - 1 - len(word)] != ' ': 
                            count1 += 1
                            li = [0] * (len(cnt1) - len(word)) + [1] * len(word)
                            cnt1 = np.sum([cnt1, li], axis=0).tolist()
                    text_split.append(str(text_sentence[n]))
                    count2 += 1
                    if text_sentence[n - 1] != ' ':
                        count1 += 1
                    cnt1.append(count1)
                    cnt2.append(count2)
                    word = ''
                elif text_sentence[n] == ',':
                    if word != '':
                        text_split.append(word)
                        if text_sentence[n - 1 - len(word)] == '(' or text_sentence[n - 1 - len(word)] == '[' or \
                                text_sentence[n - 1 - len(word)] == '{':
                            li = [0] * (len(cnt1) - len(word)) + [1] * len(word)
                            count1 += 1
                            cnt1 = np.sum([cnt1, li], axis=0).tolist()
                    text_split.append(str(text_sentence[n]))
                    count2 += 1
                    count1 += 1
                    cnt1.append(count1)
                    cnt2.append(count2)
                    word = ''

                else:
                    word += text_sentence[n]
                    count2 += 1
                    cnt1.append(count1)
                    cnt2.append(count2)

            text_new.append(text_split)
        new_len = []  ###index
        for i in range(len(len_text)):
            if i == 0:
                new_len.append(len_text[0] - 1)
            else:
                new_len.append(len_text[i] + new_len[i - 1])

        label_text = [[]]
        j = 0
        for i in range(len(text_new) - 1):
            label_text.append([])
        for la in labels:
            label_li = []
            if len(la) == 0:
                ner_out = '[]'
            else:
                new_len.append(la[0])  ##append starting index
                new_len.sort()
                idx = new_len.index(la[0])  # index of sentence
                label_B = cnt1_sen[la[0]]
                if (la[1] - 1) > len(cnt1_sen):
                    x1 = 1
                label_E = cnt1_sen[la[1] - 1]
                if label_E >= label_B:
                    label_new = [label_B, label_E, la[2], dic['entities'][j]['id']]
                    label_text[idx].append(label_new)
                new_len.remove(la[0])
                j+=1
        _entities_WordIndex_list = label_text
        sentenceTxt_SplitEachWord_List = text_new
        # out_str = '{"ners": ' + str(label_text) + ', "sentences": ' + str(text_new) + '}'
        # print(_entities_WordIndex_list)    # 输出entities 的 word index
        return _entities_WordIndex_list, sentenceTxt_SplitEachWord_List

    def relabel(self, entities_json):
        _entities_charIndex_list = []
        entities_sublist = []
        for i in range(len(entities_json)):
            entities_sublist = []
            start_label = entities_json[i]['start_offset']
            end_label = entities_json[i]['end_offset']
            label = entities_json[i]['label']
            entities_sublist.append(start_label)
            entities_sublist.append(end_label)
            entities_sublist.append(label)
            _entities_charIndex_list.append(entities_sublist)
        return _entities_charIndex_list

    def mainTransform(self):
        with open(self.output_path, 'w') as f_out:
            for line in self.doccano_data.readlines():
                generateDic = {"clusters": [], "sentences": [], "ner": [], "relations": [], "doc_key": ""}
                # print(line)
                entities_WordIndex_list, sentenceTxt_SplitEachWord_List = self.extractFromDoccano(line)
                # generateDic['clusters'] = [clusters]
                generateDic['sentences'] = sentenceTxt_SplitEachWord_List
                generateDic['ner'] = entities_WordIndex_list
                f_out.write(json.dumps(generateDic) + '\n')

        # sentences = [["English", "is", "shown", "to", "be", "trans-context-free", "on", "the", "basis", "of", "coordinations", "of", "the", "respectively", "type", "that", "involve", "strictly", "syntactic", "cross-serial", "agreement", "."], ["The", "agreement", "in", "question", "involves", "number", "in", "nouns", "and", "reflexive", "pronouns", "and", "is", "syntactic", "rather", "than", "semantic", "in", "nature", "because", "grammatical", "number", "in", "English", ",", "like", "grammatical", "gender", "in", "languages", "such", "as", "French", ",", "is", "partly", "arbitrary", "."], ["The", "formal", "proof", ",", "which", "makes", "crucial", "use", "of", "the", "Interchange", "Lemma", "of", "Ogden", "et", "al.", ",", "is", "so", "constructed", "as", "to", "be", "valid", "even", "if", "English", "is", "presumed", "to", "contain", "grammatical", "sentences", "in", "which", "respectively", "operates", "across", "a", "pair", "of", "coordinate", "phrases", "one", "of", "whose", "members", "has", "fewer", "conjuncts", "than", "the", "other", ";", "it", "thus", "goes", "through", "whatever", "the", "facts", "may", "be", "regarding", "constructions", "with", "unequal", "numbers", "of", "conjuncts", "in", "the", "scope", "of", "respectively", ",", "whereas", "other", "arguments", "have", "foundered", "on", "this", "problem", "."]]
        # ner = [[0, 0, "Material"], [10, 10, "OtherScientificTerm"], [17, 20, "OtherScientificTerm"]], [[23, 23, "Generic"], [29, 29, "OtherScientificTerm"], [31, 32, "OtherScientificTerm"], [42, 43, "OtherScientificTerm"], [45, 45, "Material"], [48, 49, "OtherScientificTerm"], [51, 51, "Material"], [54, 54, "Material"]], [[70, 71, "Method"], [86, 86, "Material"]]
        # relations = [[[6, 6, 10, 12, "USED-FOR"], [10, 12, 14, 16, "USED-FOR"]], [[32, 34, 26, 28, "FEATURE-OF"]], [[52, 57, 59, 64, "USED-FOR"]], [[90, 91, 81, 82, "USED-FOR"]], [[96, 98, 103, 105, "PART-OF"]], [[126, 127, 129, 131, "USED-FOR"]], [[142, 142, 148, 148, "COMPARE"], [142, 142, 151, 155, "USED-FOR"], [148, 148, 151, 155, "USED-FOR"], [158, 159, 153, 155, "HYPONYM-OF"], [161, 161, 158, 159, "FEATURE-OF"], [161, 161, 164, 166, "CONJUNCTION"], [164, 166, 158, 159, "FEATURE-OF"]], [[170, 170, 180, 181, "USED-FOR"]]]
        # generateDic = {"clusters":[], "sentences":[], "ner":[], "relations": [], "doc_key": ""}












