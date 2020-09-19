import numpy as np
from keras.utils import to_categorical
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import json
import random
from keras.models import Sequential
from keras import layers
from keras.layers import Dense, Dropout, Activation, Flatten
import matplotlib.pyplot as plt


def build_model(feature_num, label_num):
    model = Sequential()
    # Input - Layer
    model.add(layers.Dense(2048, activation = "relu", input_shape=(feature_num, )))
    # Hidden - Layers
    model.add(layers.Dropout(0.9, noise_shape=None, seed=None))
    model.add(layers.Dense(512, activation = "relu"))
    model.add(layers.Dropout(0.8, noise_shape=None, seed=None))
    #model.add(layers.Dense(32, activation = "relu"))
    #model.add(layers.Dropout(0.5, noise_shape=None, seed=None))
    model.add(layers.Dense(32, activation = "relu"))
    model.add(layers.Dropout(0.5, noise_shape=None, seed=None))
    model.add(layers.Dense(16, activation = "relu"))
    # Output- Layer
    model.add(Dense(label_num, activation='softmax'))
    model.compile(optimizer = "adam", loss = "categorical_crossentropy",metrics = ["accuracy"])
    return model

labels = {
    'lâm sàng cận lâm sàng': 0, 
    'liên khoa mắt tai mũi họng răng hàm mặt da liễu': 1, 
    'ngoại': 2,
    'nhi': 3, 
    'nội': 4,
    'sản': 5,
    'truyền nhiễm': 6
}

# load hết X ra
dir_name = 'category_preprocess'


filenames = []
for (dirpath, dirnames, filenames1) in os.walk(dir_name):
    for fp in filenames1:
        filenames.append(f'{dir_name}/{fp}')


#for fpath in filenames:
#    with open(fpath, 'r') as fp:
#        data = json.load(fp)
#
#        print(fpath, len(data))

#truyền nhiễm.json 2118 6
#ngoại.json 1839 2
#lâm sàng cận lâm sàng.json 1976 0
#nhi.json 1676 3
#sản.json 7769 5
#nội.json 3277 4
#liên khoa mắt tai mũi họng răng hàm mặt da liễu.json 2121 1

# Lấy min để làm chuẩn => X train = 1676
# còn lại sẽ làm X test

train_text = []
train_label = []
test_text = []
test_label = []

TRAIN_LEN = 1500 #1676
TARGET_TRAIN_LEN = 3000
TRAIN_MIN_MAX = {
    0: [1800, 1976],
    1: [2000, 2121],
    2: [1700, 1839],
    3: [1600, 1676],
    4: [3000, 3277],
    5: [3000, 4277],
    6: [2000, 2118]
}

for fpath in filenames:
    label = labels[fpath.split('/')[-1].split('.')[0]]
    print(fpath, label)

    with open(fpath, 'r') as fp:
        data = json.load(fp)
        random.shuffle(data)

        count = 0
        for obj in data:
            count += 1
            if count > TRAIN_MIN_MAX[label][1]:
                break
            if count <= TRAIN_MIN_MAX[label][0]:
                train_label.append(label)
                # ghép title và question 
                train_text.append(obj['title'] + ' ' + obj['question'])
            else:
                test_label.append(label)
                test_text.append(obj['title'] + ' ' + obj['question'])
            if (label != 5 or label != 4) and count <= TARGET_TRAIN_LEN - TRAIN_MIN_MAX[label][0]:
                train_label.append(label)
                obj1 = data[random.randrange(0, TRAIN_MIN_MAX[label][0])] 
                train_text.append(obj['title'] + ' ' + obj['question'] + ' ' + obj1['title'] + ' ' + obj1['question'])


print(len(train_text), len(train_label), max(train_label))
print(len(test_text), len(test_label), max(test_label))
### OUTPUT
# 11732 11732
# 9044 9044

word_vectorizer = TfidfVectorizer(max_features=20000)
word_vectorizer.fit(train_text)

x_train = word_vectorizer.transform(train_text)
x_test = word_vectorizer.transform(test_text)

# parse sang numpy
print(type(x_train)) # <class 'scipy.sparse.csr.csr_matrix'>
x_train = x_train.toarray()
x_test = x_test.toarray()
print(type(x_train)) # <class 'numpy.ndarray'>
print(x_train.shape, x_test.shape)

y_train = to_categorical(train_label)
y_test = to_categorical(test_label)
print(y_train.shape, y_test.shape)

mymodel = build_model(x_train.shape[1], y_train.shape[1])
mymodel.summary()

history = mymodel.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=20, batch_size=16)

acc = history.history['accuracy']
loss = history.history['loss']
epochs = range(1, len(acc) + 1)

plt.plot(epochs, acc, 'b', label='Training acc')
plt.title('Training accuracy')
plt.legend()
plt.savefig('acc.png', bbox_inches='tight')
plt.close()

plt.plot(epochs, loss, 'b', label='Training loss')
plt.title('Training loss')
plt.legend()
plt.savefig('loss.png', bbox_inches='tight')
#
#plt.show()

mymodel.save("model.h5")

