# Visualizing-Trend-of-Key-Roles-in-News-Articles

#### **Demo**: https://youtu.be/Xf_2eaSjq5w



## Dataset

The 2 news datasets we are using is from Taboola company. One is a topic specific Trump dataset containing more than two months of news from late April to early July 2018. The news in this dataset share the same character, which is they all involve President Trump. The other dataset is general 6 months news data from November 2018 to April 2019. The topic of 6 months dataset ranges from sports to politics, food recipes to crime. Detailed format of the two datasets is as follows. 

#### Trump dataset

The Trump dataset has overall 20,833 news entries. Each news entry contains title description with punctuations, a unique article id, and probability on ten topic clusters clustered by latent dirichlet allocation (LDA), which is a three-level hierarchical Bayesian model where each item of a collection is modeled as a finite mixture over an underlying set of topics [LDA](http://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf).

|     attribute     |           description            |
| :---------------: | :------------------------------: |
| title description | title description for each news  |
|    article ids    | unique article ids for each news |
|    probability    |  probability on topic clusters   |

​							Table1: Data Format of Trump Dataset



#### 6 Month Dataset

The 6 month dataset contains over half a million news title descriptions from the Taboola company. The 6 month dataset has two different formats, StepContent and StepIndexingData. They are both in json format but differ in attributes. 

##### StepContent Format

The StepContent format for the 6 months dataset includes taxonomy, first level taxonomy, unique article ids, title description, and so on. StepCotent uniquely contains title descriptions for later natural language processing. This special attribute is bolded in the table below. 

|       attribute       |               description               |
| :-------------------: | :-------------------------------------: |
|      articleIds       |    unique article ids for each news     |
|  firstLevelTaxonomy   |          first level category           |
|       taxonomy        |      multiple detailed categories       |
|         title         |               news title                |
| **title description** | **title description with punctuations** |
|          ...          |                   ...                   |

​						Table2: StepContent Format of 6 Month Dataset



**StepIndexingData** **Format**

 StepIndexingData also shares attributes that the StepContent format has, like taxonomy, unique article id, title and so on. This format has uniquely hierarchical topic cluster information including cluster id, label, labelScore, taxonomy as well as topTerms for level 0 to level 4 where level 0 indicates the most general topic clusters and level 4 indicates the most specific level. This information is bolded in the following table.

|     attribute      |                         description                          |
| :----------------: | :----------------------------------------------------------: |
|     articleIds     |               unique article ids for each news               |
| firstLevelTaxonomy |                     first level category                     |
|      taxonomy      |                 multiple detailed categories                 |
|       title        |                          news title                          |
|      traffic       |                traffic for this news article                 |
| **topic cluster**  | **contains id, label, labelScore, taxonomy, topTerms, topTermsScore** |
|        ...         |                             ...                              |

​				Table3: StepIndexingData Format of 6 Months Dataset





