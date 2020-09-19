import os
import re
from CocCocTokenizer import PyTokenizer
import json


T = PyTokenizer(load_nontone_data=True)

def add_space_between_word_and_special_char(word):
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


def remove_special_character_number(string):
    """
    Loại bỏ những kí tự  số và kí tự đặc biệt trong 1 string
    """
    return re.sub('[^a-zA-Z\săâáắấàằầảẳẩãẵẫạặậđeêéếèềẻểẽễẹệiíìỉĩịoôơóốớòồờỏổởõỗỡọộợuưúứùừủửũữụựyýỳỷỹỵaăâáắấàằầảẳẩãẵẫạặậđeêéếèềẻểẽễẹệiíìỉĩịoôơóốớòồờỏổởõỗỡọộợuưúứùừủửũữụựyýỳỷỹỵaăâáắấàằầảẳẩãẵẫạặậđeêéếèềẻểẽễẹệiíìỉĩịoôơóốớòồờỏổởõỗỡọộợuưúứùừủửũữụựyýỳỷỹỵaăâáắấàằầảẳẩãẵẫạặậđeêéếèềẻểẽễẹệiíìỉĩịoôơóốớòồờỏổởõỗỡọộợuưúứùừủửũữụựyýỳỷỹỵaăâáắấàằầảẳẩãẵẫạặậđeêéếèềẻểẽễẹệiíìỉĩịoôơóốớòồờỏổởõỗỡọộợuưúứùừủửũữụựyýỳỷỹỵaăâáắấàằầảẳẩãẵẫạặậđeêéếèềẻểẽễẹệiíìỉĩịoôơóốớòồờỏổởõỗỡọộợuưúứùừủửũữụựyýỳỷỹỵ]','', string )

def add_space_in_sentence(sentence):
    dst = []
    for word in sentence.split():
        dst.append(add_space_between_word_and_special_char(word))
    return ' '.join(dst)



def tokenizer(string):
    words = T.word_tokenize(string, tokenize_option=0)
    return ' '.join(words)

def remove_stop_words(string, stop_multiple_words, stop_words):
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


def preprocess_string(string, stop_multiple_words, stop_words):
    
    # B1: lowercase
    string = string.lower()
    # B2: thêm dấu cách, tách các chữ ra khỏi những phần dính vs số và kí tự đặc biệt

    string = add_space_in_sentence(string)

    # B3: loại bỏ số, kí tự đặc biệt
    string = remove_special_character_number(string)

    # B4: tokenizer word
    string = tokenizer(string)

    # B5: remove stop words
    string = remove_stop_words(string, stop_multiple_words, stop_words)

    return string


if __name__ == '__main__':
    #res = remove_stop_words('tử cũng có khối trống âm thành dày	chào bác sĩ   e có câu hỏi muốn hỏi bác sĩ ạ   kinh nguyệt của e lâu nay không đều   và e có tiền sử thai lưu             thai trứng           ạ   kì kinh gần nhất của em thời gian này                      kinh ra ít và có màu đen   thì đến ngày          em thử que lên   vạch nhưng đang mờ   nên e có đi khám làm xét nghiệm beta và siêu âm thì kết quả xét nghiệm là        siêu âm mọi thứ bình thường và chưa thấy gì   đến ngày           em có thử que và lần này thì vạch đã đậm hơn và e cũng đi khám lại   kết quả xét nghiệm beta lần khám      là        kết quả siêu âm   tử cung có khối trống âm thành dày   đường kính  mm   và kết luận của bác sĩ siêu âm là   td thai mới làm tổ trong buồng tử cung   liệu kết quả như vậy là e đã có thai hay chưa ạ   có nguy hiểm gì kg thưa bác sĩ   và khối trống âm kia là ntn ạ   cảm ơn bác sĩ đã lắng nghe câu hỏi của e', ['bác sĩ', 'câu hỏi', 'hỏi', 'cảm ơn', 'cho em hỏi', 'bệnh viện', 'medlatec'], ['e', 'ạ', 'vâng', 'bs', 'bv'])
    #print(res)

    src_dir = 'category'
    dst_dir = 'category_preprocess'
    stop_multiple_words = ['bác sỹ']

    stop_words = ['có', 'em', 'bị', 'và', 'bác_sĩ', 'tôi', 'thì', 'bệnh_viện', 'medlatec',  'cám_ơn', 'cảm_ơn', 'nguyên_nhân', 'hỏi',
            'e', 'ạ', 'vâng', 'bs', 'bv', 'nhưng', 'chào', 'là']


    filenames = []
    for (dirpath, dirnames, filenames1) in os.walk(src_dir):
         filenames = filenames1
         break

    for filename in filenames:
        res = []    
        
        #with open(f'{dst_dir}/{filename}', 'w') as fp1:
        #    pass

        with open(f'{src_dir}/{filename}', 'r') as fp:
            for line in fp:
                try:
                    title, q = line.split('\t')
                except Exception as e:
                    print(e)
                    print(line.split('\t'))
                    print(filename, title, q)
                               
                dst_title = preprocess_string(title, stop_multiple_words, stop_words) 
                dst_q = preprocess_string(q, stop_multiple_words, stop_words)
                #with open(f'{dst_dir}/{filename}', 'a') as fp1:
                #    fp1.write(dst_title + ' ' + dst_q)
                res.append({
                    'title': dst_title,
                    'question': dst_q
                })
        filename = filename.replace('.txt', '.json')

        with open(f'{dst_dir}/{filename}', 'w', encoding='utf8') as fp1:
            json_object = json.dumps(res, indent = 4, ensure_ascii=False)
            fp1.write(json_object)
