import csv

import requests

from lxml import etree


def main(page):
    url = 'https://www.douban.com/doulist/45004834/?start=' + str(25 * page) + '&sort=time&playable=0&sub_type='
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0'}
    html = url_request(url, headers = headers)
    books = parse(html)
    save_to_csv(page, books)

def url_request(url, headers):
    response = requests.get(url, headers = headers)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse(html):
    content = etree.HTML(html)
    title_list = content.xpath('//div[@class="title"]/a/text()')
    title_list = [_.strip() for _ in title_list]
    rating_list = content.xpath('//div/span[@class="rating_nums"]/text()')
    rating_list = ['评分: ' + _ for _ in rating_list]
    abstract = content.xpath('//div[@class="abstract"]/text()')
    author_list = []
    publisher_list = []
    publish_year = []
    for line in abstract:
        if '\n      \n          ' in line:
            if '作者' in line:
                author_list.append(line)
            else:
                author_list.append('作者: 无')
                if '\n          ' in line:
                    if '\n          出版社' in line or '\n          出版年' in line:
                        if '\n          出版社' in line :
                            publisher_list.append(line)
                    else:
                        publish_year.append(line)
        elif '\n          ' in line:
            if '\n          出版社' in line or '\n          出版年' in line:
                if '\n          出版社' in line :
                    publisher_list.append(line)
                else:
                    publish_year.append(line)             
    author_list = [_.strip() for _ in author_list]
    publisher_list = [_.strip() for _ in publisher_list]
    publish_year = [_.strip() for _ in publish_year]
    if len(title_list) == len(rating_list) == len(author_list) == len(publisher_list) == len(publish_year):
        books = list(zip(title_list, rating_list, author_list, publisher_list, publish_year))
        return books
    else:
        return None

def save_to_csv(page, books):
    if not books:
        err_msg = 'Information lost on page {}.'
        print('\n' + err_msg.format(page + 1) + '\n\n')
        with open('error.log', 'w') as f:
            f.write(err_msg.format(page + 1) + '\n')
    else:
        for book in books:
            print("writing book info ==> " + book[0] + '\n')

            with open('douban_books_top100.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(list(book))

if __name__ == '__main__':
    for i in range(4):
        main(i)
