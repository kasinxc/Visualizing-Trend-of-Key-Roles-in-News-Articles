import os
import json

import networkx as nx
import matplotlib.pyplot as plt

from coref_config import *
import allen_coref_on_input_data as allen_coref_on_data
import algorithm_patches as ap


def get_content(document, span):
    content = str()
    start = span[0]
    end = span[1]
    for i in range(start, end):
        content += document[i] + ' '
    content += document[end]
    return content


def read_clusters_from_all_files(coref_result_file_path):
    all_clusters = list()
    open_file_cnt = 0

    for file_name in os.listdir(coref_result_file_path):
        if not '.json' in file_name:
            continue
        else:
            open_file_cnt += 1
            if open_file_cnt > max_file_number:
                open_file_cnt-=1
                break

            with open(coref_result_file_path+str(file_name), 'r') as f:
                coref_result = json.load(f)
                document = coref_result["document"]
                index_clusters = coref_result["clusters"]
                for index_cluster in index_clusters:
                    cluster = list()
                    for span in index_cluster:
                        cluster.append(get_content(document, span))
                    all_clusters.append(cluster)
                f.close()

    print("total opened files: " + str(open_file_cnt))
    return all_clusters


def read_clusters_from_correct_files(coref_result_file_path):
    all_clusters = list()
    open_file_cnt = 0

    print("correct_file_counts = " + str(len(correct_file_names)))
    for file_name in correct_file_names:
        open_file_cnt += 1
        if open_file_cnt > max_file_number:
            open_file_cnt-=1
            break

        with open(coref_result_file_path+str(file_name)+".json", 'r') as f:
            coref_result = json.load(f)
            document = coref_result["document"]
            index_clusters = coref_result["clusters"]
            for index_cluster in index_clusters:
                cluster = list()
                for span in index_cluster:
                    cluster.append(get_content(document, span))
                all_clusters.append(cluster)

    print("total opened files: " + str(open_file_cnt))
    return all_clusters


def build_color_map_for_nodes(G, nodes, center_words, specific_words):
    color_map = []

    center_words = set(center_words)
    for node in nodes:
        if node in center_words:
            color_map.append('red')

        elif node in specific_words:
            color_map.append('pink')

        else:
            color_map.append('black')
    return color_map


def build_labels_for_edges(G, edges):
    labels = nx.get_edge_attributes(G, 'weight')
    return labels


def find_word_position(nodes, word):
    for i in range(len(nodes)):
        if nodes[i] == word:
            return i
    return -1


def find_center_word_position(center_words, word):
    for i in range(len(center_words)):
        if center_words[i] == word:
            return i
    return -1


def remove_isolated_nodes(nodes, center_words, edges):
    # Building new nodes from nodes by removing isolated nodes
    connected_nodes = set()

    for i in range(len(edges)):
        for j in range(len(edges[i])):
            if edges[i][j] >= min_weight_to_draw:
                connected_nodes.add(center_words[i])
                connected_nodes.add(nodes[j])

    new_nodes = list(connected_nodes)
    # Building new edges from new_nodes and original center_words
    all_count = len(new_nodes)
    center_count = len(center_words)

    new_edges = [[0] * all_count for _ in range(center_count)]

    for i in range(center_count): # index of center_words, remain unchanged 
        for j in range(all_count): # index of new_nodes
            span = new_nodes[j]
            span_pos = find_word_position(nodes, span)
            new_edges[i][j] = edges[i][span_pos] 

    return new_nodes, new_edges


