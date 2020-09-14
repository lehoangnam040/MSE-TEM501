from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import requests
import csv
import string


url = 'https://medlatec.vn'

prefix = 'hoi-dap'
category = 'co-xuong-khop-c9'
page_idx = 0

with open(f'{category}.csv', 'w', newline='') as csvfile:
    fieldnames = ['id','title', 'author', 'date', 'question', 'answer']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

def crawl_one_page(page_idx):
    soup = BeautifulSoup(urllib.request.urlopen(f'{url}/{prefix}/{category}/{page_idx}'), 'html.parser')
    paging = soup.find_all('div', {'class': 'faq-archive--content'})
    for page in paging:
        try:
            answer_div = page.find('a', href=True)
            answer_link = answer_div['href']
            title = answer_div['title']
            answer_page = BeautifulSoup(urllib.request.urlopen(urllib.parse.quote(f'{url}/{answer_link}', safe=string.printable)), 'html.parser')
            q_id = answer_link.split('-')[-1].split('#')[0]
  
            detail_div = answer_page.find('div', {'class': 'faq-archive--content'})
            info = detail_div.find('div', {'class': 'faq-archive--info clearfix'})
            author = info.find('div', {'class': 'faq-archive--author'}).text.strip()
            date = info.find('div', {'class': 'faq-archive--date'}).text.strip()
            questions = detail_div.find_all('div', {'class': 'faq-archive--desc'})
            questions = ' '.join([question.text.strip() for question in questions])

            reply_div = answer_page.find('div', {'class': 'faq-reply--desc'})
            answer_list = reply_div.find_all('p')
            answer = []
            for answer_p in answer_list:
                x = answer_p.findChildren()
                if len(x) == 0:
                    text = answer_p.text.strip()
                    if 'Mọi chi tiết về dịch vụ' in text:
                        continue
                    elif 'MEDLATEC' in text:
                        continue
                    elif 'các chi nhánh' in text:
                        continue
                    else:
                        answer.append(text)
                
            answer = ' '.join(answer)
            print(f'-{q_id}-')
            #print(f'-{answer_link}-')
            #print(f'-{title}-')
            #print(f'-{author}-')
            #print(f'-{date}-')
            #print(f'-{questions}-')
            #print(f'-{answer}')
            #print('===============================================================')
            with open(f'{category}.csv', 'a', newline='') as csvfile:
                fieldnames = ['id','title', 'author', 'date', 'question', 'answer']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'id': q_id, 'title': title, 'author': author, 'date': date, 'question': questions, 'answer': answer})
        except:
            continue

while(True):
    page_idx += 1
    r = requests.get(f'{url}/{prefix}/{category}/{page_idx}'.encode('utf-8'), allow_redirects=False)
    if r.status_code != 200:
        print('Finishing')
        break
   
    try:
        crawl_one_page(page_idx)
    except:
        continue

    print(f'Done page {page_idx}')

print('Done!!!')
