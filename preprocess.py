import os

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


def add_space_in_sentence(sentence):
    dst = []
    for word in sentence.split():
        dst.append(add_space_between_word_and_special_char(word))
    return ' '.join(dst)


if __name__ == '__main__':
    src_dir = 'category'
    dst_dir = 'preproc_category'

    filenames = []
    for (dirpath, dirnames, filenames1) in os.walk(src_dir):
         filenames = filenames1
         break

    for filename in filenames:
        with open(f'{dst_dir}/{filename}', 'w') as fp1:
            pass

        with open(f'{src_dir}/{filename}', 'r') as fp:
            for line in fp:
                try:
                    title, q = line.split('\t')
                except Exception as e:
                    print(e)
                    print(line.split('\t'))
                    print(filename, title, q)
                
                dst_title = add_space_in_sentence(title) 
                dst_q = add_space_in_sentence(q) 
                with open(f'{dst_dir}/{filename}', 'a') as fp1:
                    fp1.write(f'{dst_title}\t{dst_q}\n')
