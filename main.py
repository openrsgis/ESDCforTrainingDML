# -*- coding: utf-8 -*-
# @Time    : 2023/6/15 21:53

import argparse
# from paddlenlp.trainer.argparser import strtobool
from utils.doccano2SCIRec import doccanoTransform
from utils.entityClassFiltering import entityClassFiltering
from utils.corpusDataStatistics import corpusDataStatistics
from utils.viewCheck import viewCheck
from utils.toTrainData import toTrainData
from utils.entityTypeRename import entitytypeRenameClass
import datetime

def Doccano2SCIRec(doccano_file,identify, ifDeleteSomeLabel):
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    default_output_file = f"./data/SCIercData/data_{identify}_{current_time}.jsonl"        
    filter_output_file = f"./data/SCIercData/filterData_{identify}_{current_time}.jsonl"

    parser = argparse.ArgumentParser()
    parser.add_argument("--doccano_file", default=doccano_file, type=str, help="The doccano file exported from doccano platform.")
    parser.add_argument("--output_file", default=default_output_file, type=str, help="The path of data that you wanna output.")
    parser.add_argument("--ifRandom", default=False, type=bool)
    parser.add_argument("--ifRename", default=True, type=bool)
    parser.add_argument("--renameConfig_file_path", default="./data/renameConfig_seven.json", type=str)
    parser.add_argument("--seed", type=int, default=1000)
    parser.add_argument("--ifDeleteHttpLine", type=bool, default=True)
    parser.add_argument("--ifReplaceAbbrev", type=bool, default=True)
    parser.add_argument("--ifDeleteOtherSpatialAndOtherTime", type=bool, default=True)
    parser.add_argument("--ifDeleteotherLabel_selfDefined", type=bool, default=True)
    parser.add_argument("--ifDeleteSomeLabel", type=bool, default=ifDeleteSomeLabel)
    parser.add_argument("--ifDeleteNestedSpatial", type=bool, default=True)
    parser.add_argument("--ifDeleteOnlyDataProductsName", type=bool, default=True)
    parser.add_argument("--ifDeleteUnusedAbbreviation", type=bool, default=True)
    parser.add_argument("--filter_output_file", default=filter_output_file, type=str)

    parser.add_argument("--ifTransform", type=bool, default=True)
    args = parser.parse_args()


    transform = doccanoTransform(args.doccano_file, args.output_file, args.ifDeleteHttpLine, args.ifReplaceAbbrev)
    transform.mainTransform()

    filtering = entityClassFiltering(args.output_file, args.filter_output_file, args.ifDeleteOtherSpatialAndOtherTime, args.ifDeleteNestedSpatial, args.ifDeleteOnlyDataProductsName, args.ifDeleteUnusedAbbreviation, args.ifDeleteotherLabel_selfDefined, args.ifDeleteSomeLabel, args.ifRandom)
    filtering.mainFiltering()
    if args.ifRename:
        rename = entitytypeRenameClass(args.filter_output_file, args.filter_output_file, args.renameConfig_file_path)
        rename.toRename()

    return args.filter_output_file

def describeData(input_file):

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", default=input_file, type=str, help="The path of data that you wanna output.")
    parser.add_argument("--basicStatistics", type=bool, default=True, help="计算abstract总数，标记实体总数，实体类型总数")
    parser.add_argument("--totalNumberClassified", type=bool, default=True, help="分类计算实体类型的总个数")
    parser.add_argument("--averageLengthOfEntityTypes", type=bool, default=False, help="计算有误暂时设置为False，现代码计算了每篇文献中实体的计算实体类型的平均长度")
    parser.add_argument("--averageNumberOfEntityTypes", type=bool, default=True, help="计算每篇文献中平均的实体个数")
    parser.add_argument("--totalNumberOfNestedEntities", type=bool, default=True, help="计算嵌套实体的总个数")
    parser.add_argument("--totalNumberOfDiscontinuousEntities", type=bool, default=True, help="计算非连续实体的总个数")
    args = parser.parse_args()

    datadescribe = corpusDataStatistics(args.input_file, args.basicStatistics, args.totalNumberClassified,args.averageLengthOfEntityTypes, args.averageNumberOfEntityTypes, args.totalNumberOfNestedEntities, args.totalNumberOfDiscontinuousEntities)
    datadescribe.multiple_statistics()

def viewData(input_file, eachnumber2View):

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", default=input_file, type=str.")
    parser.add_argument("--eachnumber2View", default=eachnumber2View, type=int)
    args = parser.parse_args()

    view2Check = viewCheck(args.input_file, args.eachnumber2View)
    view2Check.view()
    pass


def SCIRec2TraningData(input_file, toDataType, timeuuid):

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", default=input_file, type=str, help="The path of data that you wanna output.")
    parser.add_argument("--output_path", default='./result/', type=str, help="The path of data that you wanna output.")

    parser.add_argument("--splits", default=[0.8, 0.1, 0.1], type=float)
    parser.add_argument("--toDataType", default=toDataType, type=str)
    args = parser.parse_args()

    startToTrainData = toTrainData(args.input_file, args.output_path, args.toDataType, timeuuid)
    startToTrainData.transfor2TrainData()

    pass



if __name__ == '__main__':

    filepath = "./data/rawData/all.jsonl"
    identify = "all"
    ifDeleteSomeLabel = True  
    SCIerc_output_file = Doccano2SCIRec(filepath, identify, ifDeleteSomeLabel)   




