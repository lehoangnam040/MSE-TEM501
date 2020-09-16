import csv

def find_wrong_category_question(file_path, keywords):
    '''
    Tìm những câu hỏi trong 1 file mà chứa những từ của category khác, do ng dùng gửi nhầm
    '''
    with open(file_path, 'r') as fp:
        reader = csv.reader(fp, delimiter=',')
        for row in reader:
            _id = row[0]
            title = row[2]
            q = row[5]

            for keyword in keywords:
                if keyword in title or keyword in q:
                    print(_id, title)
                    print(q)
                    print('=======================')


if __name__ == '__main__':
    print('Hello')

    # mắt
    # ung thư
    find_wrong_category_question('./preprocess_wrong_file/da-khoa-c73.csv', ['tai', 'mũi', 'họng'])
