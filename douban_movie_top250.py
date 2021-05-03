import csv
import requests

from lxml import etree

def main(page):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0'}
    url = 'https://movie.douban.com/top250?start=' + str(25*page) + '&filter='
    html = url_request(url, headers=headers)
    results = html_parse(html)
    save_to_csv(page, results)

def url_request(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None

def html_parse(html):
    content = etree.HTML(html)
    title_list = []
    ranking_list = []
    score_list = []
    author_list = []
    intro_list = []

    item_num = int(content.xpath('count(//li/div[@class="item"])'))

    for i in range(1, item_num+1):
        title = content.xpath('//li[' + str(i) + ']//div[@class="item"]/div[@class="info"]/div[@class="hd"]/a/span[@class="title"][1]')
        if title != []:
            title_list.append(title[0].text.strip())
        else:
            title_list.append("无标题")
        
    for i in range(1, item_num+1):
        ranking = content.xpath('//li[' + str(i) + ']/div[@class="item"]/div[@class="pic"]/em')
        if ranking != []:
            ranking_list.append(ranking[0].text.strip())
        else:
            ranking_list.append("无排名")

    for i in range(1, item_num+1):
        score = content.xpath('//li[' + str(i) + ']/div[@class="item"]/div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]')
        if score != []:
            score_list.append(score[0].text.strip())
        else:
            score_list.append("无评分")

    for i in range(1, item_num+1):
        author = content.xpath('//li[' + str(i) + ']/div[@class="item"]/div[@class="info"]/div[@class="bd"]/p[@class=""]')
        if author != []:
            author_list.append(author[0].text.strip())
        else:
            author_list.append("无作者")
        
    for i in range(1, item_num+1):
        intro = content.xpath('//li[' + str(i) + ']/div[@class="item"]/div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span[@class="inq"]')
        if intro != []:
            intro_list.append(intro[0].text.strip())
        else:
            intro_list.append("无简介")

    if len(title_list) == len(ranking_list) == len(score_list) == len(author_list) == len(intro_list):
        return zip(title_list, ranking_list, score_list, author_list, intro_list)
    else:
        return None

def save_to_csv(page, results):
    if results is None:
        err_msg = 'Information lost on page {}.'
        print('\n' + err_msg.format(page + 1) + '\n\n')
        with open('error.log', 'w') as f:
            f.write(err_msg.format(page + 1) + '\n')
    else:
        for result in results:
            print("写入电影信息 ==> " + result[0] + '\n')

            with open('douban_movie_top250.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(list(result)) 

if __name__ == '__main__':
    for i in range(10):
        main(i)
