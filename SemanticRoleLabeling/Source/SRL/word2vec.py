import os 
import gensim
import json

from srl_config import *

def build_training_data_from_file(input_data_file_path):
    training_data = list()
    with open(input_data_file_path, 'r') as f:
        lines = f.readlines()
        for data_index in range(len(lines)):
            line = lines[data_index]

            tmp = line.strip('\n').split('\t')
            title_desc = tmp[0]
            artileIds = tmp[1]
            training_data.append(gensim.utils.simple_preprocess(title_desc))
    
    return training_data

def build_training_data_from_folder(input_data_file_path):
    training_data = list()
    for root, dirs, files in os.walk(input_data_file_path, topdown=False):
        for file_name in files:
            if '.' in file_name:
                continue
            file_path = os.path.join(root, file_name)
            print(file_path)
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for data_index in range(len(lines)):
                    line = lines[data_index]

                    tmp = line.strip('\n').split('\t')
                    title_desc = tmp[2]
                    artileIds = tmp[0]
                    training_data.append(gensim.utils.simple_preprocess(title_desc))
    
    return training_data


def get_word2vec_model(word2vec_model_file_path):
    model = None
    if os.path.exists(word2vec_model_file_path):
        model = gensim.models.Word2Vec.load(word2vec_model_file_path)
    if not model:
        if use_steplines_format:
            sentences = build_training_data_from_folder(input_data_file_path)
        else:
            sentences = build_training_data_from_file(input_data_file_path)

        if sentences:
            model = gensim.models.Word2Vec(sentences, size=150, window=10, min_count=1, workers=10, iter=10)
            model.train(sentences, total_examples = len(sentences), epochs = model.iter)
            model.save(word2vec_model_file_path)
    return model

# model = get_word2vec_model(word2vec_model_file_path)
# print(model.similarity('trump', 'obama'))

# result = model.most_similar('criticize')
# for each in result:
#     print(each[0]),
#     print(each[1])