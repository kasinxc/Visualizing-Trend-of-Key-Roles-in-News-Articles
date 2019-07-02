# common

max_file_number = 535539 # used by srl_visualization and relation_extraction

# word2vec  
word2vec_model_file_path = 'models/trump_model'

# srl_visualization
min_verb_count_to_draw = 5
max_verb_count_to_draw = 6
min_verb_other_roles_count_to_draw = 1
max_verb_other_roles_count_to_draw = 500
max_length_of_role = 50
top_ranking_verbs = 18
enable_coreference_resolution = True
coref_read_from_correct_file = True
enable_inclusive_match_on_roles = False
enable_word_embedding = False
word2vec_similarity_threshold = .75
enable_tfidf = True
tfidf_threshold = .04
role_of_interest = ['Donald Trump']
# role_of_interest = ['chapo', 'amlo', 'los', 'texcoco', 'zambada', 'del chapo', 'trump', 'el chapo', 'mexicano']
# role_of_interest = ['michelle salas', 'luis miguel', 'del', 'frida', 'silvia pinal', 'boeing', 'trump', 'los', 'yalitza aparicio']
# role_of_interest = ['pope', 'priest', 'abuse', 'pope francis', 'catholic', 'bishop', 'bible', 'catholic church', 'cardinal']
# role_of_interest = ['police', 'robbery', 'murder', 'officer', 'woman', 'houston', 'texas', 'jazmine barnes', 'christmas']
# role_of_interest = ['soup', 'chocolate', 'cheese', 'chicken', 'cake', 'cookies', 'butter', 'potato', 'christmas']
# role_of_interest = ['obama', 'facebook', 'national federation', 'LeBron James', 'mayor joseph', 'Donald Trump']

# relation_extraction
enable_lemmatizer = True
use_steplines_format = False #Trump - False
# input_data_file_path = '../../Data/TopicClusters/4-1244-all/prod20181207_scheduled20181207t013500/0'
input_data_file_path = '../../Data/trump_prob'
# input_data_file_path = '../../Result/Taxonomy/basketball/prod20190205_scheduled20190205t013500/'
# input_data_file_path = '../../Data/6_month/prod20181107_scheduled20181107t013500/'
# srl_result_folder_path = '../../Result/SRL/6_month_data/Allennlp_Srl-4-1244-all/prod20181207_scheduled20181207t013500/'
srl_result_folder_path = '../../Result/SRL/Trump_data/Allennlp_Srl'
# srl_result_folder_path = '../../Result/SRL/6_month_data/Allennlp_Srl-articleIds-0-31-12'
# Data with lines number larger than 4000 is more likely to fail the SRL processing
line_length_threshold = 4000 
flag_predict_srl_on_file = False



