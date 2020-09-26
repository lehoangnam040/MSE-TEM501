# MSE-TEM501

# Tiền xử lí dữ liệu
Thống kê các từ xuất hiện ở các category, nhận xét như sau:
- từ hay bị dính với dấu, ví dụ dấu phẩy, chấm, chấm hỏi, chấm than, ba chấm  dính với các từ
- từ dính với số <br/>
-> tạo dấu cách giữa các từ với số, kí tự đặc biệt
- có rất nhiều từ nhiễu -> coi nó như stopword và remove

# Cấu trúc thư mục
## Các file dùng cho việc serving, cho người dùng
- server.py: file chạy server python để serving
- model.h5: model question classification
- text_vectorize.json: text dùng để Tf-Idf vectorizer
- frontend: thư mục chứa file .html để làm giao diện cho 3 tasks
- Dockerfile: build docker cho service
- setup_coccoc.py: dùng cho việc cài đặt CoccocTokenizer cho docker
- requirements.txt: các thư viện dùng cho service

## Các file của crawl
- crawl.py: file crawl chính, chứa các script crawl bằng beautifulSoup
- raw: file .csv gốc crawl từ medlatec
- category: từ 43 mục của medlatec, gộp lại và chia thành 7 mục, chi tiết xem file category.txt
- category.txt: cách gộp các mục nhỏ lại thành các mục to có liên quan đến nhau, có tham khảo người làm trong lĩnh vực y tế
- category_reconstruct.py: script để gộp các category lại với nhau

## Training
- category_add_spaces: thư mục category sau khi đã thêm dấu cách giữa từ và số, kí tự đặc biệt
- category_only_alphabet: thư mục category sau khi đã remove hết số, kí tự đặc biệt
- category_tokenizer: thư mục category sau khi dùng CoccocTokenizer
- category_non_stop_words: thư mục category sau khi đã remove các stop words tự định nghĩa
- category_preprocess: thư mục kết quả, sẵn sàng cho training
- preprocess_category.py: script cho tiền xử lí, thử nghiệm để ra được từng thư mục nhỏ
- preprocess.py: thư mục chính để tiền xử lí từ folder category  -> category_preprocess
- training.py và TEM501_task1.ipynb: các file cho việc training
- statistic.py: script thống kê trong quá trình chuẩn bị dataset

## Keywords cloud
- keywords_extraction.py: file để extract keyword
- category_preprocess_with_keywords: thư mục category đã preprocess và extract keyword
- prepare_bulk_es.py: script để ra được file es_bulk.json bên dưới, input là thư mục category_preprocess_with_keywords bên trên  
- es_bulk.json: danh sách câu hỏi đã có keyword, làm input để indexing vào Elasticsearch
- script bulk indexing ES: curl -s -H "Content-Type: application/json" -XPOST localhost:9200/questions/docs/_bulk --data-binary "@es_bulk.json"

## Kết quả việc training và evaluate cho task: question classification

![Accuracy](<images/training_acc.png>)
![Loss](<images/training_loss.png>)
![Confusion matrix](<images/cm.png>)


