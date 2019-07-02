from graphviz import Digraph

import operator
import sys
sys.path.append('../COREF/')
import json
import math
import string

import word2vec as word2vec

from coref_visualization import *
from relation_extraction import *
from srl_config import *
from union_patches import *



def get_role_to_relations_of_interest_mappings(role_of_interest, relations):

    new_relations = dict()

    for relation in relations:
        if relation.subject in role_of_interest: 
            if not relation.subject in new_relations:
                new_relations[relation.subject] = list()
            new_relations[relation.subject].append(relation)
    return new_relations

def clean_punctuation(s):
    s = s.replace(' n\'t', 'n t')
    s = s.replace(' n’t', 'n t')
    s = s.translate(str.maketrans('-’\'', '   ', '!"#$%&()*+,./:;<=>?@[\\]^_`{|}~“”'))
    s = s.replace(u'\xa0', ' ')
    while '  ' in s:
        s = s.replace('  ', ' ')
    while s.endswith(' '):
        s = s[:-1]
    while s.startswith(' '):
        s = s[1:]
    return s


def get_tfidf_for_object(no_punctuation_input_title_desc, relation):
    # calculate tfidf for object in relation

    old_relation_object = relation.object
    old_articles = no_punctuation_input_title_desc[relation.article_ids]

    news_article = no_punctuation_input_title_desc[relation.article_ids]
    news_article = clean_punctuation(news_article)

    object_clean_format = relation.object
    object_clean_format = clean_punctuation(object_clean_format)


    tf = news_article.count(object_clean_format) * 1.0 / len(news_article.split())

    articles_contain_object = 0
    for ai, rtd in no_punctuation_input_title_desc.items():
        if object_clean_format in rtd:
            articles_contain_object += 1

    idf = math.log(len(no_punctuation_input_title_desc) / (articles_contain_object + 1))
    if tf*idf < 0.00001:
        print(UseStyle('[Warning] tfidf too low. Please double check the rules in function: clean_punctuation.', fore='red'))

    return tf * idf

def update_object_to_tfidf_mappings(no_punctuation_input_title_desc, relation, object_to_tfidf_mappings_under_verb):
    if not relation.verb in object_to_tfidf_mappings_under_verb:
        object_to_tfidf_mappings_under_verb[relation.verb] = dict()

    if not relation.object in object_to_tfidf_mappings_under_verb[relation.verb]:
        object_to_tfidf_mappings_under_verb[relation.verb][relation.object] = get_tfidf_for_object(no_punctuation_input_title_desc, relation)
    else:
        object_to_tfidf_mappings_under_verb[relation.verb][relation.object] = max(get_tfidf_for_object(no_punctuation_input_title_desc, relation), object_to_tfidf_mappings_under_verb[relation.verb][relation.object])
    return object_to_tfidf_mappings_under_verb


def update_verb_to_other_roles_mappings(relation, verb_counts, verb_to_other_roles_mappings):
    if not relation.verb in verb_counts:
        verb_counts[relation.verb] = 1
    else:
        verb_counts[relation.verb] += 1

    if not relation.verb in verb_to_other_roles_mappings:
        verb_to_other_roles_mappings[relation.verb] = dict()
    
    if not relation.object in verb_to_other_roles_mappings[relation.verb]:
        verb_to_other_roles_mappings[relation.verb][relation.object] = 1
    else:
        verb_to_other_roles_mappings[relation.verb][relation.object] += 1
    return verb_counts, verb_to_other_roles_mappings


def merge_object(verb_to_other_roles_mappings, object_to_tfidf_mappings_under_verb):
    # union find again
    global tfidf_threshold
    for verb, other_roles_mappings in verb_to_other_roles_mappings.items():

        objects_under_certain_verb = list()
        for obj, label in other_roles_mappings.items():
            objects_under_certain_verb.append(obj)
        # if len(objects_under_certain_verb) > 1:
            # print(UseStyle("Verb: " + verb, fore='red'))
            # print("All of the objects are: ")
            # print(object_to_tfidf_mappings_under_verb[verb])
            # print("------------")
        qu = QuickUnionForList(objects_under_certain_verb)
        objects_under_certain_verb = qu.union_find_by_tfidf(verb, object_to_tfidf_mappings_under_verb[verb], tfidf_threshold)

        for obj_cluster in objects_under_certain_verb:
            # get obj with highest tfidf score
            obj_with_highest_tfidf = str()
            highest_tfidf = -1
            for obj in obj_cluster:
                if object_to_tfidf_mappings_under_verb[verb][obj] > highest_tfidf:
                    highest_tfidf = object_to_tfidf_mappings_under_verb[verb][obj]
                    obj_with_highest_tfidf = obj
                if object_to_tfidf_mappings_under_verb[verb][obj] == highest_tfidf:
                    if len(obj) > len(obj_with_highest_tfidf):
                        obj_with_highest_tfidf = obj

            for obj in obj_cluster:
                if obj and obj != obj_with_highest_tfidf:
                    verb_to_other_roles_mappings[verb][obj_with_highest_tfidf] += verb_to_other_roles_mappings[verb][obj]
                    del verb_to_other_roles_mappings[verb][obj]

    return verb_to_other_roles_mappings


