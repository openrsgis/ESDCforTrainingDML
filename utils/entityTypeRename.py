# -*- coding: utf-8 -*-
# @Time    : 2023/8/5 18:35

import json

class entitytypeRenameClass:
    def __init__(self, input_file, output_path, renameConfig_file_path):
        self.input_file = input_file
        self.output_path = output_path
        self.renameConfig_file_path =renameConfig_file_path

    def toRename(self):
        new_data_list = []
        entity_types = set()
        with open(self.input_file, 'r') as input_file:
            for line in input_file:
                data = json.loads(line.strip())
                ner_data = data["ner"]

                for entity_list in ner_data:
                    for entity in entity_list:
                        entity_type = entity[-1]
                        entity_types.add(entity_type)

                # for entity_list in ner_data:
                #     for entity in entity_list:
                #         if entity[-1] == "data products name":
                #             entity[-1] = "dataProductsName"

                new_data_list.append(data)

        entity_types_list = list(entity_types)

        # Step 2: Read and process the external file containing entity type replacement mapping
        with open(self.renameConfig_file_path, 'r') as external_file:
            entity_replacement_mapping = json.load(external_file)

        # Check if all entity types in the data match the ones in the external file
        if set(entity_replacement_mapping.keys()) != set(entity_types_list):
            print("Error: Entity types in the data do not match the ones in the external file.")
            print("Please check the external file for correct mapping.")
        else:
            # Perform entity type replacement
            for data in new_data_list:
                ner_data = data["ner"]
                for entity_list in ner_data:
                    for entity in entity_list:
                        original_entity_type = entity[-1]
                        replacement_entity_type = entity_replacement_mapping[original_entity_type]
                        entity[-1] = replacement_entity_type

            # Save the new jsonl file
            with open(self.output_path, 'w') as output_file:
                for data in new_data_list:
                    json.dump(data, output_file)
                    output_file.write('\n')

            print("New jsonl file has been saved.")

