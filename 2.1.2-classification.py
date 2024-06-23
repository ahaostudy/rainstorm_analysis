# -*- coding: utf-8 -*-
import json

import jieba
import re
import os
from sklearn import feature_extraction, linear_model
from sklearn.metrics import classification_report

train_filepath = "./data/train/"
test_filepath = "./data/test/"
basepaths = './data/htmls'


def getdata(filepath):
    data = []
    target = []

    dirs = os.listdir(filepath)
    for dirr in dirs:
        files = os.listdir(filepath + dirr)
        for file in files:
            filename = filepath + dirr + '/' + file
            print(filename)
            try:
                with open(filename, 'rb') as fp:
                    content = fp.read().decode('utf-8')
                    content = content.replace(' ', '')  # 去掉文本中的空格
                    pattern = re.compile("[^\u4e00-\u9fa5]")
                    content = re.sub(pattern, '', content)
            except:
                print("Sorry, the file " + filename + " does not exist.")
            else:
                target.append(1 if dirr == 'positive' else 0)
                data.append(content)
    return data, target


def main():
    train_data, train_target = getdata(train_filepath)
    test_data, test_target = getdata(test_filepath)

    train_data = [" ".join(jieba.lcut(e)) for e in train_data]
    test_data = [" ".join(jieba.lcut(e)) for e in test_data]
    print(len(train_data))
    print(len(train_target))
    print('----------------')
    print(len(test_data))
    print(len(test_target))
    count_vectorizer = feature_extraction.text.CountVectorizer()
    train_vectors = count_vectorizer.fit_transform(train_data)
    test_vectors = count_vectorizer.transform(test_data)

    clf = linear_model.RidgeClassifier()
    clf.fit(train_vectors, train_target)
    labels = ['negative', 'positive']
    print(classification_report(test_target, clf.predict(test_vectors), target_names=labels))

    print('start---------')
    basepath = os.listdir(basepaths)
    testdata = []
    prefile = []
    for dir1 in basepath:
        filename = os.listdir(basepaths + '/' + dir1)
        for dir2 in filename:
            testpaths = basepaths + '/' + dir1 + '/' + dir2  # data/htmls/京津冀/保定
            testlist = os.listdir(testpaths)
            for dir3 in testlist:
                testpath = testpaths + '/' + dir3  # data/htmls/京津冀/保定/0.html
                try:
                    with open(testpath, 'rb') as fp:
                        content1 = fp.read().decode("utf8", "ignore")
                        content2 = content1.replace(' ', '')
                        pattern = re.compile("[^\u4e00-\u9fa5]")
                        content3 = re.sub(pattern, '', content2)
                except Exception as e:
                    print("Sorry, the file " + testpath + " does not exist.", e)
                else:
                    prefile.append(testpath)
                    testdata.append(content3)
    testdata = [" ".join(jieba.lcut(e)) for e in testdata]
    testvectors = count_vectorizer.transform(testdata)
    test_pre = clf.predict(testvectors)
    data = list()
    for i in range(len(test_pre)):
        data.append({'path': prefile[i], 'label': labels[test_pre[i]]})
    data.sort(key=lambda x: x['path'])
    print(json.dumps(data, ensure_ascii=False))
    print('end---------')


if __name__ == '__main__':
    main()