def merge_verb(verb_counts, verb_to_other_roles_mappings, object_to_tfidf_mappings_under_verb):
    global word2vec_similarity_threshold
    word2vec_model = word2vec.get_word2vec_model(word2vec_model_file_path)
    verbs_under_certain_subject = list()
    for verb, others in verb_to_other_roles_mappings.items():
        verbs_under_certain_subject.append(verb)
    if len(verbs_under_certain_subject) > 1:
        qu = QuickUnionForList(verbs_under_certain_subject)
        verbs_to_head_verb_mapping = qu.union_find_by_word2vec(word2vec_model, word2vec_similarity_threshold)
        # update all three dicts

        for v in verbs_under_certain_subject:
            head_v = verbs_to_head_verb_mapping[v]
            if v == head_v:
                continue

            verb_counts[head_v] += verb_counts[v]
            verb_counts.pop(v, None)

            for other_role, count in verb_to_other_roles_mappings[v].items():
                if other_role not in verb_to_other_roles_mappings[head_v]:
                    # other_role not exist in head_v
                    verb_to_other_roles_mappings[head_v][other_role] = verb_to_other_roles_mappings[v][other_role]
                    if enable_tfidf == True:
                        object_to_tfidf_mappings_under_verb[head_v][other_role] = object_to_tfidf_mappings_under_verb[v][other_role]
                else:
                    # other_role already exist in head_v
                    verb_to_other_roles_mappings[head_v][other_role] += verb_to_other_roles_mappings[v][other_role]
                    if enable_tfidf == True:
                        object_to_tfidf_mappings_under_verb[head_v][other_role] = max(object_to_tfidf_mappings_under_verb[head_v][other_role], object_to_tfidf_mappings_under_verb[v][other_role])

            verb_to_other_roles_mappings.pop(v, None)
            if enable_tfidf == True:
                object_to_tfidf_mappings_under_verb.pop(v, None)



