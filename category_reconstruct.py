import csv

category_meta = {

    'lâm sàng': {
        'kw': ['xét nghiệm máu', 'huyết học', 'di truyền', 'hóa sinh']
    }
}

def find_wrong_category_question(file_path, keywords):
    '''
    Tìm những câu hỏi trong 1 file mà chứa những từ của category khác, do ng dùng gửi nhầm
    '''
    with open(file_path, 'r') as fp:
        reader = csv.reader(fp, delimiter=',')
        for row in reader:
            _id = row[0]
            title = row[2].lower()
            q = row[5].lower()

            for keyword in keywords:
                if keyword in title or keyword in q:
                    print(f'{title}\t{q}')
                    break


def recategory(old_categories, new_category):
    """
    Gộp 1 số categories vào 1 category mà những cái cũ liên quan đến nhau
    File category đích sẽ chỉ có title và question, tất cả lower case
    """
    with open(f'./category/{new_category}.txt', 'w') as fp:
        for old_category in old_categories:
            i = 0
            with open(f'./raw/{old_category}.csv', 'r') as cfp:
                reader = csv.reader(cfp, delimiter=',')
                for row in reader:
                    i += 1
                    if i == 1:
                        continue
                    title = str(row[2]).lower()
                    q = str(row[5]).lower()
                    fp.write(f'{title}\t{q}\n')


if __name__ == '__main__':
    print('Hello')
    #recategory(['tim-mach-c35', 'noi-tiet--tieu-duong-c34', 'noi-tiet-sinh-duc-c21', 'lao-c31', 'ho-hap-c55', 'than-kinh-c25', 
    #    'tieu-hoa--gan-mat-c5', 'lao-khoa-c16', 'noi-khoa-c33', 'tam-than-c24', 'ung-thu-c6', 'nam-hoc-c27'], 'nội') 

    #recategory(['co-xuong-khop-c9', 'tiet-nieu-c19', 'ngoai-khoa-c32', 'hoi-suc-cap-cuu-c57', 'phau-thuat-tham-my-c39', 
    #    'tham-my-tao-hinh-c62', 'phuc-hoi-chuc-nang-c60'], 'ngoại')

    #recategory(['san--phu-khoa-c4'], 'sản')

    #recategory(['truyen-nhiem-c10', 'viem-gan-virus-c3'], 'truyền nhiễm')

    #recategory(['nhi-khoa-c7', 'so-sinh-c61', 'tiem-chung-vaccin-c76'], 'nhi')

    #recategory(['mat-c15', 'tai--mui--hong-c14', 'rang--ham--mat-c13', 'di-ung-c22', 'da-lieu-c26'], 
    #        'liên khoa mắt tai mũi họng răng hàm mặt da liễu')

    #recategory(['chan-doan-hinh-anh-c17', 'giai-phau-benh-c28', 'hoa-sinh-c30', 'ky-sinh-trung-c23', 'vi-sinh-c29', 'di-truyen-c74', 'huyet-hoc-c11'], 'lâm sàng cận lâm sàng')

    #recategory([], 'khác')
    #find_wrong_category_question('./raw/chuyen-muc-khac-c20.csv', ['tim ', 'gan ', 'thận ', 'ho ', 'tiểu đường ', 'tiêu hóa ', 'nội soi '])
    find_wrong_category_question('./raw/chuyen-muc-khac-c20.csv', ['bé '])

    #find_wrong_category_question('./raw/dinh-duong-c18.csv', ['đau cơ', 'mỏi gối', 'cứng khớp', 'tê bì chân tay', 'thẩm mỹ', 'phục hồi chức năng'])

    #find_wrong_category_question('./raw/dinh-duong-c18.csv', ['mắt ', 'tai ', 'mũi ', 'họng ', 'răng ', 'lợi ', 'da '])

    #with open('./raw/dich-vu-c64.csv', 'r') as fp:
    #    reader = csv.reader(fp, delimiter=',')
    #    for row in reader:
    #        _id = row[0]
    #        if _id not in ['q41847', 'q48457', 'q41848', 'q34659','q55359','q47873', 'q31511','q41243','q48609','q55574','q42362',
    #            'q33768','q34549','q48509','q49276','q49419',
    #            'q42362','q33768','q34549','q48509','q49276','q49419', 'q32651', 'q45419', 'q48468']:
    #            print(_id)
    #            print(row[2].lower())
    #            print(row[5].lower())

