# -*- coding: utf-8 -*-
# @Time    : 2023/8/5 15:34

from toTrainingData.SCIRec2bartner import SCIRec2bartnerClass
from toTrainingData.SCIerc2W2NER import SCIerc2W2NERClass
import datetime
import os

class toTrainData:
    def __init__(self, input_file, output_path, toDataType, timeuuid):
        self.input_file = input_file
        self.output_path = output_path
        self.toDataType = toDataType


        if timeuuid==None:
            current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M")
            self.createFolderPath = os.path.join(output_path,f"{self.toDataType}{current_time}")
        else:
            self.createFolderPath = os.path.join(output_path,f"{self.toDataType}{timeuuid}")

        self.train_file = os.path.join(self.createFolderPath,'train.txt')
        self.train_file = self.train_file.replace('/', '\\')  # 将正斜杠替换为反斜杠

        self.valid_file = os.path.join(self.createFolderPath,'dev.txt')
        self.valid_file = self.valid_file.replace('/', '\\')  # 将正斜杠替换为反斜杠

        self.test_file = os.path.join(self.createFolderPath,'test.txt')
        self.test_file = self.test_file.replace('/', '\\')  # 将正斜杠替换为反斜杠


    def transfor2TrainData(self):

        if self.toDataType == "BARTNER":

            os.makedirs(self.createFolderPath)
            createBartner = SCIRec2bartnerClass(self.input_file, self.output_path, self.train_file, self.valid_file, self.test_file)
            createBartner.SCIRec2bartner()
        if self.toDataType == "zhixi":
            os.makedirs(self.createFolderPath)

            pass
        if self.toDataType == "W2NER":

            os.makedirs(self.createFolderPath)
            createBartner = SCIerc2W2NERClass(self.input_file, self.train_file, self.valid_file, self.test_file)
            createBartner.SCIec2W2NERfunction()
        pass









