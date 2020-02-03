import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import genesis
genesis_ic = wn.ic(genesis, False, 0.0)
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem import SnowballStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
#from sklearn.metrics import roc_auc_score

class KNN_NLC_Classifer():
    def __init__(self,global_list, k=1, distance_type = 'path'):
        self.k = k
        self.distance_type = distance_type
        self.global_list = global_list
        self.matrix_generator(self.global_list)

    # This function is used for training
    def fit(self, x_train, y_train):
        self.x_train = x_train
        self.y_train = y_train

    def camel_case_split(self, str): 
        words = [[str[0]]] 
  
        for c in str[1:]: 
            if words[-1][-1].islower() and c.isupper(): 
                words.append(list(c)) 
            else: 
                words[-1].append(c) 
  
        return [''.join(word) for word in words] 

    # This function runs the K(1) nearest neighbour algorithm and
    # returns the label with closest match. 
    def predict(self, x_test):
        self.x_test = x_test
        y_predict = []

        for i in range(len(x_test)):
            max_sim = 0
            max_index = 0
            for j in range(self.x_train.shape[0]):
                temp = self.document_similarity(x_test[i], self.x_train[j])
                if temp > max_sim:
                    max_sim = temp
                    max_index = j
            y_predict.append(self.y_train[max_index])
        return y_predict

    def convert_tag(self, tag):
        """Convert the tag given by nltk.pos_tag to the tag used by wordnet.synsets"""
        tag_dict = {'N': 'n', 'J': 'a', 'R': 'r', 'V': 'v'}
        try:
            return tag_dict[tag[0]]
        except KeyError:
            return None


    def doc_to_synsets(self, doc):
        """
            Returns a list of synsets in document.
            Tokenizes and tags the words in the document doc.
            Then finds the first synset for each word/tag combination.
        If a synset is not found for that combination it is skipped.

        Args:
            doc: string to be converted

        Returns:
            list of synsets
        """
        #tokens = word_tokenize(doc+' ')
        tokens = doc
        l = []
        tags = nltk.pos_tag([tokens[0] + ' ']) if len(tokens) == 1 else nltk.pos_tag(tokens)
        
        for token, tag in zip(tokens, tags):
            syntag = self.convert_tag(tag[1])
            syns = wn.synsets(token, syntag)
            if (len(syns) > 0):
                l.append(syns[0])
        #print(l)
        return l  

    def similarity_score(self, s1, s2, distance_type = 'path'):
          """
          Calculate the normalized similarity score of s1 onto s2
          For each synset in s1, finds the synset in s2 with the largest similarity value.
          Sum of all of the largest similarity values and normalize this value by dividing it by the
          number of largest similarity values found.

          Args:
              s1, s2: list of synsets from doc_to_synsets

          Returns:
              normalized similarity score of s1 onto s2
          """
          s1_largest_scores = []

          for i, s1_synset in enumerate(s1, 0):
              max_score = 0
              for s2_synset in s2:
                  if distance_type == 'path':
                      score = s1_synset.path_similarity(s2_synset, simulate_root = False)
                  else:
                      score = s1_synset.wup_similarity(s2_synset)                  
                  if score != None:
                      if score > max_score:
                          max_score = score
              
              if max_score != 0:
                  s1_largest_scores.append(max_score)
          
          mean_score = np.mean(s1_largest_scores)
                 
          return mean_score 


    def document_similarity(self,doc1, doc2):
          """Finds the symmetrical similarity between doc1 and doc2"""

          synsets1 = self.doc_to_synsets(doc1)
          synsets2 = self.doc_to_synsets(doc2)
          
          return (self.similarity_score(synsets1, synsets2) + self.similarity_score(synsets2, synsets1)) / 2

    def method_outlier(self, matrix) :
          class_score = []
          total_score = 0
          for i in range(0, len(matrix)) :
              method_score = 0
              for j in range(0, len(matrix[i]) ):
                  method_score = method_score + matrix[i][j]
              #method_score = method_score / len(self.global_list[i])
              class_score = class_score + [method_score]
              total_score = total_score + method_score
          
          outliers = []
          for x in range(0, len(class_score)) :
              if (class_score[x]/total_score > 0.35) :
                  outliers = outliers + [self.global_list[x][1]]
              print(class_score[x]/total_score)
          print(outliers)
          
          return outliers

    def matrix_generator(self, global_list) :
          matrix = []
          final_list = []
          
          for i in range(0, len(global_list)) :
              row = []
              inner_list = [] 
              for j in range(2, len(global_list[i])) :
                  if(self.camel_case_split(global_list[i][j]) != None) :
                      inner_list = inner_list + self.camel_case_split(global_list[i][j])
              final_list = final_list + [[global_list[i][0]] + [global_list[i][1]] + inner_list]
              for j in range(0, len(global_list)) :
                  row = row + [0]
              matrix = matrix + [row]

          #print(len(matrix)) 
          #print(final_list)
          #print(global_list)
          for i in range(0, len(final_list)) :
              for j in range(0, len(final_list)) :
                  score = self.document_similarity(final_list[i], final_list[j])  
                  matrix[i][j] = score
                  
          #print(matrix)
          methods = self.method_outlier(matrix)		  
          return methods
         

