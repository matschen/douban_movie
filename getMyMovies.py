import requests
from bs4 import BeautifulSoup
import re
import csv
import time
import random

def main(path_csv, douban_id):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    }

    # write movie information to csv
    with open('movie.csv', 'w',encoding="utf-8-sig", newline='') as file_to:
        csv_write = csv.writer(file_to)
        title = ['title', 'Directors', 'casts', 'nation', 'year', 'imdbID', 'douban_url', 'Rating', 'Review', 'WatchedDate'  ]
        csv_write.writerow(title)   # write title to csv file

        url_my_movies = '/people/' + str(douban_id) + '/collect?sort=time&amp;start=0&amp;filter=all&amp;mode=list&amp;tags_sort=count' #我看过的电影的第一页

        while url_my_movies:
            requests_url_my_movies = requests.get('https://movie.douban.com' + url_my_movies, headers=headers)
            content_url_my_movies = requests_url_my_movies.text
            soup_url_my_movies = BeautifulSoup(content_url_my_movies, 'lxml')
            
            # get 1.movie_name, 2.director, 3.casts, 4.nation, 5.year, 6.imdb_id, 7.movie_url, 8.rating, 
            # 9.review, 10. watched_Date
            movie_items = soup_url_my_movies.find_all('li', class_='item')  # get all movies information 
            
            for item in movie_items:
                movie_url = item.div.a['href']

                movie_name = item.div.a.string.strip()
                
                content = item.find('div', class_='date').contents

                # if there is no rating, rating = ""
                if len(item.find('div', class_='date').contents) > 1:
                    rating = re.findall("[1-5]{1}" ,item.find('div', class_='date').find('span')['class'][0])[0]
                else:
                    rating = ''

                watched_date = item.div.div.next_sibling.next_sibling.text.strip()

                if item.find('div', class_='comment'):
                    review = item.find('div', class_='comment').text.strip().replace("\n", "")
                else:
                    review = ''
            
                years = ""
                year_list = re.findall("\w{4}-\w{2}-\w{2}\([\u4e00-\u9fa5]{0,}\)", item.find('span', class_='intro').string)
                if len(year_list) > 0:
                    for year in year_list:
                        years = years + " " + year
                    years = years.strip()
                else:
                    years = ""

                # get imdb ID
                time.sleep(random.uniform(0,5))
                r = requests.get(movie_url,headers=headers, verify=False)  # sometimes port=433 error, need to add verify=False
                requests.packages.urllib3.disable_warnings()
                if r.status_code != 200:
                    print("movie %movie_name is not accessible" %movie_name)
                    continue  
                content = r.text
                soup = BeautifulSoup(content, 'lxml')

                movie_info = soup.find_all('div', id='info')[0].text  # movie info string including imdb
                if len(re.findall("[t]{2}[0-9]{7}", movie_info)) > 0:
                    imdb_id = re.findall("[t]{2}[0-9]{7}", movie_info)[0]
                else:
                    imdb_id = ""
                
                if soup.find('a', rel="v:directedBy") != None:
                    director = soup.find('a', rel="v:directedBy").string
                else:
                    director = ''
                
                #
                casts = ''
                casts_set = soup.find_all('a', rel="v:starring")  # type ResultSet, must converted to string
                for cast in casts_set:
                    casts = casts + ' ' + cast.string
                casts = casts.strip()

                nation_list = re.findall("制片国家/地区:\s[\u4e00-\u9fa5]{1,}[\s\/\s[\u4e00-\u9fa5]{0,}]{0,}\n", movie_info)
                if len(nation_list) > 0:
                    nation = nation_list[0][9:].replace("\n", "") # remove "制片国家/地区:" and "\n" in str 
                
                # put all inforamtion of a film in a list.
                movie = [movie_name, director, casts, nation, years, imdb_id, movie_url, rating, review, watched_date]
                csv_write.writerow(movie)
                
            if soup_url_my_movies.find('span', class_='next').find('a'):       #判断span内是否含有网页链接，若没有则为最后一页 
                url_next_page = soup_url_my_movies.find('span', class_='next').a['href']  #提取下一页看过的电影的地址
                url_my_movies = url_next_page
            else:
                url_my_movies = 0                              #若为最后一页则跳出while循环
    file_to.close()


if __name__ == '__main__':
    main('movie.csv', 12345678)
