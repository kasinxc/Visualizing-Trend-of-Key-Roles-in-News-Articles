## How to run Semantic Role Labeling

```bash
1. cd $FolderPath/Visualizing-Trend-of-Key-Roles-in-News-Articles/SemanticRoleLabeling/Source/SRL/

2. jupyter notebook
```



3. click **srl_demo.ipynb** and run



4. Configure the search bar and run interact



### **<u>Configuration</u>**

**label range**

Integer: [0. 200]

Only visualize edges with weight falling in the given range.



**top_verbs**

Integer

Show top frequent verbs for each subject. This is aiming for the situation where there are too many verbs for a given subject and user cares about the most frequent verbs.

If top_verbs <= 0, we will show top_verbs=1.



**Max_file_number**

Integer

Maximum number of semantic role labeling file to read. 

For Trump dataset, SRL count: 20769.



**Max_length_of_role**

Integer

Maximum length of a semantic role to show. This is to erase a sentense role from the graph.



**Enable_coreference_resolution**

Boolean (default: True) 



**Core_read_from_correct_file**

Boolean (default: True)

This is the same flag as the coreference resolution visualization. 

Setting this flag to True will benefit the accuracy of semantic role labeling.



**Enable_inclusive_match**

Boolean (default: False)

When searching for a role of interest, enabling inclusive match will show those roles that "string include" this given role of interest.  

This is set to False by default because there are too many semantic roles that has Donald Trump in it. This may be useful for a rare semantic role.



**Enable_lemmatizer**

Boolean (default: True)

When set to True, lemmatize the verbs and merge the result. This is to simplify the graph when the tense of verb does not matter that much.



**enable_word_embedding**

Boolean (default: False)

Try to merge verbs with similiar word embedding. Define <u>similiar</u> as the cosine similarity. 

​	When true:

​		set word_similarity threshold to filter out verbs with different meanings.

* This is an optional experiment for user to interact with. The potential risk is that, a pair of contradictory verbs may have high cosine similarity. 



**enable_tfidf**

Boolean (default: False)

Merge the object by TF-IDF score. 

When true:

Set tfidf diff threshold to merge the object by the difference of TF-DIF score.

* This is an optional experiment for user to interact with. The potential risk is that, the tfidf diff threshold may vary with a different news topic.

  


Note:

> - the default dataset is Trump data.



## How to run Coreference Resolution

```
1. cd $FolderPath/Visualizing-Trend-of-Key-Roles-in-News-Articles/SemanticRoleLabeling/Source/COREF/

2. jupyter notebook
```



3. click **coref_demo.ipynb** and run



4. Configure the search bar and run interact



### **<u>Configuration</u>**

**read_from_correct_files**

- True (default): read from correct files. These files are verfied manually to ensure that every coreference resolution cluster in each file is correct. 
- False: read from all files. This would also visualize coreference resolution cluster that has errors.



**remove_isolate_nodes**

- True (default): remove all isolate nodes that does not have any edges. For cleanness purpose.
- False: visualize nodes including isolate nodes.  



**file_count**

Integer: [0, 1024]

If file_count is larger than the number of available files, the total loaded files will be equal to all available files. 



**draw_weight**

Integer: [0, 20]

Only visualize edges with weight >= draw_weight



**center_word**

* LongestSpan: select the longest string as the cernter word of a coreference resolution cluster.
* NameEntity: select the words in name entity list generated by LDA as the center words of a coreference resolution cluster. If tied, use LongestSpan.
* WordNet: select the name not in wordnet as the center words of a coreference resolution cluster. If tied, use LongestSpan.



Note: 

> - the default dataset is Trump data.
> - The maximum number of correct files is 69. 



