import json
import re
import numpy as np


class corpusDataStatistics:
    def __init__(self, output_file, basicStatistics, totalNumberClassified, averageLengthOfEntityTypes, averageNumberOfEntityTypes, totalNumberOfNestedEntities, totalNumberOfDiscontinuousEntities):
        self.output_file = output_file
        self.basicStatistics = basicStatistics
        self.totalNumberClassified = totalNumberClassified
        self.averageLengthOfEntityTypes = averageLengthOfEntityTypes
        self.averageNumberOfEntityTypes = averageNumberOfEntityTypes
        self.totalNumberOfNestedEntities = totalNumberOfNestedEntities
        self.totalNumberOfDiscontinuousEntities = totalNumberOfDiscontinuousEntities
        self.totalNumberOfEntity = 0


    def multiple_statistics(self):

        if self.basicStatistics:
            self.calculate_basicStatistics()
        if self.totalNumberClassified:
            self.calculate_totalNumberClassified()
        if self.averageLengthOfEntityTypes:
            self.calculate_averageLengthOfEntityTypes()
        if self.averageNumberOfEntityTypes:
            self.calculate_averageNumberOfEntityTypes()
        if self.totalNumberOfNestedEntities:
            self.calculate_totalNumberOfNestedEntities()
        if self.totalNumberOfDiscontinuousEntities:
            self.calculate_totalNumberOfDiscontinuousEntities()

    def calculate_basicStatistics(self):
        totalNumberOfEntity = 0  
        entityTypeList = []
        n = 0
        number_sentecne = 0
        output_data = open(self.output_file, 'r', encoding='utf-8')
        for line in output_data.readlines():
            dic = json.loads(line)  
            processed_ner = dic['ner']  
            processed_sentences = dic['sentences'] 
            number_sentecne += len(processed_sentences)
            totalNumberOfEachArticle = 0
            for i in range(len(processed_ner)):
                if processed_ner[i] != []:
                    for j in range(len(processed_ner[i])):
                        totalNumberOfEntity += 1
                        totalNumberOfEachArticle += 1
                        # entity type
                        type = processed_ner[i][j][-1]
                        if type not in entityTypeList:
                            entityTypeList.append(type)

            n += 1
        self.totalNumberOfEntity = totalNumberOfEntity  # 方便后续调用
        typeNumber = len(entityTypeList)
        print(f"数据集中包含的文献摘要总数为：{n}")
        print(f"数据集中包含的句子总数为：{number_sentecne}")
        print(f"数据集中包含的实体类型的总个数为：{typeNumber},实体类型包含{entityTypeList}")
        print(f"所有文献中实体类型的总个数为：{totalNumberOfEntity}")


    def calculate_totalNumberClassified(self):
        na_data_products_name, na_Object, na_Variables, na_application, na_raw_data_name, na_sensor, na_method, na_spatial, na_time, na_other, na_abbreviation, na_do_application, na_other_spatial, na_other_time, na_Time_resolution, na_spatial_resolution, na_repository, na_organization = (0,) * 18
        m = 1
        output_data = open(self.output_file, 'r', encoding='utf-8')
        for line2 in output_data.readlines():
            dic2 = json.loads(line2)  
            processed_ner2 = dic2['ner']  
            
            ne_data_products_name, ne_Object, ne_Variables, ne_application, ne_raw_data_name, ne_sensor, ne_method, ne_spatial, ne_time, ne_other, ne_abbreviation, ne_do_application, ne_other_spatial, ne_other_time, ne_Time_resolution, ne_spatial_resolution, ne_repository, ne_organization = (0,) * 18
            for i in range(len(processed_ner2)):
                if processed_ner2[i] != []:
                    for j in range(len(processed_ner2[i])):
                        if len(processed_ner2[i][j]) == 3:
                            if processed_ner2[i][j][2] == 'dataProductsName':
                                ne_data_products_name += 1
                                na_data_products_name += 1
                            if processed_ner2[i][j][2] == 'Object':
                                ne_Object += 1
                                na_Object += 1
                            if processed_ner2[i][j][2] == 'Variables':
                                ne_Variables += 1
                                na_Variables += 1
                            if processed_ner2[i][j][2] == 'application':
                                ne_application += 1
                                na_application += 1
                            if processed_ner2[i][j][2] == 'rawDataName':
                                ne_raw_data_name += 1
                                na_raw_data_name += 1
                            if processed_ner2[i][j][2] == 'sensor':
                                ne_sensor += 1
                                na_sensor += 1
                            if processed_ner2[i][j][2] == 'method':
                                ne_method += 1
                                na_method += 1
                            if processed_ner2[i][j][2] == 'spatial':
                                ne_spatial += 1
                                na_spatial += 1
                            if processed_ner2[i][j][2] == 'time':
                                ne_time += 1
                                na_time += 1
                            if processed_ner2[i][j][2] == 'other':
                                ne_other += 1
                                na_other += 1
                            if processed_ner2[i][j][2] == 'abbreviation':
                                ne_abbreviation += 1
                                na_abbreviation += 1
                            if processed_ner2[i][j][2] == 'doApplication':
                                ne_do_application += 1
                                na_do_application += 1
                            if processed_ner2[i][j][2] == 'otherSpatial':
                                ne_other_spatial += 1
                                na_other_spatial += 1
                            if processed_ner2[i][j][2] == 'otherTime':
                                ne_other_time += 1
                                na_other_time += 1
                            if processed_ner2[i][j][2] == 'Time resolution':
                                ne_Time_resolution += 1
                                na_Time_resolution += 1
                            if processed_ner2[i][j][2] == 'spatial resolution':
                                ne_spatial_resolution += 1
                                na_spatial_resolution += 1
                            if processed_ner2[i][j][2] == 'repository':
                                ne_repository += 1
                                na_repository += 1
                            if processed_ner2[i][j][2] == 'organization':
                                ne_organization += 1
                                na_organization += 1
                        if len(processed_ner2[i][j]) == 5:
                            if processed_ner2[i][j][4] == 'data products name':
                                ne_data_products_name += 1
                                na_data_products_name += 1
                            if processed_ner2[i][j][4] == 'Object':
                                ne_Object += 1
                                na_Object += 1
                            if processed_ner2[i][j][4] == 'Variables':
                                ne_Variables += 1
                                na_Variables += 1
                            if processed_ner2[i][j][4] == 'application':
                                ne_application += 1
                                na_application += 1
                            if processed_ner2[i][j][4] == 'raw data name':
                                ne_raw_data_name += 1
                                na_raw_data_name += 1
                            if processed_ner2[i][j][4] == 'sensor':
                                ne_sensor += 1
                                na_sensor += 1
                            if processed_ner2[i][j][4] == 'method':
                                ne_method += 1
                                na_method += 1
                            if processed_ner2[i][j][4] == 'spatial':
                                ne_spatial += 1
                                na_spatial += 1
                            if processed_ner2[i][j][4] == 'time':
                                ne_time += 1
                                na_time += 1
                            if processed_ner2[i][j][4] == 'other':
                                ne_other += 1
                                na_other += 1
                            if processed_ner2[i][j][4] == 'abbreviation':
                                ne_abbreviation += 1
                                na_abbreviation += 1
                            if processed_ner2[i][j][4] == 'do application':
                                ne_do_application += 1
                                na_do_application += 1
                            if processed_ner2[i][j][4] == 'other_spatial':
                                ne_other_spatial += 1
                                na_other_spatial += 1
                            if processed_ner2[i][j][4] == 'other_time':
                                ne_other_time += 1
                                na_other_time += 1
                            if processed_ner2[i][j][4] == 'Time resolution':
                                ne_Time_resolution += 1
                                na_Time_resolution += 1
                            if processed_ner2[i][j][4] == 'spatial resolution':
                                ne_spatial_resolution += 1
                                na_spatial_resolution += 1
                            if processed_ner2[i][j][4] == 'repository':
                                ne_repository += 1
                                na_repository += 1
                            if processed_ner2[i][j][4] == 'organization':
                                ne_organization += 1
                                na_organization += 1
            # 每篇文献分类统计的结果
            # print(f"第 {m} 篇文献中实体类型”data products name”的总个数为：{ne_data_products_name}")
            # print(f"第 {m} 篇文献中实体类型”Object”的总个数为：{ne_Object}")
            # print(f"第 {m} 篇文献中实体类型”Variables”的总个数为：{ne_Variables}")
            # print(f"第 {m} 篇文献中实体类型”application”的总个数为：{ne_application}")
            # print(f"第 {m} 篇文献中实体类型”raw data name”的总个数为：{ne_raw_data_name}")
            # print(f"第 {m} 篇文献中实体类型”sensor”的总个数为：{ne_sensor}")
            # print(f"第 {m} 篇文献中实体类型”method”的总个数为：{ne_method}")
            # print(f"第 {m} 篇文献中实体类型”spatial”的总个数为：{ne_spatial}")
            # print(f"第 {m} 篇文献中实体类型”time”的总个数为：{ne_time}")
            # print(f"第 {m} 篇文献中实体类型”other”的总个数为：{ne_other}")
            # print(f"第 {m} 篇文献中实体类型”abbreviation”的总个数为：{ne_abbreviation}")
            # print(f"第 {m} 篇文献中实体类型”do application”的总个数为：{ne_do_application}")
            # print(f"第 {m} 篇文献中实体类型”other_spatial”的总个数为：{ne_other_spatial}")
            # print(f"第 {m} 篇文献中实体类型”other_time”的总个数为：{ne_other_time}")
            # print(f"第 {m} 篇文献中实体类型”Time resolution”的总个数为：{ne_Time_resolution}")
            # print(f"第 {m} 篇文献中实体类型”spatial resolution”的总个数为：{ne_spatial_resolution}")
            # print(f"第 {m} 篇文献中实体类型”repository”的总个数为：{ne_repository}")
            # print(f"第 {m} 篇文献中实体类型”organization”的总个数为：{ne_organization}")
            m += 1
        # 所有文献的分类统计结果
        print(f"所有文献中实体类型”data products name”的总个数为：{na_data_products_name}")
        print(f"所有文献中实体类型”Object”的总个数为：{na_Object}")
        print(f"所有文献中实体类型”Variables”的总个数为：{na_Variables}")
        print(f"所有文献中实体类型”application”的总个数为：{na_application}")
        print(f"所有文献中实体类型”raw data name”的总个数为：{na_raw_data_name}")
        print(f"所有文献中实体类型”sensor”的总个数为：{na_sensor}")
        print(f"所有文献中实体类型”method”的总个数为：{na_method}")
        print(f"所有文献中实体类型”spatial”的总个数为：{na_spatial}")
        print(f"所有文献中实体类型”time”的总个数为：{na_time}")
        print(f"所有文献中实体类型”other”的总个数为：{na_other}")
        print(f"所有文献中实体类型”abbreviation”的总个数为：{na_abbreviation}")
        print(f"所有文献中实体类型”do application”的总个数为：{na_do_application}")
        print(f"所有文献中实体类型”other_spatial”的总个数为：{na_other_spatial}")
        print(f"所有文献中实体类型”other_time”的总个数为：{na_other_time}")
        print(f"所有文献中实体类型”Time resolution”的总个数为：{na_Time_resolution}")
        print(f"所有文献中实体类型”spatial resolution”的总个数为：{na_spatial_resolution}")
        print(f"所有文献中实体类型”repository”的总个数为：{na_repository}")
        print(f"所有文献中实体类型”organization”的总个数为：{na_organization}")

    def calculate_averageLengthOfEntityTypes(self):
        totalLength = 0
        averageLengthOfEntityTypes = 0
        output_data = open(self.output_file, 'r', encoding='utf-8')
        for line in output_data.readlines():
            dic = json.loads(line)  
            processed_ner = dic['ner']  
            for i in range(len(processed_ner)):
                if processed_ner[i] != []:
                    for j in range(len(processed_ner[i])):
                        if len(processed_ner[i][j]) == 3:
                            totalLength += processed_ner[i][j][1] - processed_ner[i][j][0] + 1
                        if len(processed_ner[i][j]) == 5:
                            totalLength += ((processed_ner[i][j][1] - processed_ner[i][j][0] + 1) + (processed_ner[i][j][3] - processed_ner[i][j][2] + 1))
        averageLengthOfEntityTypes = totalLength / 500
        print(f'所有实体类型对每篇文献的平均长度为：{averageLengthOfEntityTypes}')

    def calculate_averageNumberOfEntityTypes(self):
        totalNumberOfEntityTypes = 0  # 所有文献中所有实体类型的总个数
        output_data = open(self.output_file, 'r', encoding='utf-8')
        for line in output_data.readlines():
            dic = json.loads(line)  # 逐行转为json格式
            processed_ner = dic['ner']  # 提取出ner部分
            for i in range(len(processed_ner)):
                if processed_ner[i] != []:
                    for j in range(len(processed_ner[i])):
                        totalNumberOfEntityTypes += 1
        averageNumberOfEntityTypes = totalNumberOfEntityTypes / 500
        print(f"每篇文献中平均的实体个数为：{averageNumberOfEntityTypes}")


    def calculate_totalNumberOfNestedEntities(self):
        def count_nested_nest_entities(input_list,nested_count,nested_by_count):

            for sublist in input_list:
                for entity1, entity2 in sublist:
                    entity_type1 = entity1[2]
                    entity_type2 = entity2[2]

                    if entity_type1 in nested_count:
                        nested_count[entity_type1] += 1
                    else:
                        nested_count[entity_type1] = 1

                    if entity_type2 in nested_by_count:
                        nested_by_count[entity_type2] += 1
                    else:
                        nested_by_count[entity_type2] = 1

            return nested_count, nested_by_count

        def count_elements(input_list):
            num_elements = sum(len(t) for t in input_list)

            return num_elements

        def count_nested_entities_sub(entity_list):

            nested_entity_pairs = []

            for i, entity_A in enumerate(entity_list):
                if len(entity_A) == 5:
                    continue
                start_A, end_A, type_A = entity_A

                for j, entity_B in enumerate(entity_list):
                    if len(entity_B) == 5:
                        continue
                    start_B, end_B, type_B = entity_B

                    if i != j and start_A <= start_B and end_A >= end_B:
                        nested_entity_pairs.append((entity_A, entity_B))

            return len(nested_entity_pairs), nested_entity_pairs

        def count_nested_entities(ner_data, all_nested_entity_pairs, nested_count, nested_by_count):
            ner_list = ner_data["ner"]
            nested_entities = []
            stack = []



            all_nested_entity_pairs = []
            for sorted_ner in ner_list:
                all_nested_entity_pairs_for_nest = []
                len_nested_entity_pairs, nested_entity_pairs = count_nested_entities_sub(sorted_ner)
                all_nested_entity_pairs.append(nested_entity_pairs)
                all_nested_entity_pairs_for_nest.append(nested_entity_pairs)
                nested_count, nested_by_count = count_nested_nest_entities(all_nested_entity_pairs_for_nest, nested_count, nested_by_count)




            return count_elements(all_nested_entity_pairs), all_nested_entity_pairs, nested_count, nested_by_count

        # TODO
        total_NumberOfNestedEntities = 0  
        output_data = open(self.output_file, 'r', encoding='utf-8')
        nested_count = {}
        nested_by_count = {}
        all_nested_entity_pairs = []
        for line in output_data.readlines():
            dic = json.loads(line)  # 逐行转为json格式
            num_nested_entities, nested_entities_types, nested_count, nested_by_count = count_nested_entities(dic, all_nested_entity_pairs, nested_count, nested_by_count)
            total_NumberOfNestedEntities+=num_nested_entities

        print("实体类型的嵌套数量:", nested_count)
        print("实体类型的被嵌套数量:", nested_by_count)
        print(f"嵌套实体的总数为：{total_NumberOfNestedEntities}")


    def calculate_totalNumberOfDiscontinuousEntities(self):
        numberDiscontinuousEntities = 0
        output_data = open(self.output_file, 'r', encoding='utf-8')
        Discontinuous_count = {}
        for line in output_data.readlines():
            dic = json.loads(line)  # 逐行转为json格式
            ner_list = dic["ner"]
            for sorted_ner in ner_list:
                for ner in sorted_ner:
                    if len(ner)==5:
                        numberDiscontinuousEntities+=1
                        entity_type1 = ner[-1]
                        if entity_type1 in Discontinuous_count:
                            Discontinuous_count[entity_type1] += 1
                        else:
                            Discontinuous_count[entity_type1] = 1

        print(f"非连续实体的总数为：{numberDiscontinuousEntities}")
        print(f"非连续实体各个类型的数量：{Discontinuous_count}")



