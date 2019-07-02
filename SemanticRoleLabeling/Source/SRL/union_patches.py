from srl_config import *
from color_print import *

class QuickUnionForList(object):
    parent_ids = [] 
    items = []

    def __init__(self, list_of_elements):
        self.parent_ids = []
        self.items = []
        self.items = list_of_elements
        for i in range(len(self.items)):
            self.parent_ids.append(i)

    def connected(self, p, q):
        if self.find(p) == self.find(q):
            return True
        else:            
            return False

    def find(self, p):
        while (p != self.parent_ids[p]):
            p = self.parent_ids[p]
        return p

    def union(self,p,q):
        idq = self.find(q)
        idp = self.find(p)
        if not self.connected(p,q):
            self.parent_ids[idp]=idq


    def union_find_by_tfidf(self, verb, object_to_tfidf_mappings, tfidf_threshold):
        for i in range(len(self.items)):
            obj1 = self.items[i]
            for j in range(i+1, len(self.items)):
                obj2 = self.items[j]
                if object_to_tfidf_mappings[obj1] != 0 and object_to_tfidf_mappings[obj2] != 0 and (abs(object_to_tfidf_mappings[obj1] - object_to_tfidf_mappings[obj2]) <= tfidf_threshold):
                    print(UseStyle("Under '" + verb + "' Merging: " + obj1 + "("+ str(object_to_tfidf_mappings[obj1]) + ") & " + obj2 + "(" + str(object_to_tfidf_mappings[obj2]) + ")", fore="yellow"))
                    self.union(i, j)

        # build new items which is object_under_certain_verb here.
        # list of lists of objs
        new_object_under_certain_verb = list()

        parent_id_to_objs_mapping = dict()
        for i in range(len(self.parent_ids)):
            parent = self.find(i)
            if parent not in parent_id_to_objs_mapping:
                parent_id_to_objs_mapping[parent] = list()
            parent_id_to_objs_mapping[parent].append(self.items[i])

        for parent_id, objs in parent_id_to_objs_mapping.items():
            new_object_under_certain_verb.append(objs)

        return new_object_under_certain_verb


    def union_find_by_word2vec(self, word2vec_model, word2vec_similarity_threshold):
        for i in range(len(self.items)):
            verb1 = self.items[i]
            if verb1 not in word2vec_model.wv.vocab:
                continue
            for j in range(i+1, len(self.items)):
                verb2 = self.items[j]
                if verb2 not in word2vec_model.wv.vocab:
                    continue
                similar = word2vec_model.similarity(verb1, verb2)
                if similar > word2vec_similarity_threshold:
                    print(UseStyle("Merging " + verb1 + " & " + verb2  + ": " + str(similar), fore="pink"))
                    self.union(i, j)

        # build new items which is verbs_under_certain_subject here
        # list of lists of objs
        new_verbs_under_certain_subject = list()
        parent_id_to_verbs_mapping = dict()
        

        for i in range(len(self.parent_ids)):
            parent = self.find(i)
            if parent not in parent_id_to_verbs_mapping:
                parent_id_to_verbs_mapping[parent] = list()
            parent_id_to_verbs_mapping[parent].append(self.items[i])

        parent_id_to_head_verbs_mapping = dict()
        for parent_id, verbs in parent_id_to_verbs_mapping.items():
            head_verb = str()
            for v in verbs:
                if len(v) > len(head_verb):
                    head_verb = v
            parent_id_to_head_verbs_mapping[parent_id] = head_verb

        verbs_to_head_verb_mapping = dict()
        for i in range(len(self.items)):
            verb = self.items[i]
            parent = self.find(i)
            verbs_to_head_verb_mapping[verb] = parent_id_to_head_verbs_mapping[parent]

        return verbs_to_head_verb_mapping





