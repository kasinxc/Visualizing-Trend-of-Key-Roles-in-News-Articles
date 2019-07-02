from coref_config import *
import os

class dataPoint:
    def get_topic(self):
        probs = self.topic_prob[1:-1] # remove [ and ] in the beginning and end
        probs = probs.split(',')
        max_prob = -1.0
        if len(probs) != title_num:
            print("Input probabilities do not match with configed title number!")
        for i in range(len(probs)):
            prob = probs[i]
            if ' ' in prob:
                prob = prob.replace(' ', '')
            prob = float(prob)
            if max_prob < prob:
                max_prob = prob
                self.topic_order = i
        return self.topic_order

    def __init__(self, td, ai, tp):
        self.title_desc = td
        self.article_ids = ai
        self.topic_prob = tp

        if use_steplines_format == False:
            self.topic_order = self.get_topic()
        self.words_count = dict()
        self.verbs = list() # list of labelInfos
        self.reduced_title_desc = td
        while '  ' in self.reduced_title_desc:
            self.reduced_title_desc = self.reduced_title_desc.replace('  ', ' ')



input_data_points = list()


# input dataset
def getTopicInfo():
    topic_lines = list()
    for i in range(title_num):
        topic_lines.append(0)
    for dp in input_data_points:
        topic_lines[dp.topic_order]+=1

    # for i in range(title_num):
    #     print("There are " + str(topic_lines[i]) + " lines for topic: " + str(i))


def readFileFromTrump(file_path):
    print("reading file from path: " + file_path)
    input_data_points = list()
    with open(file_path, 'r') as f:
        line_index = 1
        for line in f.readlines():
            line_index += 1
            tmp = line.strip('\n').split('\t')
            dp = dataPoint(tmp[0], tmp[1], tmp[2])
            input_data_points.append(dp)
    
    getTopicInfo()
    print("successfully read the file")
    print("total news: " + str(len(input_data_points)))

    return input_data_points


def readFileFromSteplines(folder_path):
    # folder_path are like ./Data/6_month
    # tranverse all the data file inside 6_month
    input_data_points = list()
    print("reading file from path: " + folder_path)
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for name in files:
            if not '.' in name:
                file_path = os.path.join(root, name)
                with open(file_path, 'r') as f:
                    for line in f.readlines():
                        tmp = line.strip('\n').split('\t')
                        # print(tmp)
                        dp = dataPoint(tmp[2],tmp[0],0)
                        input_data_points.append(dp)

    print("successfully read the data folder")
    print("total news: " + str(len(input_data_points)))

    return input_data_points
