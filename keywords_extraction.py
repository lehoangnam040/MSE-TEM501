import gensim
#import sklearn
import _pickle as cPickle
#import logging
import os
#import re
import json
import preprocess as mypreproc
#from CocCocTokenizer import PyTokenizer

#T = PyTokenizer(load_nontone_data=True)

class KeywordExtractor():

    def __init__(self):
        self.phraser_models = [
            gensim.models.phrases.Phraser.load('model-bin/bigram_big.pkl'),
            gensim.models.phrases.Phraser.load('model-bin/trigram_big.pkl'),
        ]

        # load a set of stop words
        self.stopwords = open("resources/vietstopwords.txt", 'r', encoding='utf-8').read().split("\n")

        with open('model-bin/tfidf_vectorizer_8mi.pk', 'rb') as fin:
            self.tfidf_vectorizer = cPickle.load(fin)
            # inv_map = {v: k for k, v in tfidf_vectorizer.vocabulary_.items()}
            self.feature_names = self.tfidf_vectorizer.get_feature_names()
        print("Model loaded")

    def sort_coo(self, coo_matrix):
        tuples = zip(coo_matrix.col, coo_matrix.data)
        return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

    def transform_ngram(self, text, phraser_list):
        line_words = text.split()

        for phraser in phraser_list:
            line_words = phraser[line_words]
            line_transform = " ".join(line_words)
        return line_transform

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

        #results = {}
        #for idx in range(len(feature_vals)):
        #    results[feature_vals[idx]] = score_vals[idx]

        return feature_vals, score_vals

    def get_keyword(self, _input):
        #clean_text = clean_raw_text(raw_input)
        clean_text = self.transform_ngram(_input, self.phraser_models)
        clean_text_tf_idf = self.tfidf_vectorizer.transform([clean_text])

        # sort the tf-idf vectors by descending order of scores
        sorted_items = self.sort_coo(clean_text_tf_idf.tocoo())

        # extract only the top n; n here is 10
        keywords, scores = self.extract_topn_from_vector(sorted_items)
        return keywords, scores


if __name__ == "__main__":
    labels = {
        'lâm sàng cận lâm sàng': 0, 
        'liên khoa mắt tai mũi họng răng hàm mặt da liễu': 1, 
        'ngoại': 2,
        'nhi': 3, 
        'nội': 4,
        'sản': 5,
        'truyền nhiễm': 6
    }
    stop_multiple_words = ['bác sỹ', 'xin chào', 'xin phép', 'cho em hỏi', 'cho tôi hỏi', 'xin cám_ơn', 'xin cảm_ơn', 'giải đáp']

    stop_words = [
        'có', 'em', 'bị', 'và', 'bác_sĩ', 'tôi', 'thì', 'bệnh_viện', 'medlatec',  'cám_ơn', 'cảm_ơn', 
        'nguyên_nhân', 'hỏi', 'không', 'cho', 'như', 'đã', 'ở', 'ko', 'nào', 'nên', 'rất', 'giúp', 'l',
        'tại', 'này', 'lúc', 'đây', 'vẫn', 'k', 'nếu', 'vì', 'do', 'còn', 'đc', 'viện', 'sẽ', 'mỗi',  
        'e', 'ạ', 'vâng', 'bs', 'bv', 'nhưng', 'chào', 'là', 'bac_si', 'hoặc', 'ít', 'nhiều', 'hơn', 
        'bsy', 'bsi', 'thưa', 'của', 'vậy', 'ra', 'của', 'ơi', 'nhờ', 'về', 'câu_hỏi', 'giải_đáp'
    ]
    
    src_dir = './category'
    dst_dir = './category_preprocess_with_keywords'
    filenames = []
    for (dirpath, dirnames, filenames1) in os.walk(src_dir):
        for fp in filenames1:
            filenames.append(f'{src_dir}/{fp}')
        break

    extractor = KeywordExtractor()
    
    for filename in filenames:
        res = []    
        label = filename.split('/')[-1].split('.')[0]
        label_num = labels[label] 
        
        with open(f'{filename}', 'r') as fp:
            count = 0 

            for line in fp:
                count += 1
                try:
                    title, q = line.split('\t')
                except Exception as e:
                    print(e)
                    print(line.split('\t'))
                    print(filename, title, q)
                            
                dst_title = mypreproc.preprocess_string(title, stop_multiple_words, stop_words) 
                dst_q = mypreproc.preprocess_string(q, stop_multiple_words, stop_words)
                keywords, scores = extractor.get_keyword(dst_title + ' ' + dst_q)
		 
                res.append({
                    '_id': str(label_num) + '-' + str(count),
                    'title': title,
                    'question': q,
                    'keywords': keywords,
                    'scores': scores
                })
                if (count % 10 == 0):
                    print(label + str(count))

        with open(f'{dst_dir}/{label}.json', 'w', encoding='utf8') as fp1:
                json_object = json.dumps(res, indent = 4, ensure_ascii=False)
                fp1.write(json_object)
        print('Done ' + label)
