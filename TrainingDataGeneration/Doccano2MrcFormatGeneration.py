# -*- coding: utf-8 -*-
# @Time    : 2023/3/8 10:54

import os
import json



class toMRCFromat:
    def __init__(self, dataname, raw_dir, mrc_dir, query_list, queryname, whichLabelKeep, ifDivide):

        self.dataname = dataname
        self.raw_dir = raw_dir  # 输入路径
        self.mrc_dir = mrc_dir  # 输出路径
        self.query_list = query_list   # 问题列表
        self.queryname = queryname   # 问题列表的命名，方便自动命名输出的文件名
        os.makedirs(mrc_dir, exist_ok=True)  # 多级创建目录
        self.whichLabelKeep = whichLabelKeep  # 保留哪些Label
        self.ifDivide = ifDivide  # 原始数据 是否划分了 train vaild test

    def entitiesList2Json(self,entities_list):

        entities_List_Json = []
        for i in range(len(entities_list)):
            entities_Json = {}
            for j in range(len(entities_list[i])):
                split_indices = []
                wordStartIndex = entities_list[i][j][0]
                wordEndIndex = entities_list[i][j][1]
                label = entities_list[i][j][2]
                if label in self.whichLabelKeep:
                    split_indices.append(f"{wordStartIndex};{wordEndIndex}")
                    entities_Json.setdefault(label, []).extend(split_indices)
                else:
                    pass
            entities_List_Json.append(json.dumps(entities_Json, ensure_ascii=False))

        return entities_List_Json

    def mainConvert(self):
        if self.ifDivide:
            for phase in ["train", "dev", "test"]:
                raw_file_path = os.path.join(self.raw_dir, f"{phase}.json")
                output_file_path = os.path.join(self.mrc_dir, self.queryname, f"mrc-ner-{self.dataname}.{phase}")
                query_list_path = os.path.join(self.query_list, f"{self.queryname}.json")
                self.convertTransform(raw_file_path, output_file_path, query_list_path)
        else:
            # train
            raw_file_path = os.path.join(self.raw_dir, f"{self.dataname}.jsonl")
            output_file_path = os.path.join(self.mrc_dir, f"{self.queryname}_{self.dataname}", f"mrc-ner{self.dataname}.train")
            query_list_path = os.path.join(self.query_list, f"{self.queryname}.json")
            self.convertTransform(raw_file_path, output_file_path, query_list_path, [0, 400])
            # dev
            raw_file_path = os.path.join(self.raw_dir, f"{self.dataname}.jsonl")
            output_file_path = os.path.join(self.mrc_dir, f"{self.queryname}_{self.dataname}", f"mrc-ner{self.dataname}.dev")
            query_list_path = os.path.join(self.query_list, f"{self.queryname}.json")
            self.convertTransform(raw_file_path, output_file_path, query_list_path, [400, 450])
            # test
            raw_file_path = os.path.join(self.raw_dir, f"{self.dataname}.jsonl")
            output_file_path = os.path.join(self.mrc_dir, f"{self.queryname}_{self.dataname}", f"mrc-ner{self.dataname}.test")
            query_list_path = os.path.join(self.query_list, f"{self.queryname}.json")
            self.convertTransform(raw_file_path, output_file_path, query_list_path, [450, 600])


    def convertTransform(self,raw_file_path, output_file_path, query_list, lineStartEnd=None):

        all_raw_line_data = [json.loads(line) for line in open(raw_file_path)] # 每一行数据读取，并解析成JSON，将所有JSON对象保存到一个列表
        tag2query_all = json.load(open(query_list))
        tag2query_filter = {k: v for k, v in tag2query_all.items() if k in self.whichLabelKeep}

        output = []
        origin_count = 0
        new_count = 0
        for raw_line_data in all_raw_line_data[lineStartEnd[0]:lineStartEnd[1]]:
            origin_count += 1
            context_mutilList = raw_line_data['sentences'] # SCIRec中原始的文本 [["English", "is", "shown"...
            entities_list = raw_line_data['ner']

            entities_List_Json = self.entitiesList2Json(entities_list)

            # ----------- 将SCIRec中 [["English", "is", "shown"... 转为
            for i,context_sublist in enumerate(context_mutilList):
                context = " ".join(context_sublist)
                print(context)
                # TODO
                for tag_idx, (tag, query) in enumerate(tag2query_filter.items()):
                    positions = json.loads(entities_List_Json[i]).get(tag, [])
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

            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

            json.dump(output, open(output_file_path, "w"), ensure_ascii=False, indent=2)
            print(f"Convert {origin_count} samples to {new_count} samples and save to {output_file_path}")














