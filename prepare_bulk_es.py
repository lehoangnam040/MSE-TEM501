import json
import os
src_dir = './category_preprocess_with_keywords'
filenames = []
for (dirpath, dirnames, filenames1) in os.walk(src_dir):
    for fp in filenames1:
        filenames.append(f'{src_dir}/{fp}')
    break
   
with open('es_bulk.json', 'w', encoding='utf8') as fp:
    pass


labels = {
    'lâm sàng cận lâm sàng': 0, 
    'liên khoa mắt tai mũi họng răng hàm mặt da liễu': 1, 
    'ngoại': 2,
    'nhi': 3, 
    'nội': 4,
    'sản': 5,
    'truyền nhiễm': 6
}

for filename in filenames:
    data = []
    with open(f'{filename}', 'r') as fp:
        data = json.load(fp)
    label = filename.split('/')[-1].split('.')[0]
    label_num = labels[label] 
    
    for q in data:
        _id = q.pop('_id')
        q['category'] = label_num
        with open('es_bulk.json', 'a', encoding='utf8') as fp:
            fp.write(json.dumps({"index":{"_id":_id}}, ensure_ascii=False))
            fp.write('\n')
            fp.write(json.dumps(q, ensure_ascii=False))
            fp.write('\n')
