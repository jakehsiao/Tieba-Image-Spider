#更新日志
'''
315 10:09 他妈的这个Sublime老吞我更新 真他妈的操蛋 #其实是我的锅我在隔壁按了Ctrl+S就GG了呗
315 10:46 改善了文件存储 这回更好玩了哈哈哈
315 18:41 改善了帖子储存 一点bug调一下而已
315 23:06 增加了count系统 可以数进了多少个帖子 同时帖子储存时带名字 傻逼idle老子再也不用你了垃圾玩意
316 13:58 增加了TimeOut 增加了一些Try Except增强运行性 还有如果第一页没图的帖子就不用爬了
316 21:21 增加多线程 哈哈哈哈这速度简直酸爽 还有 如果抵达500 请加入一个新县城！谢谢合作！
316 22:40 修复了一个致命bug 该bug导致一页爬5遍
317 9:22 加帖子改为多线程 保存图片作为线程分离 速度更快
'''

import numpy
from bs4 import BeautifulSoup
import requests
import lxml
import sqlite3
import time
import uuid
import os
import urllib
import threading

defaultPath='E:\GoodSpiders\\tiebaSpider'


count=0
class fileOperator(object):
	''' manage the store and load of files'''
	def __init__(self,localPath=defaultPath):
		self.path=localPath #path用path就好
		self.barName=''
		self.tieName=''
		self.f=0

	def generateFileName(self): 
	#生成一个文件名字
	#tiename 只在这里改动 就足够了
		try:
			fileName=self.path+'_'+self.barName+'\\'+self.tieName+str((uuid.uuid1()))+'.jpg'
			self.f=open(fileName,'wb')
		except Exception as e:
			print('wrong')
			fileName=self.path+'_'+self.barName+'\\'+str((uuid.uuid1()))+'.jpg'
			self.f=open(fileName,'wb')
		return str(uuid.uuid1())  


	#输入url，调用self.generateFileName保存图片，其中localPath需要在类里定义
	def getAndSaveImg(self,imgUrl):  
	    if(len(imgUrl)!= 0):
        	#fileName=self.path+'_'+self.barName+'\\'+self.tieName+self.generateFileName()+'.jpg'

        	#对于这个indentation的bug 我真的 真的 真的 很无奈 他妈的怎么整啊
        	self.generateFileName()
        	f=self.f #finishGenerating
	        try:
	        	f.write(urllib.request.urlopen(imgUrl).read())
	        	f.close()
	        	global count
	        	count+=1
	        	print('Saved! '+str(count))
	        except:
	        	print('出错了 保存失败')
	        finally:
	        	pass 

	#输入url的list，然后一张一张下，这个函数有些小多余但是还是写上吧
	#Barname entrance
	def downloadImg(self,urlList,barName,tieName=''): 
	    self.barName=barName
	    self.tieName=tieName
	    if not os.path.isdir(self.path+'_'+self.barName):
	    	os.mkdir(self.path+'_'+self.barName)
	    	print('文件夹已创建')
	    else:
	    	print('文件夹已存在')

	    for urlString in urlList:
	        self.getAndSaveImg(urlString)  


class dbOperator(object):
	"""operate the sqlite db in a more abstract way"""
	def __init__(self,dbPath,tblName='tiezi'):
		self.dbPath=dbPath
		self.conn=sqlite3.connect(dbPath,check_same_thread=False)
		self.cu=self.conn.cursor()
		self.tblName=tblName

	def finishDb(self):
		self.conn.commit()
		self.conn.close()
	def commit(self):
		self.conn.commit()

	def changeCurrentTbl(self,newTbName):
		self.tblName=newTbName

	def cvt(self,a): # a is str or int, convert str to 'str', int to str(int)
	    if type(a)==int:
	        return str(a)
	    else:
	        return '\''+str(a)+'\''
	def select(self):
	    self.cu.execute("select * from "+self.tblName)
	    return self.cu.fetchall()
	def insert(self,data):
	    insertStr='(' #initial insertion
	    for d in data:
	        d=self.cvt(d)
	        insertStr+=d
	        insertStr+=','
	    insertStr=insertStr[:-1] #out last ,
	    insertStr+=')'#finish insertion
	    #test
	    #print 'insert into '+tblName+' values '+insertStr
	    #test
	    try:
	    	self.cu.execute('insert into '+self.tblName+' values '+insertStr)
	    except Exception as e:
	    	pass
	def update(self,valName,value,name):#用不着
	    #print 'update '+tblName+' set '+valName+'='+cvt(value)+' where name='+cvt(name)
	    self.cu.execute('update '+self.tblName+' set '+valName+'='+self.cvt(value)+' where name='+self.cvt(name))

	def delete(self,name):
	    #print 'update '+tblName+' set '+valName+'='+cvt(value)+' where name='+cvt(name)
	    query='delete from '+self.tblName+' where url='+self.cvt(name)
	    print(query)
	    try:
	    	self.cu.execute(query) #changed
	    except:
	    	print('数据库移除时出错')
	    finally:
	    	self.commit()

		
