#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author:  Analyst1981@gmail.com
# @date:    2019-02-15
from bs4 import BeautifulSoup
import random
import requests
requests.packages.urllib3.disable_warnings()
import time
import pandas as pd
import re

def get_html(url,start):
    headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36', 
                'Upgrade-Insecure-Requests': '1', 
                'Connection':'keep-alive',
                'Host':'movie.douban.com',
                }     
    data={
        'start':start,
        'limit':20,
        'sort':'new_score',
        'status':'P',
    }
    #https://movie.douban.com/subject/26266893/comments?start=20&limit=20&sort=new_score&status=P
    starts=[]
    _eval=[]
    nickname=[]
    link=[]
    img_link=[]
    votes=[]
    comments_time=[]
    comments=[]
    while(start<2000):
        time.sleep(random.randint(0,10))
        
        response = requests.get(url,headers=headers, verify=False,params=data,timeout=10).text
        soup = BeautifulSoup(response, "lxml")
        for comment in soup.find_all('div',class_="comment-item"):
            #print(len(comment))
            #print(comment)
            ava_a =comment.find('div',class_="avatar").find('a')
            nickname.append(ava_a.attrs['title'])
            link.append(ava_a.attrs['href'])
            img_link.append(ava_a.find('img').attrs['src'])
            com =comment.find('div',class_="comment")
            votes.append(com.find('span',class_="votes").get_text()) #get_text()==.string
            comments_time.append(com.find('span',class_="comment-time").get_text())
            comments.append(com.find('span',class_="short").string) #get_text()

            com_span=com.find('span',class_="comment-info")
            starts.append(re.findall(r'<span class="allstar(.+) rating" title=".+"></span>',str(com_span),re.S)[0])
            _eval.append(re.findall(r'<span class=".+" title="(.+)"></span>',str(com_span),re.S)[0])
            
        start+=20
        print("开始爬取第{}条评论".format(start))
    comment_dict={'nickname':nickname,
                  'link':link,
                  'img_link':img_link,
                  'votes':votes,   
                  'comments_time':comments_time,
                  'comments':comments,
                  }
    return comment_dict
def main():
    start_time = time.time()  # 结束时间
    url_base='https://movie.douban.com/subject/26266893/'
    #'https://movie.douban.com/subject/26266893/comments?status=P'
    start=0
    url =url_base+'/comments'
    print("开始爬取")
    comments=get_html(url,start)
    name=['nickname','link','img_link','start','eval','votes','comments_time','comments']
    print("开始写入文件!")
    comment=pd.DataFrame(columns=name,data=comments)
    #comment.head()
    comment.to_csv(r'liulang.csv',encoding='utf_8_sig')
    print("--------------")
    end_time = time.time()  # 结束时间
    print("程序耗时%f秒." % (end_time - start_time))
    print("已完成")    
if __name__ == '__main__':
    main() 