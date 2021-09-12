import csv
import requests
import re

def getjson(url):
    i = 0
    while i < 3:
        try:
            response = requests.get(url, timeout=15)
            return response
        except requests.exceptions.RequestException:
            i += 1
    
with open('c:/Users/matsj/Desktop/douban_movie/douban_movie.csv',encoding="utf-8-sig") as file_from, open('c:/Users/matsj/Desktop/douban_movie/douban_movie_with_imdb.csv', 'w',encoding="utf-8-sig", newline='') as file_to:
    list_no_imdb = csv.reader(file_from)
    csv_write = csv.writer(file_to)
    for list in list_no_imdb:
        if list[6] == '条目链接':
            csv_head = [list[0], list[1], list[2], list[3], list[4], list[5], list[6], 'imdbId']
            csv_write.writerow(csv_head)
        else:
            movie_num = re.findall('\d+', list[6])
            url = 'https://movie.querydata.org/api?id='+ str(movie_num[0])
            json = getjson(url).json()                   #获取requests返回对象的json内容，即电影信息。
            #假如返回内容里有imdbId
            if 'imdbId' in json:                
                csv_row = [list[0], list[1], list[2], list[3], list[4], list[5], list[6], json['imdbId']]
                csv_write.writerow(csv_row)
            #假如没有imdbId
            else:
                csv_row = [list[0], list[1], list[2], list[3], list[4], list[5], list[6]]
                csv_write.writerow(csv_row)
file_from.close()
file_to.close()