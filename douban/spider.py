from urllib import request
import sys
import warnings
warnings.filterwarnings("ignore")
import re
import jieba
import pandas as pd
import numpy
import matplotlib
matplotlib.rcParams['figure.figsize']=(10.0,5.0)
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as bs 
#!!! python 3.0 以下下载 BeautifulSoup   python3.0 以上 pip install BeautifulSoup4
#!!! BeautifulSoup4 在python3 中改名bs4
#!!! BeautifulSoup将html解析为对象进行处理，全部页面转变为字典或者数组


# #################################################################################
# 分析页面内容 获取电影名 和 电影id 
# /data-subject属性里面放了电影的id号码/img标签的alt属性里面放了电影的名字
def  getNowPlayingMovieList():
	resp = request.urlopen('https://movie.douban.com/nowplaying/hangzhou')
	html_data = resp.read().decode('utf-8')
	soup = bs(html_data,'html.parser')
	nowplaying_movies = soup.find_all('div',id = 'nowplaying')
	nowplaying_movies_list = nowplaying_movies[0].find_all('li',class_='list-item')
	nowplaying_list = []
	for item in nowplaying_movies_list:#every item means the sub-set label of label div
		nowplaying_dict={}
		nowplaying_dict['id'] = item['data-subject']
		for tag_img_item in item.find_all('img'):
			nowplaying_dict['name'] = tag_img_item['alt']
			nowplaying_list.append(nowplaying_dict)
	return nowplaying_list 

def getCommentById(movieId,pageNum):
	eachCommentList = []
	if pageNum>0:
		start = (pageNum-1)*20
	else:
		return False
	requrl = 'https://movie.douban.com/subject/'+movieId+'/comments'+'?'+'start='+str(start)+'&limit=20'
	print(requrl)
	resp = request.urlopen(requrl)
	html_data = resp.read().decode('utf-8')
	soup = bs(html_data,'html.parser')
	comment_div_list = soup.find_all('div',class_='comment') # n
	for item in comment_div_list:
		if item.find_all('p')[0].string is not None:
			eachCommentList.append(item.find_all('p')[0].string)
	return eachCommentList

def main():
	commentList = []
	NowPlayingMovieList = getNowPlayingMovieList()
	for i in range(2):
		num = i+1
		commentListTemp = getCommentById(NowPlayingMovieList[0]['id'],num)
		commentList.append(commentListTemp)
	comments =''
	for k in range(len(commentList)):
		comments = comments+str(commentList[k]).strip()
	pattern  = re.compile(r'[\u4e00-\u9fa5]+')
	filterdata = re.findall(pattern,comments)
	cleaned_comments = ''.join(filterdata)

	segment = jieba.lcut(cleaned_comments)
	words_df = pd.DataFrame({'segment':segment})

	stopwords = pd.read_csv("stopwords.txt",index_col=False,quoting = 3,sep="\t",names= ['stopword'],encoding ='utf-8')
	words_df = words_df[~words_df.segment.isin(stopwords.stopword)]
	print(stopwords.stopword.head(10))
	words_stat = words_df.groupby(by = ['segment'])['segment'].agg({"计数":numpy.size})
	words_stat = words_stat.reset_index().sort_values(by = ['计数'],ascending=False)

	wordcloud = WordCloud(font_path="simhei.ttf",background_color="white",max_font_size=80)
	word_frequence = {x[0]:x[1] for x in words_stat.head(1000).values}

	word_frequence_list=[]
	for key in word_frequence:
		temp = (key,word_frequence[key])
		word_frequence_list.append(temp)

	wordcloud = wordcloud.fit_words(dict(word_frequence_list))
	plt.imshow(wordcloud)
	plt.savefig("result.jpg")


main()