tiezi=[]
class spider(object):
	# request, 然后创立一个soup对象的文件
	def __init__(self,Path=defaultPath):
		self.urllist=[] #备份request过的网页
		self.tiezi=[]#for tieba
		self.path=Path
		self.fo=fileOperator(Path)
		if !os.path.exist("spider_db.db"):
			''' if db not exist, create one'''
			dbfile=open("spider_db.db","w")
			dbfile.close()
			self.db=dbOperator('spider_db.db')
			self.db.cu.execute("CREATE TABLE tiezi(tieziUrl varchar(200),barname varchar(20))")
		else:
			self.db=dbOperator('spider_db.db','tiezi')
		self.barName=''
		self.tieName=''

	def request(self,url):
		self.url=url 
		self.urllist.append(url) #备份

		#在这里加入代理

		#加入完成

		print('开始请求！')
		try:
			urlData=requests.get(url,timeout=10) #request with header #取消header怕封号
		except:
			print('请求超时 等待下一次请求')
			time.sleep(20)
			self.request(url)
		finally:
			pass
		print('完成请求！')
		self.soup=BeautifulSoup(urlData.text,'lxml') #initiate soup
		print('完成解析！')

		#print出问题了哈哈哈哈

	# get tiezi if self.soup is a page in tieba
	# 进入数据库！
	def getTiezi(self):
		for i in self.soup.find_all('a',class_='j_th_tit'):
			tieziUrl='http://tieba.baidu.com'+i.get('href')
			try:
				self.db.insert([tieziUrl,self.barName])
			except Exception as e:
				print(e)
				pass


	def getImgInTiezi(self):# just one page
		 #把一页里的图统统放进列表 然后传给隔壁
		for img in self.soup.find_all('img',class_='BDE_Image'):
			src=img.get('src')
		#print(src)
			self.imageList.append(src)
		#fo=fileOperator(self.path) #for test, default
		self.fo.downloadImg(self.imageList,self.barName)

	def getPageNum(self):
		red=self.soup.find_all('span',class_='red')
		print(red[1].get_text())
		print([i.get_text() for i in red])
		pageNum=int(red[1].get_text()) #get the num of pages
		#30页不能更多
		if pageNum>30:
			pageNum=30
		return pageNum

	def formTiezi(self):
		self.tiezi=self.db.select()
		#useless



	def getImgInTieba(self): # all pages
		print('调用ImgInTieba开始') #别逼我他妈的
		# self.tiezi=self.db.select() # input the data
		#为了加快县城速度 这一步写外面
		
		#第一步 打印！
		
		# if len(self.tiezi)==0:
		# 	print('抱歉没东西了')
		# 	return
		#程序宣布 任务完成		

		 #第一步 搞到所有需要玩的帖子
		 #第二步 从列表里一个一个扒图咯
		global tiezi
		if len(tiezi)==0:
			print('工作完成')
			return
		else:
			print('剩余帖子 '+str(len(tiezi)))
		j=tiezi.pop() #妈的让你在重复
		self.db.delete(j[0]) #首先 首要 把帖子从db里删了 以免多线程被扰乱

		for i in self.tiezi:
			print(i)
		print('帖子数量',len(self.tiezi))

		self.imageList=[] # 首先 开一个空帖子 然后imglist的起始直是空的
		i=j[0]# 网址
		self.barName=j[1]#吧名
		#BarName Entrance
		 #delete it in db 既然开扒 那还要图片网址做什么呢
		try:
			print('下一个帖子！')
			self.request(i+'?see_lz=1') #enter the tiezi at first #从一个帖子开始
			#搞到标题
			try:
				self.tieName=self.soup('title')[0].get_text().encode('utf-8','replace').decode('utf-8','replace')
				print(self.tieName)
			except:
				pass

			#搞到页数
			pageNum=self.getPageNum()
			
			#第一页扒图
			for img in self.soup.find_all('img',class_='BDE_Image'):
				src=img.get('src')
				#print(src)
				self.imageList.append(src)
			#test
			#print(self.imageList)

			if pageNum>1 and len(self.imageList)>0: #他妈的如果比一夜多 而且 第一页有图
				for j in range(2,1+pageNum):
					print('帖子的下一页！')
					self.request(i+'?see_lz=1&pn=%s'%(str(j)))
					for img in self.soup.find_all('img',class_='BDE_Image'):
						src=img.get('src')
					#print(src)
						self.imageList.append(src)
			
		except:
			print('Sorry出错了')
		finally:
			threading.Thread(target=self.fo.downloadImg,args=(self.imageList,self.barName,self.tieName)).start()
			if len(tiezi)>0:
				self.getImgInTieba()
				


	def getTieba(self,barName,times=5):
		self.barName=barName
		for i in range(0,times): #350 per times #3times for more bar #or200 if like
			tiebaUrl='http://tieba.baidu.com/f?kw=%s&ie=utf-8&pn=%s'%(barName,str(i*200)) 
			print(tiebaUrl) #test
			print('贴吧的下一页！')
			self.request(tiebaUrl) #这里爬黑丝吧
			self.getTiezi()
		self.db.commit()

	def getGoodInTieba(self,barName,times=5):
		self.barName=barName
		try:
			for i in range(0,times): #350 per times #3times for more bar #or200 if like
				tiebaUrl='http://tieba.baidu.com/f/good?kw=%s&ie=utf-8&cid=0&pn=%s'%(barName,str(i*50)) 
				print(tiebaUrl) #test
				print('贴吧的下一页！')
				self.request(tiebaUrl) #这里爬黑丝吧
				self.getTiezi()
		except:
			print('出错了')
		self.db.commit()





