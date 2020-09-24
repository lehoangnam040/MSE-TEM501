import _pickle as cPickle
import logging
import os
import json
import keras
from keras.models import load_model
from sklearn.feature_extraction.text import TfidfVectorizer
import json
#import preprocess as my_preproc
import numpy as np
from flask import Flask, request, jsonify
import re
from CocCocTokenizer import PyTokenizer
from elasticsearch import Elasticsearch
import warnings
def warn(*args, **kwargs):
        pass
warnings.warn = warn
import sys

class KeywordExtractor():

    def __init__(self):
        with open('tfidf_vectorizer_8mi.pk', 'rb') as fin:
            self.tfidf_vectorizer = cPickle.load(fin)
            self.feature_names = self.tfidf_vectorizer.get_feature_names()
        print("Model loaded")

    def sort_coo(self, coo_matrix):
        tuples = zip(coo_matrix.col, coo_matrix.data)
        return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


    def extract_topn_from_vector(self, sorted_items, topn=10):
        """get the feature names and tf-idf score of top n items"""

        # use only topn items from vector
        sorted_items = sorted_items[:topn]

        score_vals = []
        feature_vals = []

        # word index and corresponding tf-idf score
        for idx, score in sorted_items:
            # keep track of feature name and its corresponding score
            score_vals.append(round(score, 3))
            feature_vals.append(self.feature_names[idx])

        return feature_vals, score_vals

    def get_keyword(self, _input):
        clean_text_tf_idf = self.tfidf_vectorizer.transform([_input])

        # sort the tf-idf vectors by descending order of scores
        sorted_items = self.sort_coo(clean_text_tf_idf.tocoo())

        # extract only the top n; n here is 10
        keywords, scores = self.extract_topn_from_vector(sorted_items)
        return keywords, scores


class MyPreprocess():

    def __init__(self):
        self.T = PyTokenizer(load_nontone_data=True)

    def add_space_between_word_and_special_char(self, word):
        """
        thêm dấu cách giữa các từ và các kí tự ko phải từ
        """
        res = ''
        for x in word:
            if not str.isalpha(x) and x != ' ' :
                if res and res[-1] != ' ':
                    res+= ' '
                res += x
                res += ' '
            else:
                res += x
        return res
    
    
    def remove_special_character_number(self, string):
        """
        Loại bỏ những kí tự  số và kí tự đặc biệt trong 1 string
        """
        return re.sub('[^a-zA-Z\săâáắấàằầảẳẩãẵẫạặậđeêéếèềẻểẽễẹệiíìỉĩịoôơóốớòồờỏổởõỗỡọộợuưúứùừủửũữụựyýỳỷỹỵaăâáắấàằầảẳẩãẵẫạặậđeêéếèềẻểẽễẹệiíìỉĩịoôơóốớòồờỏổởõỗỡọộợuưúứùừủửũữụựyýỳỷỹỵaăâáắấàằầảẳẩãẵẫạặậđeêéếèềẻểẽễẹệiíìỉĩịoôơóốớòồờỏổởõỗỡọộợuưúứùừủửũữụựyýỳỷỹỵaăâáắấàằầảẳẩãẵẫạặậđeêéếèềẻểẽễẹệiíìỉĩịoôơóốớòồờỏổởõỗỡọộợuưúứùừủửũữụựyýỳỷỹỵaăâáắấàằầảẳẩãẵẫạặậđeêéếèềẻểẽễẹệiíìỉĩịoôơóốớòồờỏổởõỗỡọộợuưúứùừủửũữụựyýỳỷỹỵaăâáắấàằầảẳẩãẵẫạặậđeêéếèềẻểẽễẹệiíìỉĩịoôơóốớòồờỏổởõỗỡọộợuưúứùừủửũữụựyýỳỷỹỵ]','', string )
    
    def add_space_in_sentence(self, sentence):
        dst = []
        for word in sentence.split():
            dst.append(self.add_space_between_word_and_special_char(word))
        return ' '.join(dst)
    
    
    def tokenizer(self, string):
        words = self.T.word_tokenize(string, tokenize_option=0)
        return ' '.join(words)
    
    def remove_stop_words(self, string, stop_multiple_words, stop_words):
        """
        remove những từ không quan tâm trong 1 string
        """
        for stop_word in stop_multiple_words:
            string = re.sub(stop_word, '', string)
    
        res = []
        words = string.split()
        for word in words:
            if word not in stop_words:
                res.append(word)
        return ' '.join(res)
    
    
    def preprocess_string(self, string, stop_multiple_words, stop_words):
        
        # B1: lowercase
        string = string.lower()
        # B2: thêm dấu cách, tách các chữ ra khỏi những phần dính vs số và kí tự đặc biệt
    
        string = self.add_space_in_sentence(string)
    
        # B3: loại bỏ số, kí tự đặc biệt
        string = self.remove_special_character_number(string)
    
        # B4: tokenizer word
        string = self.tokenizer(string)
    
        # B5: remove stop words
        string = self.remove_stop_words(string, stop_multiple_words, stop_words)
    
        return string

