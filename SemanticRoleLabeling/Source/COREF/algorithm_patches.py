from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

import numpy as np

from coref_config import *


class QuickUnion(object):
    ids = [] 
    size = []
    total_merge_cluster_ids = list()

    def __init__(self, total_merge_cluster_ids):
        print("Performing Quick Union Algorithm...")
        # initialize
        self.ids = []
        self.size = []
        self.total_merge_cluster_ids = list()
        # [[1,2], [2,3], [4]]
        # ids [0, 1, 2]
        self.total_merge_cluster_ids = total_merge_cluster_ids
        for i in range(len(total_merge_cluster_ids)):
            self.ids.append(i)

    def intersect(self, p, q):
        if len(p) < len(q):
            min_ = p
            max_ = q
        else:
            min_ = q
            max_ = p

        for element in min_:
            if element in max_:
                return True
        return False

    def union_find(self):
        for i in range(len(self.total_merge_cluster_ids)):
            for j in range(i+1, len(self.total_merge_cluster_ids)):
                if (self.intersect(self.total_merge_cluster_ids[i], self.total_merge_cluster_ids[j])):
                    self.union(i, j)
        tmp_total_merge_cluster_ids = [set() for _ in range(len(self.total_merge_cluster_ids))]

        for i in range(len(self.ids)):
            parent = self.find(i)
            for cluster_id in self.total_merge_cluster_ids[i]:
                tmp_total_merge_cluster_ids[parent].add(cluster_id)
        
        new_total_merge_cluster_ids = list()
        for cluster in tmp_total_merge_cluster_ids:
            if cluster:
                new_total_merge_cluster_ids.append(list(cluster))
        return new_total_merge_cluster_ids

    def union(self, p, q):
        idp = self.find(p)
        idq = self.find(q)
        if not self.connected(p, q):
            self.ids[idp] = idq

    def find(self, p):
        while(p != self.ids[p]):
            p = self.ids[p]
        return p

    def connected(self, p, q):
        if self.find(p) == self.find(q):
            return True
        else:
            return False


def get_stop_list():
    stop_list = stopwords.words('english')
    return stop_list


def is_merge_key(span):
    stop_list = get_stop_list()
    if span.lower() in stop_list:
        return False
    else:
        return True


def get_merge_ids(cluster, ids, i):
    merge_ids = set()
    for span in cluster:
        if span in ids:
            if ids[span] != i:
                if is_merge_key(span):
                    merge_ids.add(ids[span])
        else:
            ids[span] = i

    merge_ids.add(i)
    return list(merge_ids)


def remove_stop_words(clusters):
    stop_list = get_stop_list()

    for j in range(len(clusters)):
        cluster = clusters[j]
        clusters[j] = []
        for span in cluster:
            if not span.lower() in stop_list:
                clusters[j].append(span)
    return clusters


def merge(clusters):
    clusters = remove_stop_words(clusters)

    span_to_cluster_ids = dict() # first span -> cluster_id mapping, do not care second same span
    total_merge_cluster_ids = list()
    merged_clusters = list()

    for i in range(len(clusters)):
        cluster = clusters[i]

        merge_ids = get_merge_ids(cluster, span_to_cluster_ids, i) #ids is mutable
        if merge_ids:
            total_merge_cluster_ids.append(merge_ids)

    # [[1,2], [2,3], [4]]
    qu = QuickUnion(total_merge_cluster_ids)
    new_total_merge_cluster_ids = qu.union_find()
  
    # [[1,2,3], [4]]
    for cluster_ids in new_total_merge_cluster_ids:
        tmp_cluster = list()
        for cluster_id in cluster_ids:
            tmp_cluster.extend(clusters[cluster_id])
        merged_clusters.append(tmp_cluster)

    return merged_clusters


def longest_span(cluster):
    max_len = -1
    center_word = str()
    num_of_center_word = 0
    specific_words_for_cluster = list()

    stop_list = get_stop_list()

    for span in cluster:
        if span.lower() in stop_list:
            continue
        if span == center_word:
            num_of_center_word += 1

        if len(span) > max_len:
            max_len = len(span)
            center_word = span
            num_of_center_word = 1

    specific_words_for_cluster.append(center_word)

    return center_word, num_of_center_word, specific_words_for_cluster


'''
Algorithm: word_net algorithm 
Goal: to find specific word and center word
Implementation:
if span is a stop word, it should be a generic word
if span in the cluster is in the word net, then it is a generic word
else it could be a specific word

'''
def word_net(cluster):
    # specific words are those not exist in the word net
    # word net words are generic words
    stop_list = get_stop_list()

    specific_words = dict()
    specific_words_for_cluster = list()

    for span in cluster:
        if span.lower() in stop_list:
            continue

        if not wn.synsets(span):
            specific_words_for_cluster.append(span)

            if span in specific_words:
                specific_words[span] += 1
            else:
                specific_words[span] = 1
    
    center_word = str()
    num_of_center_word = -1

    for key, value in specific_words.items():
        if value > num_of_center_word:
            center_word = key
            num_of_center_word = value
        elif value == num_of_center_word:
            if len(key) > len(center_word):
                center_word = key

    return center_word, num_of_center_word, specific_words_for_cluster


def load_name_entities():
    name_entities = set()
    ner = np.load(ne_file_path)
    for nes in ner.flat:
        for e2 in nes:
            combine_ne = str()
            combine_type = str()
            for e3 in e2:
                ne = e3[0]
                ne_type = e3[1]

                name_entities.add(ne)
                if ne_type == 'O':
                    continue

                if not combine_type:
                    combine_type = ne_type
                    combine_ne = ne

                elif ne_type == combine_type:
                    combine_ne += ' ' + ne

                else: # meet a new type 
                    combine_type = ne_type
                    if combine_ne:
                        name_entities.add(combine_ne)
                    combine_ne = ne
            if combine_ne:
                name_entities.add(combine_ne)

    return name_entities


# specific words for cluster: those in the name entity
# center word in specific words: longest word
def name_entity(cluster):
    name_entities = load_name_entities()

    specific_words = dict()
    specific_words_for_cluster = list()

    for span in cluster:
        if not span in name_entities:
            continue

        specific_words_for_cluster.append(span)

        if span in specific_words:
            specific_words[span] += 1
        else:
            specific_words[span] = 1
    
    center_word = str()
    num_of_center_word = -1

    for key, value in specific_words.items():
        if value > num_of_center_word:
            center_word = key
            num_of_center_word = value
        elif value == num_of_center_word:
            if len(key) > len(center_word):
                center_word = key

    return center_word, num_of_center_word, specific_words_for_cluster


def get_center_words_for_cluster(cluster, center_word_selection):
    if center_word_selection == 'LongestSpan':
        return longest_span(cluster)
    if center_word_selection == 'NameEntity':
        return name_entity(cluster)
    if center_word_selection == 'WordNet':
        return word_net(cluster)