#多线程实验开始
#一次测试失败 什么没有thread模块？

#19:31开始
#当前速度 平均1秒1.5-2张
#今日目标 提升到3-4张

#0315未完成的工作交给0316了

adder=[spider('E:\GoodSpiders\\tiebaSpider\images') for i in range(10)]
a='1'
tester=adder[0]
th=[]
for i in range(10):
	if a=='0':
		b=input('普通帖子or精品帖子？(0/1)')
		c=input('贴吧名字？')
		d=input('爬几页？')
		tester=adder[i]
		try: #他妈的精品就没这么多页
			if b=='0':
				th.append(threading.Thread(target=tester.getTieba,args=(c,int(d))))
			else:
				th.append(threading.Thread(target=tester.getGoodInTieba,args=(c,int(d))))
			th[-1].start()
		except:
			pass
		finally:
			print('Ok')


tester=spider('E:\GoodSpiders\\tiebaSpider\images')
print('开始扒图！')
testers=[spider('E:\GoodSpiders\\tiebaSpider\images') for i in range(10)]
print('testers就绪')
tiezi=tester.db.select()
for t in testers:
	#t.formTiezi()
	th=threading.Thread(target=t.getImgInTieba)
	print('开始工作')
	th.start()



def keepOn():
	try:
		tester.getImgInTieba()
	except:
		tester.db.delete(tester.db.select()[0][0])
		tester.getImgInTieba()



# print('完成工作！')
# a=input()

#今后跑测试之前 先设计好测试strategic 再继续吧
def operate():
	a=input('添加帖子or继续爬取？(0/1)')

	if a=='0':
		b=input('普通帖子or精品帖子？(0/1)')
		c=input('贴吧名字？')
		d=input('爬几页？')

		
		try: #他妈的精品就没这么多页
			if b=='0':
				tester.getTieba(c,int(d))
			else:
				tester.getGoodInTieba(c,int(d))
		finally:
			for i in tester.db.select():
				print(i)
			tester.db.commit()
			tester.db.conn.close()
	else:
		testers=[spider('E:\GoodSpiders\\tiebaSpider\images') for i in range(10)]

		print('开始工作')

		print('testers就绪')
		for t in testers:
			try:
				t.formTiezi()
			except:
				print('Failed To Form')
			th=threading.Thread(target=t.getImgInTieba())
			th.start()

#main
def main():
	a='1'
	while a=='1':
		operate()
		a=input('One query finished, Keep On or Exit?(1 or 0)')
	print('完成！')
	tester.db.finishDb()
	a=input()



	#原来sqldb的db默认为cursor啊
	#get了





# tester.getTieba('黑丝')
# for i in tester.tiezi:
# 	print(i)
# 测试一通过
# 1 慎用print 2 print出的结果注释出来
# 多放提示性print

#this, n times please
# tester.getTieba('搞笑图片',5)
# tester.getTieba('药娘四区',8)
# tester.getTieba('表情包',5)
# tester.getImgInTieba()

# tester=spider('E:\Good Spiders\heisi spider\images-摄影')


# tester.getGoodInTieba('摄影',8)


# tester.getImgInTieba()
'''
http://tieba.baidu.com/p/4329762670
'''
#tester.request('http://tieba.baidu.com/p/3350881165?see_lz=1&pn=1')
#testinNum=tester.soup.find_all(class_='red')

#测试二通过
#测试数据和运行数据应该分离




