app = Flask(__name__)

vocab_text = []

with open('text_vectorize.json', 'r', encoding='utf8') as fp:
    vocab_text = json.load(fp)

word_vectorizer = TfidfVectorizer(max_features=20000)
word_vectorizer.fit(vocab_text)
model = load_model('model.h5')
keyword_extractor = KeywordExtractor()
my_preproc = MyPreprocess()
es = Elasticsearch('172.17.0.1')
stop_multiple_words = ['bác sỹ', 'xin chào', 'xin phép', 'cho em hỏi', 'cho tôi hỏi', 'xin cám_ơn', 'xin cảm_ơn', 'giải đáp']

stop_words = [
        'có', 'em', 'bị', 'và', 'bác_sĩ', 'tôi', 'thì', 'bệnh_viện', 'medlatec',  'cám_ơn', 'cảm_ơn',
        'nguyên_nhân', 'hỏi', 'không', 'cho', 'như', 'đã', 'ở', 'ko', 'nào', 'nên', 'rất', 'giúp', 'l',
        'tại', 'này', 'lúc', 'đây', 'vẫn', 'k', 'nếu', 'vì', 'do', 'còn', 'đc', 'viện', 'sẽ', 'mỗi',
        'e', 'ạ', 'vâng', 'bs', 'bv', 'nhưng', 'chào', 'là', 'bac_si', 'hoặc', 'ít', 'nhiều', 'hơn',
        'bsy', 'bsi', 'thưa', 'của', 'vậy', 'ra', 'của', 'ơi', 'nhờ', 'về', 'câu_hỏi', 'giải_đáp'
        ]
labels = {
    0: 'lâm sàng cận lâm sàng',
    1: 'liên khoa mắt tai mũi họng răng hàm mặt da liễu',
    2: 'ngoại',
    3: 'nhi',
    4: 'nội',
    5: 'sản',
    6: 'truyền nhiễm'
}

def cosine_similarity_of_2_string(str1, str2):
    x_set = {w for w in str1.split()}
    y_set = {w for w in str2.split()} 
    l1 = []
    l2 = []
    rvector = x_set.copy().union(y_set)
    for w in rvector: 
        if w in x_set:
            l1.append(1)
        else: l1.append(0) 
    
        if w in y_set:
            l2.append(1) 
        else: l2.append(0) 
    c = 0
                          
    # cosine formula  
    for i in range(len(rvector)): 
        c += l1[i] * l2[i] 
    cosine = c / float((sum(l1) * sum(l2)) ** 0.5) 
    #print("similarity: ", cosine) 
    return cosine
   

@app.route("/", methods=['POST'])
def hello():
    question = request.json.get('question')
    if question:
        preprocess_str = my_preproc.preprocess_string(question, stop_multiple_words, stop_words)
        _input = word_vectorizer.transform([preprocess_str])
        _input = _input.toarray()

        output = model.predict(_input)
        res = {}
        l = list(output[0])
        for i, acc in enumerate(l):
            res[labels[i]] = str(round(acc * 100, 1)) + '%'

        keywords, _ = keyword_extractor.get_keyword(preprocess_str)
        relation_q = es.search(
            body={"query": {"terms": {"question":  keywords}}}, _source=True, index='questions', 
            filter_path=['hits.hits._source.title','hits.hits._source.question']
        )
        relation_question_list = relation_q.get('hits', {}).get('hits', [])
        

        task2_res = []
        for relation_question in relation_question_list:
            title = relation_question.get('_source', {}).get('title', '')
            q = relation_question.get('_source', {}).get('question', '')
            preprocess_relation_question = my_preproc.preprocess_string(title + ' ' + q, stop_multiple_words, stop_words)
            simlarity_score = cosine_similarity_of_2_string(preprocess_str, preprocess_relation_question)
            task2_res.append({
                'title': title,
                'question': q,
                'score': simlarity_score
            })
        
        #sys.stdout.flush()
        return jsonify({
            'task1': res,
            'task2': sorted(task2_res, key=lambda k: k['score'], reverse=True) 
        })
    else:
        return "Need question!!!"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