def build_nodes_and_edges(clusters):
    nodes = list()
    center_words = set() # remove duplicates (center words of each cluster) and then become list type to be the index of edges
    specific_words = set() # only checks existance

    center_words_for_cluster = list() # for computing edges
    center_words_for_cluster_count = list() # how many same center_words in cluster i

    # get nodes
    for cluster in clusters:
        for span in cluster:
            nodes.append(span)

    nodes = list(nodes)

    # get center_word and how many of each center_word
    for cluster in clusters:
        center_word, num_of_center_word, specific_words_for_cluster = ap.get_center_words_for_cluster(cluster, center_word_selection)

        for word in specific_words_for_cluster:
            specific_words.add(word)

        center_words.add(center_word)
        center_words_for_cluster.append(center_word)
        center_words_for_cluster_count.append(num_of_center_word)

    center_words = list(center_words)

    # get edges
    all_count = len(nodes)
    center_count = len(center_words)

    edges = [[0] * all_count for _ in range(center_count)]
    for i in range(len(clusters)):
        cluster = clusters[i]
        center_word = center_words_for_cluster[i]
        num_of_center_word = center_words_for_cluster_count[i] # factor of labels between center_word and other words

        center_word_pos = find_center_word_position(center_words, center_word)

        for span in cluster:
            if span == center_word:
                continue
            else:
                span_pos = find_word_position(nodes, span)
                if flags_num_of_center_word_as_factor == False:
                    num_of_center_word = 1
                edges[center_word_pos][span_pos] += 1*num_of_center_word

    if flags_remove_isolate_nodes == True:
        new_nodes, edges = remove_isolated_nodes(nodes, center_words, edges)
    else:
        new_nodes = nodes

    return new_nodes, center_words, specific_words, edges


def add_edges_to_graph(G, nodes, center_words, edges):
    for i in range(len(edges)):
        center_word = center_words[i]
        for j in range(len(edges[i])):
            span = nodes[j]
            if edges[i][j] >= min_weight_to_draw:
                G.add_weighted_edges_from([(center_word, span, edges[i][j])])


def visualize_graph(clusters):
    G = nx.Graph()

    nodes, center_words, specific_words, edges = build_nodes_and_edges(clusters)
    
    G.add_nodes_from(nodes)

    color_map = build_color_map_for_nodes(G, G.nodes, center_words, specific_words)
    add_edges_to_graph(G, nodes, center_words, edges)

    labels = build_labels_for_edges(G, edges)

    pos = nx.spring_layout(G)

    nx.draw(G, pos = pos, with_labels = True, node_color = color_map, node_shape='o', alpha = .7)

    nx.draw_networkx_edge_labels(G, pos = pos, edge_labels = labels)
    plt.savefig("coref_demo.png")
    plt.show()


def load_configurations(configurations):
    global flags_read_from_correct_files, flags_remove_isolate_nodes, max_file_number, min_weight_to_draw, center_word_selection
    
    for config in configurations:
        name = config[0]
        content = config[1]

        if name == 'read_from_correct_files':
            flags_read_from_correct_files = content
        if name == 'remove_isolate_nodes':
            flags_remove_isolate_nodes = content
        if name == 'max_file_number':
            max_file_number = content
        if name == 'min_weight_to_draw':
            min_weight_to_draw = content
        if name == 'center_word_selection':
            center_word_selection = content


def get_clusters(flags_read_from_correct_files):
    global coref_result_file_path
    if not os.path.exists(coref_result_file_path):
        os.makedirs(coref_result_file_path)
        if use_steplines_format == False:
            input_data_points = allen_coref_on_data.readFileFromTrump(input_data_file_path)
        else:
            input_data_points = allen_coref_on_data.readFileFromSteplines(input_data_file_path)

        allen_coref_on_data.applyAllenToDP(input_data_points)

    if flags_read_from_correct_files:
        clusters = read_clusters_from_correct_files(coref_result_file_path)
    else:
        clusters = read_clusters_from_all_files(coref_result_file_path)

    clusters = ap.merge(clusters)

    return clusters


def main(configurations):
    load_configurations(configurations)
    clusters = get_clusters(flags_read_from_correct_files)
    visualize_graph(clusters)


if __name__ == '__main__':
    configurations = list()
    main(configurations)