def tree(relations, input_data_entries):
    role_to_relations_of_interest_mappings = get_role_to_relations_of_interest_mappings(role_of_interest, relations)
    
    tree_graph = Digraph(format='png')
    tree_graph.clear()
    tree_graph.attr(rankdir='LR')

    no_punctuation_input_title_desc = dict() # tfidf use
    for ai, de in input_data_entries.items():
        no_punctuation_input_title_desc[ai] = clean_punctuation(de.reduced_title_desc)

    for interested_role_name, relations_of_interest in role_to_relations_of_interest_mappings.items():
        # print(UseStyle("add interested node: " + interested_role_name, fore='green'))

        verb_counts = dict()
        verb_to_other_roles_mappings = dict() # currently just object

        object_to_tfidf_mappings_under_verb = dict() # verb -> obj -> tfidf use

        for relation in relations_of_interest:
            verb_counts, verb_to_other_roles_mappings = update_verb_to_other_roles_mappings(relation, verb_counts, verb_to_other_roles_mappings)

            if enable_tfidf == True:
                object_to_tfidf_mappings_under_verb = update_object_to_tfidf_mappings(no_punctuation_input_title_desc, relation, object_to_tfidf_mappings_under_verb)

            # get tfidf for each relation.object, if the difference falls within a certain threshold:
                # Merge them together!

        if enable_word_embedding == True:
            # print(UseStyle('Before', fore='red'))
            # print(verb_counts)
            merge_verb(verb_counts, verb_to_other_roles_mappings, object_to_tfidf_mappings_under_verb)
            # print(UseStyle('After', fore='green'))
            # print(verb_counts)

        sorted_verb_counts = sorted(verb_counts.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        # sorted_verb_counts = sorted(verb_counts.items(), key=lambda kv: kv[1], reverse=True)

        # if enable_tfidf == True:
            # print(UseStyle('This is tfidf score: ', fore='green'))
            # print(object_to_tfidf_mappings_under_verb)

        if enable_tfidf == True:
            verb_to_other_roles_mappings = merge_object(verb_to_other_roles_mappings, object_to_tfidf_mappings_under_verb)

        drew_verbs = set()
        for (verb_words, count) in sorted_verb_counts:
            verb_name = interested_role_name + '.' + verb_words
            if count >= min_verb_count_to_draw and count <= max_verb_count_to_draw:
                can_draw=False
                
                for other_role_words, other_role_count in verb_to_other_roles_mappings[verb_words].items():
                    if other_role_count >= min_verb_other_roles_count_to_draw and other_role_count <= max_verb_other_roles_count_to_draw:
                        can_draw=True
                        break

                if can_draw:
                    tree_graph.node(interested_role_name, interested_role_name, color='red')
                    tree_graph.node(verb_name, verb_words)
                    tree_graph.edge(interested_role_name, verb_name, label=str(count))
                    drew_verbs.add(verb_words)
                    if len(drew_verbs) >= top_ranking_verbs:
                        break

        for verb_words, other_roles_count in verb_to_other_roles_mappings.items():
            if not verb_words in drew_verbs:
                continue
            verb_name = interested_role_name + '.' + verb_words
            for other_role_words, count in other_roles_count.items():
                other_role_name = verb_name + '.' + other_role_words
                if count >= min_verb_other_roles_count_to_draw and count <= max_verb_other_roles_count_to_draw:
                    tree_graph.node(other_role_name, other_role_words)
                    tree_graph.edge(verb_name, other_role_name, label=str(count))

    return tree_graph


def get_lower(role_of_interest):
    lower_case_role_of_interest = list()
    for role in role_of_interest:
        lower_case_role_of_interest.append(role.lower())
    return lower_case_role_of_interest


def remove_duplicates_from_list(a):
    b = set()
    for aa in a:
        b.add(aa)
    a.clear()
    for bb in b:
        a.append(bb)


def load_configurations(configurations):
    global role_of_interest,min_verb_count_to_draw, min_verb_other_roles_count_to_draw, max_verb_count_to_draw, max_verb_other_roles_count_to_draw
    global max_file_number, top_ranking_verbs, max_length_of_role, enable_coreference_resolution, coref_read_from_correct_file
    global enable_inclusive_match_on_roles, enable_word_embedding, word2vec_similarity_threshold, enable_tfidf, tfidf_threshold

    for configuration in configurations:
        label = configuration[0]
        content = configuration[1]
        if label == 'interested_roles':
            role_of_interest = content
        if label == 'min_count_to_draw':
            min_verb_count_to_draw = content
            min_verb_other_roles_count_to_draw = content
        if label == 'max_count_to_draw':
            max_verb_count_to_draw = content
            max_verb_other_roles_count_to_draw = content
        if label == 'max_file_number':
            max_file_number = content
        if label == 'top_ranking_verbs':
            top_ranking_verbs = content
        if label == 'max_length_of_role':
            max_length_of_role = content
        if label == 'enable_coreference_resolution':
            enable_coreference_resolution = content
        if label == 'coref_read_from_correct_file':
            coref_read_from_correct_file = content
        if label == 'enable_inclusive_match_on_roles':
            enable_inclusive_match_on_roles = content
        if label == 'enable_lemmatizer':
            enable_lemmatizer = content

        if label == 'enable_word_embedding':
            enable_word_embedding = content
        if label == 'word2vec_similarity_threshold':
            word2vec_similarity_threshold = content
        if label == 'enable_tfidf':
            enable_tfidf = content
        if label == 'tfidf_threshold':
            tfidf_threshold = content



    if enable_coreference_resolution == True:
        clusters = get_clusters(coref_read_from_correct_file)
        lower_case_role_of_interest = get_lower(role_of_interest) 
        role_of_interest_from_coref = list()
        for cluster in clusters:
            role_in_cluster = False
            for word in cluster:
                if word.lower() in lower_case_role_of_interest:
                    role_in_cluster = True
                    break
            if role_in_cluster == True:
                for role in cluster:
                    if not role in role_of_interest:
                        role_of_interest_from_coref.append(role)
        
        remove_duplicates_from_list(role_of_interest_from_coref)
        role_of_interest.extend(role_of_interest_from_coref)
        remove_duplicates_from_list(role_of_interest)
        print(UseStyle("Added role of interest from coref: ", fore='yellow'))
        print(role_of_interest_from_coref)


# use when querying what search options we have
def show_all_arg0(relations):
    arg0 = set()
    for relation in relations:
        arg0.add(relation.subject)
    # set is not JSON serializable  
    arg0_list = list()          
    for a in arg0:
        arg0_list.append(a)

    with open('arg0', 'w') as f:
        json.dump(arg0_list, f)
    return arg0


def main(configurations):
    global enable_inclusive_match_on_roles

    load_configurations(configurations)
    relations, input_data_entries = get_relations_api(max_file_number)

    # add arg0s by containing role of interests

    if enable_inclusive_match_on_roles == True:
        arg0s = show_all_arg0(relations)
        lower_case_role_of_interest = get_lower(role_of_interest)
        add_arg0s = list()
        for arg0 in arg0s:
            for role in lower_case_role_of_interest:
                if role in arg0.lower():
                    add_arg0s.append(arg0)
                    break

        print(UseStyle("Added role of interest from inclusive match on arg0: ", fore='yellow'))
        print(add_arg0s)
        role_of_interest.extend(add_arg0s)


    print(UseStyle('Loaded ' + str(len(relations)) +' relations from file', fore='green'))
    tree_graph = tree(relations, input_data_entries)
    print(UseStyle('Finish', fore='green'))
    return tree_graph


if __name__ == '__main__':
    configuration = list()
    tree_graph = main(configuration)
    tree_graph.view()
