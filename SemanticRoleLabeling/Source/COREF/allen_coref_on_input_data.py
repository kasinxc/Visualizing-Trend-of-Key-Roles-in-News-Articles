# allennlp
from allennlp.predictors.predictor import Predictor
from tqdm import tqdm
import json
import os
import string

from utils import *
from coref_config import *


def loadCorefPredictor():
    print("loading predictor...")
    predictor = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/coref-model-2018.02.05.tar.gz")
    print("successfully loaded the predictor")
    return predictor


def have_punctuation(input_data):
    punctuations = string.punctuation
    for p in punctuations:
        if p in input_data:
            return True
    return False


# Output Tmp Files
def applyAllenToDP(input_data_points):
    global data_low_index, data_high_index

    predictor = loadCorefPredictor()

    if not os.path.exists(coref_result_file_path):
        os.makedirs(coref_result_file_path)
    
    pbar = tqdm(range(data_low_index, data_high_index)) # process bar

    skip_article_ids = list()
    for index in range(data_low_index, data_high_index):

        pbar.update(1)
        
        dp = input_data_points[index]

        if use_steplines_format == False and (index+1) in end_error_indice:
            continue
        elif use_steplines_format == True and int(dp.article_ids) in end_error_indice:
            continue

        
        if not have_punctuation(dp.reduced_title_desc):
            skip_article_ids.append(dp.article_ids)
            continue

        with open(coref_result_file_path + str(input_data_points[index].article_ids) + ".json", 'w') as f:
            
            # print("predicting file: " + coref_result_file_path + str(index+1) + ".json")
            # print("article id: " + str(dp.article_ids))
            # print("predicting data: " + dp.title_desc)
            coref = predictor.predict(document=dp.reduced_title_desc)
            json.dump(coref, f)

    pbar.close()
    print("skipped article ids due to no punctuation")
    print(skip_data_indice)


if __name__ == '__main__':
    global use_steplines_format
    if use_steplines_format == True:
        input_data_points = readFileFromSteplines(input_data_file_path)
    else:
        input_data_points = readFileFromTrump(input_data_file_path)
    applyAllenToDP(input_data_points)
