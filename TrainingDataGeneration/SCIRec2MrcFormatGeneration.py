# -*- coding: utf-8 -*-
# @Time    : 2023/3/8 10:54

import os
import json


class toMRCFromat:
    def __init__(self, dataname, raw_dir, mrc_dir, query_list_path, ifDivide):

        self.dataname = dataname
        self.raw_dir = raw_dir  # 输入路径
        self.mrc_dir = mrc_dir  # 输出路径
        self.query_list_path = query_list_path   # 问题列表
        os.makedirs(mrc_dir, exist_ok=True)  # 多级创建目录
        self.ifDivide = ifDivide

    def SCIRecSplitSubList(self, lst, jsn):

        json_dict = []
        for i, sublst in enumerate(lst):
            split_index = sum(len(sub) for sub in lst[:i])
            # print(split_index)
            split_jsn = {}
            for key, indices in jsn.items():
                split_indices = []
                for index in indices:
                    start, end = index.split(';')
                    start = int(start) - split_index
                    end = int(end) - split_index
                    if start >= 0 and end < len(sublst):
                        split_indices.append(f"{start};{end}")
                if split_indices:
                    split_jsn[key] = split_indices
            # print(json.dumps(split_jsn))
            json_dict.append(json.dumps(split_jsn))
        return json_dict

    def mainConvert(self):
        if self.ifDivide:
            for phase in ["train", "dev", "test"]:
                raw_file_path = os.path.join(self.raw_dir, f"{phase}.json")
                output_file_path = os.path.join(self.mrc_dir, f"mrc-ner-{self.dataname}.{phase}")
                self.convertTransform(raw_file_path, output_file_path, self.query_list_path)
        else:
            raw_file_path = os.path.join(self.raw_dir, f"{self.dataname}.json")
            output_file_path = os.path.join(self.mrc_dir, f"mrc-ner.{self.dataname}.json")
            self.convertTransform(raw_file_path, output_file_path, self.query_list_path)


    def convertTransform(self,raw_file_path, output_file_path, query_list):

        all_raw_line_data = [json.loads(line) for line in open(raw_file_path)]  # 每一行数据读取，并解析成JSON，将所有JSON对象保存到一个列表
        tag2query = json.load(open(query_list))

        output = []
        origin_count = 0
        new_count = 0
        for raw_line_data in all_raw_line_data:
            origin_count += 1
            context_mutilList = raw_line_data['sentences'] # SCIRec中原始的文本 [["English", "is", "shown"...
            index_label_list = raw_line_data['ner']

            index_label_dic = {}
            for sublist in index_label_list:
                for pos in sublist:
                    for tag in pos[2:]:
                        if tag not in index_label_dic:
                            index_label_dic[tag] = []
                        index_label_dic[tag].append(';'.join(str(x) for x in pos[:2]))

            reindex_label_dic=self.SCIRecSplitSubList(context_mutilList, index_label_dic)



            for i,context_sublist in enumerate(context_mutilList):
                context = " ".join(context_sublist)
                print(context)
                # TODO
                for tag_idx, (tag, query) in enumerate(tag2query.items()):
                    positions = json.loads(reindex_label_dic[i]).get(tag, [])
                    # TODO 非连续的没有做
                    mrc_sample = {
                        "context": context,                                                 
                        "query": query,                                                     
                        "start_position": [int(x.split(";")[0]) for x in positions],        
                        "end_position": [int(x.split(";")[1]) for x in positions],         
                        "span_position":positions,
                        "entity_label": tag,                                                
                        "qas_id": f"{origin_count}.{tag_idx}",                              
                        "impossible": False if [int(x.split(";")[0]) for x in positions] else True
                    }
                    output.append(mrc_sample)
                    new_count += 1
                    print(mrc_sample)
            json.dump(output, open(output_file_path, "w"), ensure_ascii=False, indent=2)
            print(f"Convert {origin_count} samples to {new_count} samples and save to {output_file_path}")














