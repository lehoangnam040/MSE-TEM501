import keras
from keras.models import load_model
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import preprocess as my_preproc
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

vocab_text = []

with open('text_vectorize.json', 'r', encoding='utf8') as fp:
    vocab_text = json.load(fp)

print(len(vocab_text))
word_vectorizer = TfidfVectorizer(max_features=20000)
word_vectorizer.fit(vocab_text)
model = load_model('model.h5')
model.summary()
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

        return jsonify(res)
    else:       
        return "Need question!!!"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
