from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import requests
import csv
import string


url = 'https://medlatec.vn'

prefix = 'hoi-dap'
category = 'y-hoc-co-truyen-c56'

page_idx = 0
fieldnames = ['id', 'link', 'title', 'author', 'date', 'question']

with open(f'{category}.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

def crawl_one_page(page_idx):
    soup = BeautifulSoup(urllib.request.urlopen(f'{url}/{prefix}/{category}/{page_idx}'), 'html.parser')
    q_div_list = soup.find_all('div', {'class': 'faq-archive--content'})
    for q_div in q_div_list:
        try:
            answer_div = q_div.find('a', href=True)
            answer_link = answer_div['href']
            q_id = answer_link.split('-')[-1].split('#')[0]

            try:
                title = answer_div['title']
            except:
                title = ''

            info = q_div.find('div', {'class': 'faq-archive--info clearfix'})
            try:
                author = info.find('div', {'class': 'faq-archive--author'}).text.strip()
            except:
                author = ''

            try:
                date = info.find('div', {'class': 'faq-archive--date'}).text.strip()
            except:
                date = ''

            q_detail_div = q_div.find_all('div', {'class': 'faq-archive--desc'})
            question = ' '.join([' '.join(q_text.text.split()) for q_text in q_detail_div])

            print(f'-{q_id}-')
            #print(f'-{answer_link}-')
            #print(f'-{title}-')
            #print(f'-{author}-')
            #print(f'-{date}-')
            #print(f'-{questions}-')
            #print('===============================================================')
            with open(f'{category}.csv', 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'id': q_id, 'link': answer_link, 'title': title, 'author': author, 'date': date, 'question': question})
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
