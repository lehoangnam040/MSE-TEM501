import preprocess as my_preproc
import os

def add_spaces_category():
    src_dir = 'category'
    dst_dir = 'category_add_spaces'

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
                
                dst_title = my_preproc.add_space_in_sentence(title) 
                dst_q = my_preproc.add_space_in_sentence(q) 
                with open(f'{dst_dir}/{filename}', 'a') as fp1:
                    fp1.write(f'{dst_title}\t{dst_q}\n')


def remove_non_alphabet_unicode():
    src_dir = 'category_add_spaces'
    dst_dir = 'category_only_alphabet'
    
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
                
                dst_title = my_preproc.remove_special_character_number(title) 
                dst_q = my_preproc.remove_special_character_number(q) 
                with open(f'{dst_dir}/{filename}', 'a') as fp1:
                    fp1.write(f'{dst_title}\t{dst_q}')

def tokenize_word():
    """
    using CocCoc tokenizer
    """
    src_dir = 'category_only_alphabet'
    dst_dir = 'category_tokenizer'
    
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
                
                dst_title = my_preproc.tokenizer(title) 
                dst_q = my_preproc.tokenizer(q) 
                with open(f'{dst_dir}/{filename}', 'a') as fp1:
                    fp1.write(f'{dst_title}\t{dst_q}')



def remove_stop_words():
    src_dir = 'category_tokenizer'
    dst_dir = 'category_non_stop_words'
    stop_multiple_words = ['bác sỹ']

    stop_words = ['có', 'em', 'bị', 'và', 'bác_sĩ', 'tôi', 'thì', 'bệnh_viện', 'medlatec',  'cám_ơn', 'cảm_ơn', 'nguyên_nhân', 'hỏi',
            'e', 'ạ', 'vâng', 'bs', 'bv', 'nhưng', 'chào', 'là']


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
                
                dst_title = my_preproc.remove_stop_words(title, stop_multiple_words, stop_words) 
                dst_q = my_preproc.remove_stop_words(q, stop_multiple_words, stop_words)
                with open(f'{dst_dir}/{filename}', 'a') as fp1:
                    fp1.write(f'{dst_title}\t{dst_q}\n')

if __name__ == '__main__':
    #remove_only_alphabet_unicode()
    remove_stop_words()
    #tokenize_word()
