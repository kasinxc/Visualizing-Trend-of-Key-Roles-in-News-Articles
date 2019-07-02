# common
coref_result_file_path = "../../Result/COREF/Allennlp_Coref/" # used by allen_coref_on_trump_data and coref_visualization

# utils.py 
use_steplines_format = True
input_data_file_path = '../../Data/trump_prob'
title_num = 10

# allen_coref_on_trump_data.py
data_low_index = 0
data_high_index = 535539
# causing error during the running process, article ids in 6_month data
# end_error_indice = [505215]
end_error_indice = [211, 330, 13571, 9451, 11994, 13412] # for example, "donald trump", "melania trump" without any punctuations, 9451, 11994 are link


# coref_visualization.py
max_file_number = 1000
min_weight_to_draw = 1
center_word_selection = "WordNet" # LongestSpan, NameEntity, WordNet
flags_num_of_center_word_as_factor = True
flags_read_from_correct_files = True
flags_remove_isolate_nodes = True
# correct_file_names = []
# for trump_data
correct_file_names = [30, 31, 47, 56, 57, 84, 92, 111, 121, 130, 138, 144, 151, 256, 260, 291, 294, 295, 361, 364, 371, 381, 389, 393, 402, 405, 414, 420, 421, 468, 505, 511, 536, 551, 564, 569, 588, 590, 596, 603, 604, 662, 674, 678, 695, 712, 719, 752, 758, 764, 790, 812, 819, 826, 830, 839, 869, 904, 921, 943, 953, 959, 967, 976, 980, 987, 996, 1000, 1007]


# algorithm_patches.py
ne_file_path = '../../Data/NER.npy'

